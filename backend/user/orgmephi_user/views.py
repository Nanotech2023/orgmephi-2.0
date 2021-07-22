import datetime

from flask import request, make_response
import re

from orgmephi_user.models import *
from orgmephi_user.errors import *
from orgmephi_user import app, db, openapi

user_roles = {
    'Participant': UserRoleEnum.participant,
    'Creator': UserRoleEnum.creator,
    'Admin': UserRoleEnum.admin,
    'System': UserRoleEnum.system
}

user_roles_reverse = {val: key for key, val in user_roles.items()}

user_types = {
    'PreUniversity': UserTypeEnum.pre_university,
    'Enrollee': UserTypeEnum.enrollee,
    'School': UserTypeEnum.school,
    'University': UserTypeEnum.university,
    'Internal': UserTypeEnum.internal,
    'PreRegister': UserTypeEnum.pre_register
}

user_types_reverse = {val: key for key, val in user_types.items()}


def check_auth_info(username, password):
    query = db.session.query(User).filter(User.username == username)
    if db.session.query(query.exists()).scalar():
        raise AlreadyExists('username', username)
    passcheck = app.config['ORGMEPHI_PASSWORD_POLICY'].test(password)
    if passcheck:
        raise WeakPassword(passcheck)


def grade_to_year(grade):
    now = datetime.utcnow().date()
    last_admission = datetime(now.year, 9, 1)
    if now > last_admission:
        last_admission = datetime(now.year - 1, 9, 1)
    admission_date = datetime(last_admission.year - grade + 1, 9, 1)
    return admission_date


email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


@app.route('/register', methods=['POST'])
@openapi
def register():
    try:
        values = request.openapi.body
        username = values['auth_info']['email']
        password = values['auth_info']['password']
        check_auth_info(username, password)
        if not email_regex.match(username):
            raise WrongValue('email', username)
        reg_type = user_types[values['register_type']]
        if reg_type == UserTypeEnum.university and 'student_info' not in values:
            raise MissingField('student_info')
        if reg_type == UserTypeEnum.pre_register or reg_type == UserTypeEnum.internal:
            raise WrongValue('register_type', values['register_type'])
        hash_policy = app.config['ORGMEPHI_PASSLIB_CONTEXT']
        password_hash = hash_policy.hash(password)
        user = User(
            username=username,
            password_hash=password_hash,
            role=UserRoleEnum.participant,
            type=reg_type
        )
        db.session.add(user)
        # Generate user.id
        db.session.flush()
        date_of_birth = values['personal_info']['date_of_birth']
        user_data = values['personal_info']
        user_info = UserInfo(
            user_id=user.id,
            email=username,
            first_name=user_data['first_name'],
            second_name=user_data['second_name'],
            middle_name=user_data['middle_name'],
            date_of_birth=date_of_birth
        )
        db.session.add(user_info)
        if reg_type == UserTypeEnum.university:
            student_data = values['student_info']
            university_name = student_data['university']
            university = University.query.filter(University.name == university_name).one_or_none
            student_info = StudentInfo(
                user_id=user.id,
                phone=student_data['phone_number'],
                university=(university.id if university is not None else None),
                custom_university=(university_name if university is None else None),
                admission_year=grade_to_year(student_data['grade']),
                university_country=student_data['university_country'],
                citizenship=student_data['citizenship'],
                region=student_data['region'],
                city=student_data['city']
            )
            db.session.add(student_info)
        db.session.commit()
        return make_response(
            {
                "id": user.id,
                "username": user.username,
                "role": user_roles_reverse[user.role],
                "type": user_types_reverse[user.type]
            }, 200)
    except RequestError as err:
        db.session.rollback()
        return err.to_response()
