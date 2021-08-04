from functools import wraps

from flask import request, make_response, abort
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies,\
    get_csrf_token, unset_jwt_cookies, get_jwt
import sqlalchemy.exc

from common.errors import RequestError, NotFound, WrongCredentials, AlreadyExists, InsufficientData
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id

from .models import *

db = get_current_db()
module = get_current_module()
app = get_current_app()

user_roles = {role.value: role for role in UserRoleEnum}

user_types = {user_type.value: user_type for user_type in UserTypeEnum}


def catch_request_error(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except RequestError as err:
            return err.to_response()
    return wrapper


def get_or_raise(entity, field, value):
    result = get_one_or_null(entity, field, value)
    if result is None:
        raise NotFound(field, value)
    return result


def get_missing(values, search):
    missing = []
    for value in search:
        if value not in values:
            missing.append(value)
    return missing


def grade_to_year(grade):
    from datetime import date
    now = datetime.utcnow().date()
    last_admission = date(now.year, 9, 1)
    if now < last_admission:
        last_admission = date(now.year - 1, 9, 1)
    admission_date = date(last_admission.year - grade + 1, 9, 1)
    return admission_date


def update_password(user_id, new_password, old_password, admin=False):
    user = get_or_raise(User, "id", user_id)
    if not admin:
        app.password_policy.validate_password(old_password, user.password_hash)
    password_hash = app.password_policy.hash_password(new_password, check=not admin)
    user.password_hash = password_hash
    db.session.commit()
    return make_response({}, 200)


def generate_access_token(user_id, name, role):
    additional_claims = {"name": name, "role": role}
    access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
    csrf_access_token = get_csrf_token(access_token)
    return access_token, csrf_access_token


def generate_refresh_token(user_id, remember_me):
    additional_claims = {"remember": remember_me}
    if remember_me:
        refresh_token = create_refresh_token(identity=user_id, expires_delta=app.config['ORGMEPHI_REMEMBER_ME_TIME'],
                                             additional_claims=additional_claims)
    else:
        refresh_token = create_refresh_token(identity=user_id, additional_claims=additional_claims)
    csrf_refresh_token = get_csrf_token(refresh_token)
    return refresh_token, csrf_refresh_token


# Registration

def register():
    values = request.openapi.body
    username = values['auth_info']['email']
    reg_type = user_types[values['register_type']]
    password_hash = app.password_policy.hash_password(values['auth_info']['password'], check=True)

    user_data = values['personal_info']

    try:
        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, reg_type)
        add_personal_info(db.session, user, username, user_data['first_name'], user_data['second_name'],
                          user_data['middle_name'], user_data['date_of_birth'])

        if reg_type == UserTypeEnum.university:
            student_data = values['student_info']
            add_university_info(db.session, user, student_data['phone_number'], student_data['university'],
                                grade_to_year(student_data['grade']), student_data['university_country'],
                                student_data['citizenship'], student_data['region'], student_data['city'])

        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)
    except Exception:
        db.session.rollback()
        raise
    return make_response(user.serialize(), 200)


@module.route('/register/school', methods=['POST'])
def register_school():
    return register()


@module.route('/register/university', methods=['POST'])
def register_university():
    return register()


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


# Authentication

@module.route('/login', methods=['POST'])
def login():
    values = request.openapi.body
    user = get_one_or_null(User, 'username', values['auth_credentials']['username'])

    if user is not None:
        app.password_policy.validate_password(values['auth_credentials']['password'], user.password_hash)
    else:
        # align response times
        app.password_policy.validate_password(values['auth_credentials']['password'],
                                              '$pbkdf2-sha256$29000$h8DWeu8dg3CudQ4BAACg1A'
                                              '$JMTWWR9uLxzruMTaZObU8CJxMJoDTjJPwfL.aboeCIM')
        raise WrongCredentials

    access_token, access_csrf = generate_access_token(user.id, user.username, user.role.value)
    refresh_token, refresh_csrf = generate_refresh_token(user.id, values['remember_me'])

    response = make_response(
        {
            "csrf_access_token": access_csrf,
            "csrf_refresh_token": refresh_csrf
        }, 200)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@module.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = jwt_get_id()
    user = get_or_raise(User, "id", user_id)
    access_token, access_csrf = generate_access_token(user_id, user.username, user.role.value)
    refresh_token, refresh_csrf = generate_refresh_token(user_id, get_jwt()['remember'])

    response = make_response(
        {
            "csrf_access_token": access_csrf,
            "csrf_refresh_token": refresh_csrf
        }, 200)

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@module.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response({}, 200)
    unset_jwt_cookies(response)
    return response


# User info

@module.route('/user/self', methods=['GET'])
@jwt_required()
def get_user_self():
    user = get_or_raise(User, "id", jwt_get_id())
    return make_response(user.serialize(), 200)


@module.route('/user/<int:user_id>', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_admin(user_id):
    user = get_or_raise(User, "id", user_id)
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
    group = get_or_raise(Group, "id", group_id)
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
    user = get_or_raise(User, 'id', user_id)
    user.role = role
    db.session.commit()
    return make_response({}, 200)


@module.route('/user/<int:user_id>/type', methods=['PUT'])
@jwt_required_role(['Admin', 'System'])
def set_user_type(user_id):
    user_type = user_types[request.openapi.body['type']]
    user = get_or_raise(User, 'id', user_id)
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
    user = get_or_raise(User, "id", jwt_get_id())
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


@module.route('/user/<int:user_id>/personal', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_info_admin(user_id):
    user = get_or_raise(User, "id", user_id)
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


@module.route('/user/<int:user_id>/personal', methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def set_user_info_admin(user_id):
    values = request.openapi.body
    user = get_or_raise(User, "id", user_id)
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
    user = get_or_raise(User, "id", jwt_get_id())
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


@module.route('/user/<int:user_id>/university', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_university_info_admin(user_id):
    user = get_or_raise(User, "id", user_id)
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


@module.route('/user/<int:user_id>/university', methods=['PATCH'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def set_university_info_admin(user_id):
    values = request.openapi.body
    user = get_or_raise(User, "id", user_id)
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
    group = get_or_raise(Group, 'id', group_id)
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
    group = get_or_raise(Group, 'id', group_id)
    db.session.delete(group)
    db.session.commit()
    return make_response({}, 200)


# User group management

@module.route('/user/self/groups', methods=['GET'])
@jwt_required()
def get_user_groups_self():
    user = get_or_raise(User, "id", jwt_get_id())
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)


@module.route('/user/<int:user_id>/groups', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_user_groups_admin(user_id):
    user = get_or_raise(User, "id", user_id)
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)


@module.route('/user/<int:user_id>/groups/add', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def add_user_groups(user_id):
    values = request.openapi.body
    user = get_or_raise(User, "id", user_id)
    group = get_or_raise(Group, 'id', values['group_id'])
    if user in group.users:
        raise AlreadyExists('group.users', str(user_id))
    group.users.append(user)
    db.session.commit()
    return make_response({}, 200)


@module.route('/user/<int:user_id>/groups/remove', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def remove_user_groups(user_id):
    values = request.openapi.body
    user = get_or_raise(User, "id", user_id)
    group = get_or_raise(Group, 'id', values['group_id'])
    if user not in group.users:
        raise NotFound('group.users', str(user_id))
    group.users.remove(user)
    db.session.commit()
    return make_response({}, 200)


# Reference Information

@module.route('/info/universities', methods=['GET'])
def get_universities():
    universities = get_all(University)
    university_list = [uni.name for uni in universities]
    return make_response({'university_list': university_list}, 200)


@module.route('/info/countries', methods=['GET'])
def get_countries():
    countries = get_all(Country)
    country_list = [country.name for country in countries]
    return make_response({'country_list': country_list}, 200)
