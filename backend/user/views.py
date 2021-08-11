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


def get_missing(values, search):
    return [value for value in search if value not in values]


def update_password(user_id, new_password, old_password, admin=False):
    user = db_get_or_raise(User, "id", user_id)
    if not admin:
        app.password_policy.validate_password(old_password, user.password_hash)
    password_hash = app.password_policy.hash_password(new_password, check=not admin)
    user.password_hash = password_hash
    db.session.commit()
    return make_response({}, 200)


@module.route('/register/internal', methods=['POST'])
@jwt_required_role(['Admin', 'System'])
def register_internal():
    values = request.openapi.body
    username = values['username']
    password_hash = app.password_policy.hash_password(values['password'], check=False)
    try:
        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, UserTypeEnum.internal)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)
    except Exception:
        db.session.rollback()
        raise
    return make_response(user.serialize(), 200)


@module.route('/preregister', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def preregister():
    abort(501)

# User info


@module.route('/user/self', methods=['GET'])
@jwt_required()
def get_user_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    return make_response(user.serialize(), 200)


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


# Password

@module.route('/user/self/password', methods=['POST'])
@jwt_required()
def change_password_self():
    values = request.openapi.body
    user_id = jwt_get_id()
    return update_password(user_id, values['new_password'], values['old_password'], False)


@module.route('/user/<int:user_id>/password', methods=['POST'])
@jwt_required_role(['Admin'])
def change_password_admin(user_id):
    values = request.openapi.body
    return update_password(user_id, values['new_password'], None, True)


# Permissions

@module.route('/user/<int:user_id>/role', methods=['PUT'])
@jwt_required_role(['Admin', 'System'])
def set_user_role(user_id):
    role = user_roles[request.openapi.body['role']]
    user = db_get_or_raise(User, 'id', user_id)
    user.role = role
    db.session.commit()
    return make_response({}, 200)


@module.route('/user/<int:user_id>/type', methods=['PUT'])
@jwt_required_role(['Admin', 'System'])
def set_user_type(user_id):
    user_type = user_types[request.openapi.body['type']]
    user = db_get_or_raise(User, 'id', user_id)
    if user_type != UserTypeEnum.internal and user_type != UserTypeEnum.pre_register and user.user_info is None:
        raise InsufficientData('user', 'personal info')
    if user_type == UserTypeEnum.university and user.student_info is None:
        raise InsufficientData('user', 'university info')
    user.type = user_type
    db.session.commit()
    return make_response({}, 200)


# Personal info

@module.route('/user/self/personal', methods=['GET'])
@jwt_required()
def get_user_info_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


@module.route('/user/<int:user_id>/personal', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_info_admin(user_id):
    user = db_get_or_raise(User, "id", user_id)
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


@module.route('/user/<int:user_id>/personal', methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def set_user_info_admin(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    if 'email' in values:
        info = get_one_or_null(UserInfo, 'email', values['email'])
        if info is not None and info.user_id != user_id:
            raise AlreadyExists('user.email', values['email'])
    if user.user_info is None:
        missing = get_missing(values, ['email', 'first_name', 'second_name', 'middle_name', 'date_of_birth'])
        if len(missing) > 0:
            raise InsufficientData(str(missing), 'for user %d' % user.id)
        try:
            add_personal_info(db.session, user, values['email'], values['first_name'], values['second_name'],
                              values['middle_name'], values['date_of_birth'])
        except Exception:
            db.session.rollback()
            raise
    else:
        try:
            user.user_info.update(**values)
        except Exception:
            db.session.rollback()
            raise
    db.session.commit()
    return make_response(user.user_info.serialize(), 200)


# University info

@module.route('/user/self/university', methods=['GET'])
@jwt_required()
def get_university_info_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


@module.route('/user/<int:user_id>/university', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_university_info_admin(user_id):
    user = db_get_or_raise(User, "id", user_id)
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


@module.route('/user/<int:user_id>/university', methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def set_university_info_admin(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    if user.student_info is None:
        missing = get_missing(values, ['phone_number', 'university', 'admission_year', 'university_country',
                                       'citizenship', 'region', 'city'])
        if len(missing) > 0:
            raise InsufficientData(str(missing), 'for user %d' % user.id)
        try:
            add_university_info(db.session, user, values['phone_number'], values['university'],
                                values['admission_year'], values['university_country'], values['citizenship'],
                                values['region'], values['city'])
        except Exception:
            db.session.rollback()
            raise
    else:
        try:
            user.student_info.update(**values)
        except Exception:
            db.session.rollback()
            raise
    db.session.commit()
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


@module.route('/group/add', methods=['POST'])
@jwt_required_role(['Admin', 'System'])
def add_group_admin():
    values = request.openapi.body
    name = values['name']
    try:
        group = add_group(db.session, name)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('name', name)
    except Exception:
        db.session.rollback()
        raise
    return make_response(group.serialize(), 200)


@module.route('/group/<int:group_id>/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System'])
def remove_group_admin(group_id):
    group = db_get_or_raise(Group, 'id', group_id)
    db.session.delete(group)
    db.session.commit()
    return make_response({}, 200)


# User group management

@module.route('/user/self/groups', methods=['GET'])
@jwt_required()
def get_user_groups_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)


@module.route('/user/<int:user_id>/groups', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_groups_admin(user_id):
    user = db_get_or_raise(User, "id", user_id)
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)


@module.route('/user/<int:user_id>/groups/add', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def add_user_groups(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    group = db_get_or_raise(Group, 'id', values['group_id'])
    if user in group.users:
        raise AlreadyExists('group.users', str(user_id))
    group.users.append(user)
    db.session.commit()
    return make_response({}, 200)


@module.route('/user/<int:user_id>/groups/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def remove_user_groups(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    group = db_get_or_raise(Group, 'id', values['group_id'])
    if user not in group.users:
        raise NotFound('group.users', str(user_id))
    group.users.remove(user)
    db.session.commit()
    return make_response({}, 200)


# Reference Information


