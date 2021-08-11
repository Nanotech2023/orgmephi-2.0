from flask import request, make_response

from common.errors import NotFound, AlreadyExists, InsufficientData
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise, db_get_one_or_none

from user.models import User, UserRoleEnum, UserTypeEnum, add_user, user_roles, user_types, create_personal_info, \
    UserInfo, create_university_info, add_group, Group

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/internal_register', methods=['POST'])
def register_internal():
    import sqlalchemy.exc
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
def preregister():
    from flask import abort
    abort(501)


@module.route('/password/<int:user_id>', methods=['POST'])
def change_password_admin(user_id):
    from user.util import update_password
    values = request.openapi.body
    return update_password(user_id, values['new_password'], None, True)


@module.route('/role/<int:user_id>', methods=['PUT'])
def set_user_role(user_id):
    role = user_roles[request.openapi.body['role']]
    user = db_get_or_raise(User, 'id', user_id)
    user.role = role
    db.session.commit()
    return make_response({}, 200)


@module.route('/type/<int:user_id>', methods=['PUT'])
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


def get_missing(values, search):
    return [value for value in search if value not in values]


@module.route('/personal/<int:user_id>', methods=['PATCH'])
def set_user_info_admin(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    if 'email' in values:
        info = db_get_one_or_none(UserInfo, 'email', values['email'])
        if info is not None and info.user_id != user_id:
            raise AlreadyExists('user.email', values['email'])
    if user.user_info is None:
        missing = get_missing(values, ['email', 'first_name', 'second_name', 'middle_name', 'date_of_birth'])
        if len(missing) > 0:
            raise InsufficientData(str(missing), 'for user %d' % user.id)
        try:
            user.user_info = create_personal_info(values['email'], values['first_name'], values['second_name'],
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


@module.route('/university/<int:user_id>', methods=['PATCH'])
def set_university_info_admin(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    if user.student_info is None:
        missing = get_missing(values, ['phone_number', 'university', 'admission_year', 'university_country',
                                       'citizenship', 'region', 'city'])
        if len(missing) > 0:
            raise InsufficientData(str(missing), 'for user %d' % user.id)
        try:
            user.student_info = create_university_info(values['phone_number'], values['university'],
                                                       values['admission_year'], values['university_country'],
                                                       values['citizenship'], values['region'], values['city'])
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


@module.route('/add_group', methods=['POST'])
def add_group_admin():
    import sqlalchemy.exc
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


@module.route('/remove_group/<int:group_id>', methods=['POST'])
def remove_group_admin(group_id):
    group = db_get_or_raise(Group, 'id', group_id)
    db.session.delete(group)
    db.session.commit()
    return make_response({}, 200)


@module.route('/add_member/<int:user_id>', methods=['POST'])
def add_user_groups(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    group = db_get_or_raise(Group, 'id', values['group_id'])
    if user in group.users:
        raise AlreadyExists('group.users', str(user_id))
    group.users.append(user)
    db.session.commit()
    return make_response({}, 200)


@module.route('/remove_member/<int:user_id>', methods=['POST'])
def remove_user_groups(user_id):
    values = request.openapi.body
    user = db_get_or_raise(User, "id", user_id)
    group = db_get_or_raise(Group, 'id', values['group_id'])
    if user not in group.users:
        raise NotFound('group.users', str(user_id))
    group.users.remove(user)
    db.session.commit()
    return make_response({}, 200)
