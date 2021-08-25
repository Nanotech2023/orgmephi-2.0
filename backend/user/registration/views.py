import datetime

from flask import request, render_template
from flask_mail import Message
from marshmallow import EXCLUDE
from itsdangerous import URLSafeTimedSerializer

from common.errors import AlreadyExists, NotFound
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_all, db_get_or_raise, db_get_one_or_none

from user.models import add_user, UserRoleEnum, University, Country, Region, UserInfo
from user.model_schemas.auth import UserSchema
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.university import StudentInfoSchema

from .schemas import *


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


def generate_email_token(email):
    serializer = URLSafeTimedSerializer(app.config['ORGMEPHI_MAIL_CONFIRM_KEY'])
    token = serializer.dumps(email, salt=app.config['ORGMEPHI_MAIL_CONFIRM_SALT'])
    return token


def send_email_confirmation(user):
    token = generate_email_token(user.user_info.email)
    subj = app.config['ORGMEPHI_MAIL_CONFIRM_SUBJECT']
    # noinspection PyUnresolvedReferences
    msg_body = render_template('email_confirmation.html', confirmation_token=token)
    msg = Message(subject=subj, body=msg_body, html=msg_body, recipients=[user.user_info.email])

    app.mail.send(msg)


def register():
    values = request.marshmallow
    username = values['auth_info']['email']
    reg_type = values['register_type']
    password_hash = app.password_policy.hash_password(values['auth_info']['password'], check=True)
    email_confirm = app.config.get('ORGMEPHI_CONFIRM_EMAIL', False)

    existing_user = db_get_one_or_none(UserInfo, 'email', username)
    if existing_user is not None:
        age = datetime.date.today() - existing_user.user.registration_date.date()
        max_age = app.config['ORGMEPHI_MAIL_CONFIRM_EXPIRATION']
        if existing_user.user.role == UserRoleEnum.unconfirmed and age > max_age:
            db.session.delete(existing_user.user)
            db.session.flush()
        else:
            raise AlreadyExists('email', username)

    default_role = UserRoleEnum.unconfirmed if email_confirm else UserRoleEnum.participant
    user = add_user(db.session, username, password_hash, default_role, reg_type)
    UserInfoSchema(load_instance=True).load(request.json['personal_info'], instance=user.user_info,
                                            session=db.session, partial=False, unknown=EXCLUDE)
    user.user_info.email = username

    if reg_type == UserTypeEnum.university:
        StudentInfoSchema(load_instance=True).load(request.json['student_info'], instance=user.student_info,
                                                   session=db.session, partial=False, unknown=EXCLUDE)
        UserInfoSchema(only=['dwelling', 'phone'], load_instance=True).load(request.json['student_info'],
                                                                            instance=user.user_info,
                                                                            session=db.session,
                                                                            partial=False, unknown=EXCLUDE)

    if email_confirm:
        send_email_confirmation(user)

    db.session.commit()
    return user


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
    return register(), 200


@module.route('/university', methods=['POST'],
              input_schema=UniversityRegistrationRequestUserSchema, output_schema=UserSchema)
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
    return register(), 200


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
    serializer = URLSafeTimedSerializer(app.config['ORGMEPHI_MAIL_CONFIRM_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['ORGMEPHI_MAIL_CONFIRM_SALT'],
            max_age=app.config['ORGMEPHI_MAIL_CONFIRM_EXPIRATION'].total_seconds()
        )
    except Exception:
        raise NotFound('token', token)
    user_info = db_get_or_raise(UserInfo, 'email', email)
    if user_info.user.role == UserRoleEnum.unconfirmed:
        user_info.user.role = UserRoleEnum.participant
    else:
        raise NotFound('token', token)
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
