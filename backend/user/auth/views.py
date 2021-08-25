from flask import request, make_response

from common.errors import WrongCredentials, PermissionDenied
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_one_or_none, db_get_or_raise
from common.jwt_verify import jwt_required, jwt_get_id
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies,\
    get_csrf_token, unset_jwt_cookies, get_jwt

from user.models import User, UserRoleEnum

from .schemas import LoginRequestUserSchema

db = get_current_db()
module = get_current_module()
app = get_current_app()


def generate_access_token(user):
    additional_claims = {"name": user.username, "role": user.role.value}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    csrf_access_token = get_csrf_token(access_token)
    return access_token, csrf_access_token


def generate_refresh_token(user, original_user, remember_me):
    additional_claims = {"remember": remember_me, "orig_sub": original_user.id}

    if remember_me:
        expires_delta = app.config['ORGMEPHI_REMEMBER_ME_TIME']
    else:
        expires_delta = None

    refresh_token = create_refresh_token(identity=user.id, expires_delta=expires_delta,
                                         additional_claims=additional_claims)
    csrf_refresh_token = get_csrf_token(refresh_token)
    return refresh_token, csrf_refresh_token


def serve_tokens(user, original_user, remember_me):
    access_token, access_csrf = generate_access_token(user)
    refresh_token, refresh_csrf = generate_refresh_token(user, original_user, remember_me)

    response = make_response(
        {
            "csrf_access_token": access_csrf,
            "csrf_refresh_token": refresh_csrf
        }, 200)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@module.route('/login', methods=['POST'], input_schema=LoginRequestUserSchema)
def login():
    """
    Authenticate a user
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: LoginRequestUserSchema
      security: []
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
                example: access_token_cookie=eyJ0eXAi...; Path=/; HttpOnly
          content:
            application/json:
              schema: CSRFPairUserSchema
        '400':
          description: Bad request
        '401':
          description: Wrong credentials
    """
    values = request.marshmallow
    user = db_get_one_or_none(User, 'username', values['username'])

    if user is not None:
        app.password_policy.validate_password(values['password'], user.password_hash)
    else:
        # Align response times
        # noinspection SpellCheckingInspection
        app.password_policy.validate_password(values['password'],
                                              '$pbkdf2-sha256$29000$h8DWeu8dg3CudQ4BAACg1A'
                                              '$JMTWWR9uLxzruMTaZObU8CJxMJoDTjJPwfL.aboeCIM')
        raise WrongCredentials

    return serve_tokens(user, user, values['remember_me'])


@module.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh JWT token for current user
    ---
    post:
      security:
        - JWTRefreshToken: [ ]
        - CSRFRefreshToken: [ ]
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
                example: access_token_cookie=eyJ0eXAi...; Path=/; HttpOnly
          content:
            application/json:
              schema: CSRFPairUserSchema
    """
    user_id = jwt_get_id()
    user = db_get_or_raise(User, "id", user_id)

    orig_id = get_jwt()['orig_sub']
    orig_user = db_get_or_raise(User, "id", orig_id)

    return serve_tokens(user, orig_user, get_jwt()['remember'])


@module.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout current user
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
                example: access_token_cookie=deleted; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT
    """
    response = make_response({}, 200)
    unset_jwt_cookies(response)
    return response


@module.route('/impersonate/<int:user_id>', methods=['POST'])
@jwt_required(refresh=True)
def impersonate(user_id):
    """
    Impersonate a user
    ---
    post:
      security:
        - JWTRefreshToken: []
        - CSRFRefreshToken: []
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
                example: access_token_cookie=eyJ0eXAi...; Path=/; HttpOnly
          content:
            application/json:
              schema: CSRFPairUserSchema
        '404':
          description: User not found
    """
    orig_id = get_jwt()['orig_sub']
    orig_user = db_get_or_raise(User, "id", orig_id)
    if orig_user.role not in [UserRoleEnum.admin, UserRoleEnum.system]:
        raise PermissionDenied(['Admin', 'System'])

    user = db_get_or_raise(User, "id", user_id)

    return serve_tokens(user, orig_user, get_jwt()['remember'])


@module.route('/unimpersonate', methods=['POST'])
@jwt_required(refresh=True)
def unimpersonate():
    """
    Stop impersonating another user
    ---
    post:
      security:
        - JWTRefreshToken: []
        - CSRFRefreshToken: []
      responses:
        '200':
          description: OK
          headers:
            Set-Cookie:
              schema:
                description: Set both access_token_cookie and refresh_token_cookie
                type: string
                example: access_token_cookie=eyJ0eXAi...; Path=/; HttpOnly
          content:
            application/json:
              schema: CSRFPairUserSchema
    """
    orig_id = get_jwt()['orig_sub']
    orig_user = db_get_or_raise(User, "id", orig_id)

    return serve_tokens(orig_user, orig_user, get_jwt()['remember'])
