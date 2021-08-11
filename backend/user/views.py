from flask import request, make_response, abort

import sqlalchemy.exc

from common.errors import NotFound, AlreadyExists, InsufficientData
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_or_raise

from .models import *

db = get_current_db()
module = get_current_module()
app = get_current_app()





# User info

@module.route('/user/<int:user_id>', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_admin(user_id):
    user = db_get_or_raise(User, "id", user_id)
    return make_response(user.serialize(), 200)


@module.route('/user/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_all():
    users = get_all(User)
    user_list = [user.serialize() for user in users]
    return make_response({'users': user_list}, 200)


@module.route('/user/by-group/<int:group_id>', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_by_group(group_id):
    group = db_get_or_raise(Group, "id", group_id)
    users = [value.serialize() for value in group.users]
    return make_response({'users': users}, 200)


# Personal info

@module.route('/user/<int:user_id>/personal', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_info_admin(user_id):
    user = db_get_or_raise(User, "id", user_id)
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


# University info

@module.route('/user/<int:user_id>/university', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_university_info_admin(user_id):
    user = db_get_or_raise(User, "id", user_id)
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


# Groups

@module.route('/group/<int:group_id>', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_group(group_id):
    group = db_get_or_raise(Group, 'id', group_id)
    return make_response(group.serialize(), 200)


@module.route('/group/all', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_groups_all():
    groups = get_all(Group)
    groups_dict = [grp.serialize() for grp in groups]
    return make_response({'groups': groups_dict}, 200)


# User group management

@module.route('/user/<int:user_id>/groups', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_groups_admin(user_id):
    user = db_get_or_raise(User, "id", user_id)
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)


