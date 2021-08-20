from common.errors import NotFound
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise, db_get_all

from user.models import User, Group
from user.model_schemas.auth import UserSchema, GroupSchema
from user.model_schemas.personal import UserInfoSchema
from user.model_schemas.university import StudentInfoSchema
from user.model_schemas.school import SchoolInfoSchema

from .schemas import GroupListResponseUserSchema, UserListResponseUserSchema, UserFullListResponseUserSchema

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/user/<int:user_id>', methods=['GET'], output_schema=UserSchema)
def get_user_admin(user_id):
    """
    Get common info for a different user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
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
          content:
            application/json:
              schema: UserSchema
        '403':
          description: Invalid role of current user
        '404':
          description: User not found
    """
    user = db_get_or_raise(User, "id", user_id)
    return user, 200


@module.route('/user/all', methods=['GET'], output_schema=UserListResponseUserSchema)
def get_user_all():
    """
    Get common info for all users
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserListResponseUserSchema
        '403':
          description: Invalid role of current user
    """
    users = db_get_all(User)
    return {'users': users}, 200


@module.route('/user_full/all', methods=['GET'], output_schema=UserFullListResponseUserSchema)
def get_user_full_all():
    """
    Get full info for all users
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserFullListResponseUserSchema
        '403':
          description: Invalid role of current user
    """
    users = db_get_all(User)
    return {'users': users}, 200


@module.route('/user/by-group/<int:group_id>', methods=['GET'], output_schema=UserListResponseUserSchema)
def get_user_by_group(group_id):
    """
    Get common info for different users
    ---
    get:
      security:
        - JWTAccessToken: [ ]
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
          content:
            application/json:
              schema: UserListResponseUserSchema
        '403':
          description: Invalid role of current user
        '404':
          description: Group not found
    """
    group = db_get_or_raise(Group, "id", group_id)
    return {'users': group.users}, 200


@module.route('/personal/<int:user_id>', methods=['GET'], output_schema=UserInfoSchema)
def get_user_info_admin(user_id):
    """
    Get personal info for any user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
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
          content:
            application/json:
              schema: UserInfoSchema
        '403':
          description: Invalid role of current user
        '404':
          description: Personal info is not set or user not found
    """
    user = db_get_or_raise(User, "id", user_id)
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return user.user_info, 200


@module.route('/university/<int:user_id>', methods=['GET'], output_schema=StudentInfoSchema)
def get_university_info_admin(user_id):
    """
    Get university student info for any user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
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
          content:
            application/json:
              schema: StudentInfoSchema
        '403':
          description: Invalid role of current user
        '404':
          description: User not found or is not a university student
    """
    user = db_get_or_raise(User, "id", user_id)
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return user.student_info, 200


@module.route('/school/<int:user_id>', methods=['GET'], output_schema=SchoolInfoSchema)
def get_school_info_admin(user_id):
    """
    Get school student info for any user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
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
          content:
            application/json:
              schema: SchoolInfoSchema
        '403':
          description: Invalid role of current user
        '404':
          description: User not found or is not a school student
    """
    user = db_get_or_raise(User, "id", user_id)
    if user.school_info is None:
        raise NotFound('user.school_info', 'for user %d' % user.id)
    return user.school_info, 200


@module.route('/group/<int:group_id>', methods=['GET'], output_schema=GroupSchema)
def get_group(group_id):
    """
    Get any group
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      parameters:
        - in: path
          description: Id of the group
          name: group_id
          required: true
          schema:
            type: integer
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
    """
    group = db_get_or_raise(Group, 'id', group_id)
    return group, 200


@module.route('/group/all', methods=['GET'], output_schema=GroupListResponseUserSchema)
def get_groups_all():
    """
    Get all groups
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GroupListResponseUserSchema
        '403':
          description: Invalid role of current user
    """
    groups = db_get_all(Group)
    return {'groups': groups}, 200


@module.route('/membership/<int:user_id>', methods=['GET'], output_schema=GroupListResponseUserSchema)
def get_user_groups_admin(user_id):
    """
    Get groups for a different user
    ---
    get:
      security:
        - JWTAccessToken: [ ]
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
          content:
            application/json:
              schema: GroupListResponseUserSchema
        '403':
          description: Invalid role of current user
        '404':
          description: User not found
    """
    user = db_get_or_raise(User, "id", user_id)
    return {'groups': user.groups}, 200
