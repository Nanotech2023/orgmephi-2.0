from flask import request
from marshmallow import EXCLUDE

from common.errors import NotFound
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise
from common.jwt_verify import jwt_get_id

from user.models import User, UserInfo, StudentInfo, SchoolInfo
from user.model_schemas.auth import UserSchema
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.university import StudentInfoSchema, StudentInfoInputSchema
from user.model_schemas.school import SchoolInfoSchema, SchoolInfoInputSchema

from .schemas import SelfPasswordRequestUserSchema, SelfGroupsResponseUserSchema, UserInfoRestrictedInputSchema

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


@module.route('/personal', methods=['PATCH'], input_schema=UserInfoRestrictedInputSchema)
def set_user_info_self():
    """
    Set personal info for current user
    ---
    patch:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      requestBody:
        required: true
        content:
          application/json:
            schema: UserInfoRestrictedInputSchema
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
    UserInfoSchema(load_instance=True).load(request.json, instance=user.user_info, session=db.session, partial=False,
                                            unknown=EXCLUDE)
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


@module.route('/university', methods=['PATCH'], input_schema=StudentInfoInputSchema)
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
            schema: StudentInfoInputSchema
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


@module.route('/school', methods=['PATCH'], input_schema=SchoolInfoInputSchema)
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
            schema: SchoolInfoInputSchema
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
