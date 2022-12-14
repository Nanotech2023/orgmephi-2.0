import secrets
from flask import request
from marshmallow import EXCLUDE
import sqlalchemy.exc

from common.errors import NotFound, AlreadyExists
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise, db_exists

from user.util import update_password

from user.models import User, init_user, UserInfo, Group, StudentInfo, SchoolInfo

from user.model_schemas.auth import UserSchema, GroupSchema
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.university import StudentInfoSchema
from user.model_schemas.school import SchoolInfoSchema

from .schemas import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/internal_register', methods=['POST'],
              input_schema=RegisterInternalRequestUserSchema, output_schema=UserSchema)
def register_internal():
    """
    Register an internal user
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: RegisterInternalRequestUserSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserSchema
        '400':
          description: Bad request
        '409':
          description: Username already in use
    """
    values = request.marshmallow
    username = values['username']
    password_hash = app.password_policy.hash_password(values['password'], check=False)
    try:
        user = init_user(username, password_hash, UserRoleEnum.participant, UserTypeEnum.internal)
        db.session.add(user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)

    return user, 200


@module.route('/preregister', methods=['POST'], output_schema=PreregisterResponseUserSchema)
def preregister():
    """
    Register an unconfirmed user with a one-time password
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: PreregisterResponseUserSchema
        '403':
          description: Invalid role of current user
    """
    rand_name = secrets.token_urlsafe(16)
    while db_exists(db.session, User, 'username', rand_name):
        rand_name = secrets.token_urlsafe(16)
    rand_pass = secrets.token_urlsafe(app.config['ORGMEPHI_PREREGISTER_PASSWORD_LENGTH'])
    user = User(username=rand_name, role=UserRoleEnum.unconfirmed, type=UserTypeEnum.pre_register)
    user.password_hash = app.password_policy.hash_password(rand_pass, check=False)
    db.session.add(user)
    db.session.commit()
    return {'registration_number': user.id, 'password': rand_pass}, 200


@module.route('/password/<int:user_id>', methods=['POST'], input_schema=PasswordRequestUserSchema)
def change_password_admin(user_id):
    """
    Change password for another user
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: PasswordRequestUserSchema
      responses:
        '200':
          description: OK
        '400':
          description: Bad request or weak password
        '403':
          description: Invalid role of current user
        '404':
          description: User not found
    """
    values = request.marshmallow
    return update_password(user_id, values['new_password'], None, True)


@module.route('/role/<int:user_id>', methods=['PUT'], input_schema=RoleRequestUserSchema)
def set_user_role(user_id):
    """
    Set the role of any user
    ---
    put:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: RoleRequestUserSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User not found
    """
    role = request.marshmallow['role']
    user = db_get_or_raise(User, 'id', user_id)
    user.role = role
    db.session.commit()
    return {}, 200


@module.route('/type/<int:user_id>', methods=['PUT'], input_schema=TypeRequestUserSchema)
def set_user_type(user_id):
    """
    Set the type of any user
    ---
    put:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: TypeRequestUserSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User not found
    """
    user_type = request.marshmallow['type']
    user = db_get_or_raise(User, 'id', user_id)
    user.type = user_type
    db.session.commit()
    return {}, 200


@module.route('/personal/<int:user_id>', methods=['PATCH'])
def set_user_info_admin(user_id):
    """
    Set personal info for a user
    ---
    patch:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
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
    user = db_get_or_raise(User, "id", user_id)
    if user.user_info is None:
        user.user_info = UserInfo()
    UserInfoSchema(load_instance=True).load(request.json, instance=user.user_info, session=db.session, partial=False,
                                            unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/university/<int:user_id>', methods=['PATCH'])
def set_university_info_admin(user_id):
    """
    Set university student info for a user
    ---
    patch:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
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
    user = db_get_or_raise(User, "id", user_id)
    if user.student_info is None:
        user.student_info = StudentInfo()
    StudentInfoSchema(load_instance=True).load(request.json, instance=user.student_info, session=db.session,
                                               partial=False, unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/school/<int:user_id>', methods=['PATCH'])
def set_school_info_admin(user_id):
    """
    Set school student info for a user
    ---
    patch:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
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
    user = db_get_or_raise(User, "id", user_id)
    if user.school_info is None:
        user.school_info = SchoolInfo()
    SchoolInfoSchema(load_instance=True).load(request.json, instance=user.school_info, session=db.session,
                                              partial=False, unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/add_group', methods=['POST'], input_schema=GroupAddRequestUserSchema, output_schema=GroupSchema)
def add_group_admin():
    """
    Add a group
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      requestBody:
        required: true
        content:
          application/json:
            schema: GroupAddRequestUserSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GroupSchema
        '403':
          description: Invalid role of current user
        '404':
          description: Group not found
        '409':
          description: Group already exists
    """
    values = request.marshmallow
    name = values['name']
    try:
        group = Group(name=name)
        db.session.add(group)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('name', name)
    return group, 200


@module.route('/remove_group/<int:group_id>', methods=['POST'])
def remove_group_admin(group_id):
    """
    Delete a group
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the group
          name: group_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: Group not found
    """
    group = db_get_or_raise(Group, 'id', group_id)
    db.session.delete(group)
    db.session.commit()
    return {}, 200


@module.route('/add_member/<int:user_id>', methods=['POST'], input_schema=MembershipRequestUserSchema)
def add_user_groups(user_id):
    """
    Assign a user to a group
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: MembershipRequestUserSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User or group not found
        '409':
          description: User already in the group
    """
    values = request.marshmallow
    user = db_get_or_raise(User, "id", user_id)
    group = db_get_or_raise(Group, 'id', values['group_id'])
    if user in group.users:
        raise AlreadyExists('group.users', str(user_id))
    group.users.append(user)
    db.session.commit()
    return {}, 200


@module.route('/remove_member/<int:user_id>', methods=['POST'], input_schema=MembershipRequestUserSchema)
def remove_user_groups(user_id):
    """
    Remove a user from a group
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: MembershipRequestUserSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User or group not found
    """
    values = request.marshmallow
    user = db_get_or_raise(User, "id", user_id)
    group = db_get_or_raise(Group, 'id', values['group_id'])
    if user not in group.users:
        raise NotFound('group.users', str(user_id))
    group.users.remove(user)
    db.session.commit()
    return {}, 200


@module.route('/personal/<int:user_id>/photo', methods=['PUT'])
def post_photo(user_id):
    """
    Edit photo
    ---
    put:
      parameters:
        - in: path
          description: ID of user
          name: user_id
          required: true
          schema:
            type: integer
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
    from common.media_types import ProfileImage
    user = db_get_or_raise(User, 'id', user_id)
    app.store_media('PROFILE', user.user_info, 'photo', ProfileImage)
    db.session.commit()
    return {}, 204


@module.route('/personal/<int:user_id>/photo', methods=['GET'])
def get_photo(user_id):
    """
    Get photo
    ---
    get:
      parameters:
        - in: path
          description: ID of user
          name: user_id
          required: true
          schema:
            type: integer
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
    user = db_get_or_raise(User, 'id', user_id)
    return app.send_media(user.user_info.photo)
