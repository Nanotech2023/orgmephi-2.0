import datetime
import secrets
import string
import sys
from threading import Thread
from flask import request, render_template, abort, send_file
from flask_mail import Message
from marshmallow import EXCLUDE
from itsdangerous import URLSafeTimedSerializer
from captcha.image import ImageCaptcha

from common.errors import AlreadyExists, NotFound, CaptchaError, WrongType, InsufficientData
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_all, db_get_or_raise, db_get_one_or_none, db_exists
from common.jwt_verify import jwt_required, jwt_get_id

from user.models import init_user, UserRoleEnum, University, Country, Region, UserInfo
from user.model_schemas.auth import User, UserSchema, Captcha
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.university import StudentInfoSchema

from .schemas import *
from ..util import get_username_case_insensitive, get_email_case_insensitive_or_raise, \
    get_email_case_insensitive_or_none

db = get_current_db()
module = get_current_module()
app = get_current_app()


def dump_email_token(claims, token_type):
    serializer = URLSafeTimedSerializer(app.config['ORGMEPHI_MAIL_CONFIRM_KEY'])
    token = serializer.dumps({'claims': claims, 'type': token_type}, salt=app.config['ORGMEPHI_MAIL_CONFIRM_SALT'])
    if app.config.get('TESTING', False):
        app.config['TESTING_LAST_EMAIL_TOKEN'] = token
    return token


def load_email_token(token, token_type, return_timestamp=False):
    serializer = URLSafeTimedSerializer(app.config['ORGMEPHI_MAIL_CONFIRM_KEY'])
    try:
        values, timestamp = serializer.loads(
            token,
            salt=app.config['ORGMEPHI_MAIL_CONFIRM_SALT'],
            max_age=app.config['ORGMEPHI_MAIL_CONFIRM_EXPIRATION'].total_seconds(),
            return_timestamp=True
        )
        received_type = values['type']
        claims = values['claims']
    except Exception:
        raise NotFound('token', token)
    if received_type != token_type:
        raise NotFound('token', token)
    if return_timestamp:
        return claims, timestamp
    return claims


class EmailThread(Thread):
    def __init__(self, app, message):
        self.app = app
        self.message = message
        Thread.__init__(self)

    def run(self):
        with self.app.app.app_context():
            app.mail.send(self.message)


def send_email(subject, recipient, template_name_or_list, **context):
    msg_body = render_template(template_name_or_list, **context)
    msg = Message(subject=subject, body=msg_body, html=msg_body, recipients=[recipient])
    app.mail.send(msg)
    # email = EmailThread(app, msg)
    # email.start()


_captcha_chars = string.ascii_uppercase + string.digits
_captcha_chars = _captcha_chars.replace('1', '').replace('I', '').replace('0', '').replace('O', '')


def send_email_confirmation(email):
    token = dump_email_token(email, 'confirm')
    subj = app.config['ORGMEPHI_MAIL_CONFIRM_SUBJECT']
    send_email(subj, email, 'email_confirmation.html', confirmation_token=token, title=subj)


def generate_captcha(width, height):
    captcha_gen = ImageCaptcha(width=width, height=height)
    captcha_len = app.config['ORGMEPHI_CAPTCHA_LENGTH']

    answer = ''.join(secrets.choice(_captcha_chars) for _ in range(captcha_len))
    while db_exists(db.session, Captcha, 'answer', answer):
        answer = secrets.token_urlsafe(app.config['ORGMEPHI_CAPTCHA_LENGTH'])
    image = captcha_gen.generate(answer)
    Captcha.cleanup()
    captcha = Captcha(answer=answer)
    db.session.add(captcha)
    db.session.commit()
    return image


def check_captcha(answer):
    Captcha.cleanup()
    captcha = db_get_one_or_none(Captcha, 'answer', answer)
    if captcha is None:
        raise CaptchaError()
    db.session.delete(captcha)
    db.session.commit()


def register(values):
    if app.config['ORGMEPHI_CAPTCHA_ENABLE']:
        answer = values.get('captcha', '')
        check_captcha(answer)

    username = values['auth_info']['email']
    reg_type = values['register_type']
    password_hash = app.password_policy.hash_password(values['auth_info']['password'], check=True)
    email_confirm = app.config.get('ORGMEPHI_CONFIRM_EMAIL', False)

    existing_user = get_username_case_insensitive(username)
    if existing_user is not None:
        age = datetime.date.today() - existing_user.registration_date.date()
        max_age = app.config['ORGMEPHI_MAIL_CONFIRM_EXPIRATION']
        if existing_user.role == UserRoleEnum.unconfirmed \
                and existing_user.type != UserTypeEnum.pre_register \
                and age > max_age:
            db.session.delete(existing_user)
            db.session.flush()
        else:
            raise AlreadyExists('email', username)

    default_role = UserRoleEnum.unconfirmed if email_confirm else UserRoleEnum.participant

    register_confirm = values.get('register_confirm', None)
    if register_confirm is not None:
        user_id = register_confirm['registration_number']
        user = db_get_or_raise(User, 'id', user_id)
        if user.type != UserTypeEnum.pre_register:
            raise NotFound('id', user_id)
        app.password_policy.validate_password(register_confirm['password'], user.password_hash)
        init_user(username, password_hash, default_role, reg_type, user=user)
    else:
        user = init_user(username, password_hash, default_role, reg_type)
        db.session.add(user)

    UserInfoSchema(load_instance=True).load(request.json['personal_info'], instance=user.user_info, session=db.session,
                                            partial=False, unknown=EXCLUDE)
    user.user_info.email = username

    if reg_type == UserTypeEnum.university:
        StudentInfoSchema(load_instance=True, only=['grade', 'university']) \
            .load(request.json['student_info'], instance=user.student_info, session=db.session, partial=False,
                  unknown=EXCLUDE)
        UserInfoSchema(only=['dwelling', 'phone'], load_instance=True).load(request.json['student_info'],
                                                                            instance=user.user_info,
                                                                            session=db.session,
                                                                            partial=False, unknown=EXCLUDE)

    if email_confirm:
        send_email_confirmation(user.user_info.email)

    db.session.commit()
    return user


@module.route('/captcha', methods=['GET'])
def get_captcha():
    """
    Generate captcha
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            image/png:
              schema:
                type: string
                format: binary
    """
    captcha = generate_captcha(280, 90)
    return send_file(captcha, mimetype='image/png')


@module.route('/school', methods=['POST'],
              input_schema=SchoolRegistrationRequestUserSchema, output_schema=UserSchema)
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
            schema: SchoolRegistrationRequestUserSchema
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
    return register(request.marshmallow), 200


@module.route('/university', methods=['POST'], output_schema=UserSchema,
              input_schema=UniversityRegistrationRequestUserSchema(exclude=['student_info']))
def register_university():
    """
    Register a university student
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: UniversityRegistrationRequestUserSchema
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
    return register(request.marshmallow), 200


@module.route('/resend/<string:email>', methods=['POST'])
def resend_email(email):
    """
    Resend email confirmation message
    ---
    post:
      parameters:
        - in: path
          description: Email
          name: email
          required: true
          schema:
            type: string
      responses:
        '204':
          description: OK
        '404':
          description: User not found
        '409':
          description: User is already confirmed
    """
    if not app.config.get('ORGMEPHI_CONFIRM_EMAIL', False):
        abort(404)
    user_info = get_email_case_insensitive_or_raise(email)
    if user_info.user.role != UserRoleEnum.unconfirmed or user_info.user.type == UserTypeEnum.pre_register:
        raise WrongType('User is already confirmed')
    send_email_confirmation(user_info.email)
    return {}, 204


@module.route('/resend', methods=['POST'])
@jwt_required()
def resend_email_auth():
    """
    Resend email confirmation message for authorized user
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '409':
          description: User is already confirmed or is not linked to email
    """
    if not app.config.get('ORGMEPHI_CONFIRM_EMAIL', False):
        abort(404)
    user = db_get_or_raise(User, 'id', jwt_get_id())
    if user.role != UserRoleEnum.unconfirmed or user.type == UserTypeEnum.pre_register:
        raise WrongType('User is already confirmed')
    if getattr(getattr(user, 'user_info', None), 'email', None) is None:
        raise InsufficientData('user', 'email')
    send_email_confirmation(user.user_info.email)
    return {}, 204


@module.route('/confirm/<string:token>', methods=['POST'])
def confirm_email(token):
    """
    Confirm email
    ---
    post:
      parameters:
        - in: path
          description: Email confirmation token
          name: token
          required: true
          schema:
            type: string
      responses:
        '204':
          description: OK
        '404':
          description: Wrong token
    """
    if not app.config.get('ORGMEPHI_CONFIRM_EMAIL', False):
        abort(404)
    email = load_email_token(token, 'confirm')
    if not isinstance(email, str):
        raise NotFound('token', token)
    user_info = get_email_case_insensitive_or_raise(email)
    if user_info.user.role == UserRoleEnum.unconfirmed:
        user_info.user.role = UserRoleEnum.participant
    else:
        raise NotFound('token', token)
    db.session.commit()
    return {}, 204


@module.route('/forgot/<string:email>', methods=['POST'])
def forgot_password(email):
    """
    send email for password recovery
    ---
    post:
      parameters:
        - in: path
          description: User's email
          name: email
          required: true
          schema:
            type: string
      responses:
        '204':
          description: OK
    """
    if not app.config.get('ORGMEPHI_ENABLE_PASSWORD_RECOVERY', False):
        abort(404)
    user = getattr(get_email_case_insensitive_or_none(email), 'user', None)
    if user is None:
        return {}, 204
    token = dump_email_token(user.user_info.email, 'recover')
    subj = app.config['ORGMEPHI_MAIL_RECOVER_SUBJECT']
    send_email(subj, user.user_info.email, 'password_reset.html', reset_token=token, title=subj)
    return {}, 204


@module.route('/recover/<string:token>', methods=['POST'], input_schema=ResetPasswordUserSchema)
def recover_password(token):
    """
    Recover password
    ---
    post:
      parameters:
        - in: path
          description: Recovery token
          name: token
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema: ResetPasswordUserSchema
      responses:
        '204':
          description: OK
    """
    if not app.config.get('ORGMEPHI_ENABLE_PASSWORD_RECOVERY', False):
        abort(404)
    email, timestamp = load_email_token(token, 'recover', True)
    user = getattr(get_email_case_insensitive_or_none(email), 'user', None)
    if user is None:
        raise NotFound('token', token)
    if user.password_changed.replace(tzinfo=datetime.timezone.utc) > timestamp.replace(tzinfo=datetime.timezone.utc):
        raise NotFound('token', token)
    values = request.marshmallow
    password_hash = app.password_policy.hash_password(values['password'], check=True)
    user.password_hash = password_hash
    user.password_changed = datetime.datetime.utcnow()
    db.session.commit()
    return {}, 204


@module.route('/info/universities', methods=['GET'], output_schema=InfoUniversitiesResponseUserSchema)
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
              schema: InfoUniversitiesResponseUserSchema
    """
    return {"university_list": db_get_all(University)}, 200


@module.route('/info/countries', methods=['GET'], output_schema=InfoCountriesResponseUserSchema)
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
              schema: InfoCountriesResponseUserSchema
    """
    return {"country_list": db_get_all(Country)}, 200


@module.route('/info/regions', methods=['GET'], output_schema=InfoRegionsResponseUserSchema)
def get_regions():
    """
    Get known RF region list
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: InfoRegionsResponseUserSchema
    """
    return {"region_list": db_get_all(Region)}, 200


@module.route('/info/cities/<string:region>', methods=['GET'], output_schema=InfoCitiesResponseUserSchema)
def get_cities(region):
    """
    Get cities within the region
    ---
    get:
      parameters:
        - in: path
          description: Region name
          name: region
          required: true
          schema:
            type: string
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: InfoCitiesResponseUserSchema
        '404':
          description: Region not found
    """
    region_obj = db_get_or_raise(Region, 'name', region)
    return {"city_list": region_obj.cities}, 200
