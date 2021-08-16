from flask import request
import sqlalchemy.exc
from marshmallow import EXCLUDE

from common.errors import AlreadyExists
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_all

from user.models import add_user, UserRoleEnum, UserTypeEnum, University, Country, UserInfo, StudentInfo
from user.model_schemas.auth import UserSchema
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.university import StudentInfoSchema

from .schemas import SchoolRequestRegistrationSchema, UniversityRequestRegistrationSchema, \
    InfoUniversitiesResponseRegistrationSchema, InfoCountriesResponseRegistrationSchema


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
    values = request.marshmallow
    username = values['auth_info']['email']
    reg_type = values['register_type']
    password_hash = app.password_policy.hash_password(values['auth_info']['password'], check=True)

    try:
        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, reg_type)
        user.user_info = UserInfo()
        UserInfoSchema(load_instance=True).load(request.json['personal_info'], instance=user.user_info,
                                                session=db.session, partial=False, unknown=EXCLUDE)
        user.user_info.email = username

        if reg_type == UserTypeEnum.university:
            user.student_info = StudentInfo()
            StudentInfoSchema(load_instance=True).load(request.json['student_info'], instance=user.student_info,
                                                       session=db.session, partial=False, unknown=EXCLUDE)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as err:
        raise AlreadyExists('username', username)
    return user


@module.route('/school', methods=['POST'],
              input_schema=SchoolRequestRegistrationSchema, output_schema=UserSchema)
def register_school():
    """
    Register a school student
    ---
    post:
      summary: Register a new school student
      requestBody:
        required: true
        content:
          application/json:
            schema: SchoolRequestRegistrationSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserSchema
        '400':
          description: Bad request or weak password
        '409':
          description: Username already in use
    """
    return register(), 200


@module.route('/university', methods=['POST'],
              input_schema=UniversityRequestRegistrationSchema, output_schema=UserSchema)
def register_university():
    """
    Register a university student
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: UniversityRequestRegistrationSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserSchema
        '400':
          description: Bad request or weak password
        '409':
          description: Username already in use
    """
    return register(), 200


@module.route('/info/universities', methods=['GET'], output_schema=InfoUniversitiesResponseRegistrationSchema)
def get_universities():
    """
    Get known university list
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: InfoUniversitiesResponseRegistrationSchema
    """
    return {"university_list": db_get_all(University)}, 200


@module.route('/info/countries', methods=['GET'], output_schema=InfoCountriesResponseRegistrationSchema)
def get_countries():
    """
    Get known country list
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: InfoCountriesResponseRegistrationSchema
    """
    return {"country_list": db_get_all(Country)}, 200
