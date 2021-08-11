from flask import request, make_response

from common.errors import WrongCredentials
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_one_or_none, db_get_or_raise
from common.jwt_verify import jwt_required, jwt_get_id
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies,\
    get_csrf_token, unset_jwt_cookies, get_jwt

from user.models import User

db = get_current_db()
module = get_current_module()
app = get_current_app()


def generate_access_token(user_id, name, role):
    additional_claims = {"name": name, "role": role}
    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    csrf_access_token = get_csrf_token(access_token)
    return access_token, csrf_access_token


def generate_refresh_token(user_id, remember_me):
    additional_claims = {"remember": remember_me}
    if remember_me:
        refresh_token = create_refresh_token(identity=user_id, expires_delta=app.config['ORGMEPHI_REMEMBER_ME_TIME'],
                                             additional_claims=additional_claims)
    else:
        refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)
    csrf_refresh_token = get_csrf_token(refresh_token)
    return refresh_token, csrf_refresh_token


@module.route('/login', methods=['POST'])
def login():
    values = request.openapi.body
    user = db_get_one_or_none(User, 'username', values['auth_credentials']['username'])

    if user is not None:
        app.password_policy.validate_password(values['auth_credentials']['password'], user.password_hash)
    else:
        # align response times
        app.password_policy.validate_password(values['auth_credentials']['password'],
                                              '$pbkdf2-sha256$29000$h8DWeu8dg3CudQ4BAACg1A'
                                              '$JMTWWR9uLxzruMTaZObU8CJxMJoDTjJPwfL.aboeCIM')
        raise WrongCredentials

    access_token, access_csrf = generate_access_token(user.id, user.username, user.role.value)
    refresh_token, refresh_csrf = generate_refresh_token(user.id, values['remember_me'])

    response = make_response(
        {
            "csrf_access_token": access_csrf,
            "csrf_refresh_token": refresh_csrf
        }, 200)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@module.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = jwt_get_id()
    user = db_get_or_raise(User, "id", user_id)
    access_token, access_csrf = generate_access_token(user_id, user.username, user.role.value)
    refresh_token, refresh_csrf = generate_refresh_token(user_id, get_jwt()['remember'])

    response = make_response(
        {
            "csrf_access_token": access_csrf,
            "csrf_refresh_token": refresh_csrf
        }, 200)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@module.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response({}, 200)
    unset_jwt_cookies(response)
    return response
