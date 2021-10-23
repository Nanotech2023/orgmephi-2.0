import io

from flask import request
from marshmallow import EXCLUDE

from common import get_current_app, get_current_module, get_current_db
from common.errors import NotFound, InsufficientData, WrongType, QuotaExceeded, DataConflict
from common.jwt_verify import jwt_get_id
from common.util import db_get_or_raise, send_pdf
from user.model_schemas.auth import UserSchema
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.school import SchoolInfoSchema
from user.model_schemas.university import StudentInfoSchema
from user.models import User, UserInfo, StudentInfo, SchoolInfo, UserTypeEnum
from .schemas import SelfPasswordRequestUserSchema, SelfGroupsResponseUserSchema

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/user', methods=['GET'], output_schema=UserSchema)
def get_user_self():
    """
    Get common info for current user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserSchema
        '404':
          description: User not found
    """
    return db_get_or_raise(User, "id", jwt_get_id()), 200


@module.route('/password', methods=['POST'], input_schema=SelfPasswordRequestUserSchema)
def change_password_self():
    """
    Change password for current user
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      requestBody:
        required: true
        content:
          application/json:
            schema: SelfPasswordRequestUserSchema
      responses:
        '200':
          description: OK
        '400':
          description: Bad request or weak password
        '401':
          description: Wrong credentials
        '404':
          description: User not found
    """
    from user.util import update_password
    values = request.marshmallow
    user_id = jwt_get_id()
    return update_password(user_id, values['new_password'], values['old_password'], False)


@module.route('/personal', methods=['GET'], output_schema=UserInfoSchema)
def get_user_info_self():
    """
    Get personal info for current user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserInfoSchema
        '404':
          description: Personal info is not set or user not found
    """
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return user.user_info, 200


@module.route('/personal', methods=['PATCH'])
def set_user_info_self():
    """
    Set personal info for current user
    ---
    patch:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      requestBody:
        description: Will not set 'email', 'first_name', 'middle_name', 'second_name' and 'date_of_birth'
        required: true
        content:
          application/json:
            schema: UserInfoSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User not found
    """
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.user_info is None:
        user.user_info = UserInfo()
    UserInfoSchema(load_instance=True, exclude=['email', 'first_name', 'middle_name', 'second_name', 'date_of_birth'])\
        .load(request.json, instance=user.user_info, session=db.session, partial=False, unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/university', methods=['GET'], output_schema=StudentInfoSchema)
def get_university_info_self():
    """
    Get university student info for current user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: StudentInfoSchema
        '404':
          description: User not found or is not a university student
    """
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return user.student_info, 200


@module.route('/university', methods=['PATCH'])
def set_university_info_self():
    """
    Set university student info for a user
    ---
    patch:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      requestBody:
        required: true
        content:
          application/json:
            schema: StudentInfoSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User not found or is not a university student
    """
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.student_info is None:
        user.student_info = StudentInfo()
    StudentInfoSchema(load_instance=True).load(request.json, instance=user.student_info, session=db.session,
                                               partial=False, unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/school', methods=['GET'], output_schema=SchoolInfoSchema)
def get_school_info_self():
    """
    Get school info for current user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: SchoolInfoSchema
        '404':
          description: User not found or is not a school student
    """
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.school_info is None:
        raise NotFound('user.school_info', 'for user %d' % user.id)
    return user.school_info, 200


@module.route('/school', methods=['PATCH'])
def set_school_info_self():
    """
    Set school student info for a user
    ---
    patch:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      requestBody:
        required: true
        content:
          application/json:
            schema: SchoolInfoSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User not found or is not a school student
    """
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.school_info is None:
        user.school_info = SchoolInfo()
    SchoolInfoSchema(load_instance=True).load(request.json, instance=user.school_info, session=db.session,
                                              partial=False, unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/groups', methods=['GET'], output_schema=SelfGroupsResponseUserSchema)
def get_user_groups_self():
    """
    Get groups for current user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: SelfGroupsResponseUserSchema
        '404':
          description: User not found
    """
    user = db_get_or_raise(User, "id", jwt_get_id())
    return {'groups': user.groups}, 200


@module.route('/unfilled', methods=['GET'])
def check_filled():
    """
    Get fields of a user that must be filled to take part in a contest
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/pdf:
              schema: SelfUnfilledResponseSchema
        '404':
          description: User not found
    """
    user = db_get_or_raise(User, 'id', jwt_get_id())
    return {'unfilled': user.unfilled()}, 200


@module.route('/card', methods=['GET'])
def generate_card():
    """
    Generate a participant card
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/pdf:
              schema:
                type: string
                format: binary
        '404':
          description: User not found
        '409':
          description: User is not a school student or has missing data
    """
    user = db_get_or_raise(User, 'id', jwt_get_id())
    if user.type not in [UserTypeEnum.pre_university, UserTypeEnum.enrollee, UserTypeEnum.school]:
        raise WrongType('User is not a school student')
    unfilled = user.unfilled()
    if len(unfilled) > 0:
        raise InsufficientData('user', str(unfilled))
    return send_pdf('participant_card.html', u=user)


@module.route('/photo', methods=['PUT'])
def post_photo():
    """
    Edit photo
    ---
    put:
      requestBody:
        required: true
        content:
          image/*:
            schema:
              type: string
              format: binary
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '409':
          description: File is too big

    """
    file = request.data
    if file == b'':
        raise InsufficientData('request', 'image')
    if len(file) > 4 * 1024 * 1024:
        raise QuotaExceeded('Image is too large', 4 * 1024 * 1024)
    user = db_get_or_raise(User, 'id', jwt_get_id())
    user.user_info.photo = file
    db.session.commit()
    return {}, 204


@module.route('/photo', methods=['GET'])
def get_photo():
    """
    Get photo
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            image/*:
              schema:
                type: string
                format: binary
        '404':
          description: User not found
        '409':
          description: Photo not attached
    """
    from flask import send_file
    user = db_get_or_raise(User, 'id', jwt_get_id())
    if user.user_info.photo is None:
        raise DataConflict('Image not present')
    return send_file(io.BytesIO(user.user_info.photo), mimetype='image/*')
