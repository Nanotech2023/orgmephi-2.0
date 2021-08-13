from flask import request
from marshmallow import EXCLUDE

from common.errors import NotFound, AlreadyExists, InsufficientData
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise, db_get_one_or_none

from user.models import User, UserRoleEnum, UserTypeEnum, add_user, UserInfo, Group

from user.model_schemas.auth import UserSchema, GroupSchema
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.university import StudentInfoSchema

from .schemas import RegisterInternalRequestSchema, PasswordAdminRequestSchema, RoleRequestSchema, \
    TypeRequestSchema, GroupAddRequestSchema, MembershipRequestSchema, PreregisterResponseSchema

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/internal_register', methods=['POST'],
              input_schema=RegisterInternalRequestSchema, output_schema=UserSchema)
def register_internal():
    """
    Register an internal user
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: RegisterInternalRequestSchema
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
    import sqlalchemy.exc
    values = request.marshmallow
    username = values['username']
    password_hash = app.password_policy.hash_password(values['password'], check=False)
    try:
        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, UserTypeEnum.internal)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)

    return user, 200


@module.route('/preregister', methods=['POST'], output_schema=PreregisterResponseSchema)
def preregister():
    """
    !NOT IMPLEMENTED!
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
              schema: PreregisterResponseSchema
        '403':
          description: Invalid role of current user
    """
    from flask import abort
    abort(501)


@module.route('/password/<int:user_id>', methods=['POST'], input_schema=PasswordAdminRequestSchema)
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
            schema: PasswordAdminRequestSchema
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
    from user.util import update_password
    values = request.marshmallow
    return update_password(user_id, values['new_password'], None, True)


@module.route('/role/<int:user_id>', methods=['PUT'], input_schema=RoleRequestSchema)
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
            schema: RoleRequestSchema
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


@module.route('/type/<int:user_id>', methods=['PUT'], input_schema=TypeRequestSchema)
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
            schema: TypeRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: User not found
        '409':
          description: User is missing required info (e.g. university info for a university student)
    """
    user_type = request.marshmallow['type']
    user = db_get_or_raise(User, 'id', user_id)
    if user_type != UserTypeEnum.internal and user_type != UserTypeEnum.pre_register and user.user_info is None:
        raise InsufficientData('user', 'personal info')
    if user_type == UserTypeEnum.university and user.student_info is None:
        raise InsufficientData('user', 'university info')
    user.type = user_type
    db.session.commit()
    return {}, 200


@module.route('/personal/<int:user_id>', methods=['PATCH'], input_schema=UserInfoSchema)
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
        '409':
          description: Personal info is not set and request is not full
    """
    values = request.marshmallow
    user = db_get_or_raise(User, "id", user_id)
    if 'email' in values:
        info = db_get_one_or_none(UserInfo, 'email', values['email'])
        if info is not None and info.user_id != user_id:
            raise AlreadyExists('user.email', values['email'])
    if user.user_info is None:
        user.user_info = UserInfo()
    UserInfoSchema().load(request.json, session=db.session, instance=user.user_info, partial=True, unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/university/<int:user_id>', methods=['PATCH'], input_schema=StudentInfoSchema)
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
        '409':
          description: University info is not set and request is not full
    """
    from user.models.university import StudentInfo
    values = request.marshmallow
    user = db_get_or_raise(User, "id", user_id)
    if user.student_info is None:
        user.student_info = StudentInfo()
    StudentInfoSchema().load(request.json, session=db.session, instance=user.student_info, partial=True,
                             unknown=EXCLUDE)
    db.session.commit()
    return {}, 200


@module.route('/add_group', methods=['POST'], input_schema=GroupAddRequestSchema, output_schema=GroupSchema)
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
            schema: GroupAddRequestSchema
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
    import sqlalchemy.exc
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


@module.route('/add_member/<int:user_id>', methods=['POST'], input_schema=MembershipRequestSchema)
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
            schema: MembershipRequestSchema
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


@module.route('/remove_member/<int:user_id>', methods=['POST'], input_schema=MembershipRequestSchema)
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
            schema: MembershipRequestSchema
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
