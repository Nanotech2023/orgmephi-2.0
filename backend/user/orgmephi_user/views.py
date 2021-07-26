from os import getcwd

from flask import request, make_response, send_file
from flask_jwt_extended import create_access_token, set_access_cookies, \
    create_refresh_token, set_refresh_cookies, get_csrf_token

from orgmephi_user.models import *
from orgmephi_user.errors import RequestError, WeakPassword
from orgmephi_user import app, db, openapi
from orgmephi_user.jwt_verify import *

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


@app.route('/api.yaml', methods=['GET'])
def get_api():
    if not app.config['DEBUG']:
        abort(404)
    api_path = app.config['ORGMEPHI_API_PATH']
    if api_path[0] != '/':
        api_path = '%s/%s' % (getcwd(), api_path)
    return send_file(api_path)


def grade_to_year(grade):
    now = datetime.utcnow().date()
    last_admission = datetime(now.year, 9, 1)
    if now > last_admission:
        last_admission = datetime(now.year - 1, 9, 1)
    admission_date = datetime(last_admission.year - grade + 1, 9, 1)
    return admission_date


def hash_password(password):
    pass_check = app.config['ORGMEPHI_PASSWORD_POLICY'].test(password)
    if pass_check:
        raise WeakPassword(pass_check)
    hash_policy = app.config['ORGMEPHI_PASSLIB_CONTEXT']
    password_hash = hash_policy.hash(password)
    return password_hash


@app.route('/register', methods=['POST'])
@openapi
def register():
    try:
        values = request.openapi.body
        username = values['auth_info']['email']
        reg_type = user_types[values['register_type']]
        password_hash = hash_password(values['auth_info']['password'])

        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, reg_type)
        user_data = values['personal_info']
        add_personal_info(db.session, user, username, user_data['first_name'], user_data['second_name'],
                          user_data['middle_name'], user_data['date_of_birth'])

        if reg_type == UserTypeEnum.university:
            student_data = values['student_info']
            add_university_info(db.session, user, student_data['phone_number'], student_data['university'],
                                grade_to_year(student_data['grade']), student_data['university_country'],
                                student_data['citizenship'], student_data['region'], student_data['city'])

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


def validate_password(password, password_hash):
    hash_policy = app.config['ORGMEPHI_PASSLIB_CONTEXT']
    if not hash_policy.verify(password, password_hash):
        abort(401)


def generate_access_token(user):
    additional_claims = {"name": user.username, "role": user_roles_reverse[user.role]}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    csrf_access_token = get_csrf_token(access_token)
    return access_token, csrf_access_token


def generate_refresh_token(user, remember_me):
    if remember_me:
        refresh_token = create_refresh_token(identity=user.id, expires_delta=app.config['ORGMEPHI_REMEMBER_ME_TIME'])
    else:
        refresh_token = create_refresh_token(identity=user.id)
    csrf_refresh_token = get_csrf_token(refresh_token)
    return refresh_token, csrf_refresh_token


@app.route('/login', methods=['POST'])
@openapi
def login():
    values = request.openapi.body
    user = get_user_by_name(values['auth_credentials']['username'])

    if user is not None:
        validate_password(values['auth_credentials']['password'], user.password_hash)
    else:
        # align response times
        validate_password(values['auth_credentials']['password'],
                          '$pbkdf2-sha256$29000$h8DWeu8dg3CudQ4BAACg1A$JMTWWR9uLxzruMTaZObU8CJxMJoDTjJPwfL.aboeCIM')
        abort(401)

    access_token, access_csrf = generate_access_token(user)
    refresh_token, refresh_csrf = generate_refresh_token(user, values['remember_me'])

    response = make_response(
        {
            "csrf_access_token": access_csrf,
            "csrf_refresh_token": refresh_csrf
        }, 200)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response
