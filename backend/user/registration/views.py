from flask import request, make_response
import sqlalchemy.exc

from common.errors import AlreadyExists
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_all

from user.models import user_types, add_user, UserRoleEnum, UserTypeEnum, add_personal_info, create_university_info, \
    University, Country

db = get_current_db()
module = get_current_module()
app = get_current_app()


def grade_to_year(grade):
    from datetime import date, datetime
    now = datetime.utcnow().date()
    last_admission = date(now.year, 9, 1)
    if now < last_admission:
        last_admission = date(now.year - 1, 9, 1)
    admission_date = date(last_admission.year - grade + 1, 9, 1)
    return admission_date


def register():
    values = request.openapi.body
    username = values['auth_info']['email']
    reg_type = user_types[values['register_type']]
    password_hash = app.password_policy.hash_password(values['auth_info']['password'], check=True)

    user_data = values['personal_info']

    try:
        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, reg_type)
        add_personal_info(db.session, user, username, user_data['first_name'], user_data['second_name'],
                          user_data['middle_name'], user_data['date_of_birth'])

        if reg_type == UserTypeEnum.university:
            student_data = values['student_info']
            user.student_info = create_university_info(db.session, student_data['phone_number'],
                                                       student_data['university'], grade_to_year(student_data['grade']),
                                                       student_data['university_country'], student_data['citizenship'],
                                                       student_data['region'], student_data['city'])

        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)
    except Exception:
        db.session.rollback()
        raise
    return make_response(user.serialize(), 200)


@module.route('/school', methods=['POST'])
def register_school():
    return register()


@module.route('/university', methods=['POST'])
def register_university():
    return register()


@module.route('/info/universities', methods=['GET'])
def get_universities():
    universities = db_get_all(University)
    university_list = [uni.name for uni in universities]
    return make_response({'university_list': university_list}, 200)


@module.route('/info/countries', methods=['GET'])
def get_countries():
    countries = db_get_all(Country)
    country_list = [country.name for country in countries]
    return make_response({'country_list': country_list}, 200)
