from os import getcwd

from flask import request, make_response, send_file
from flask_jwt_extended import create_access_token, set_access_cookies, create_refresh_token, set_refresh_cookies,\
    get_csrf_token, jwt_required, unset_jwt_cookies
import sqlalchemy.exc

from orgmephi_user.models import *
from orgmephi_user.errors import RequestError, WeakPassword, NotFound, WrongCredentials, AlreadyExists, InsufficientData
from orgmephi_user import app, db, openapi
from orgmephi_user.jwt_verify import *

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


@app.route('/api.yaml', methods=['GET'])
def get_api():
    if app.config['ENV'] != 'development':
        abort(404)
    api_path = app.config['ORGMEPHI_API_PATH']
    if api_path[0] != '/':
        api_path = '%s/%s' % (getcwd(), api_path)
    return send_file(api_path)


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
    now = datetime.utcnow().date()
    last_admission = datetime(now.year, 9, 1)
    if now > last_admission:
        last_admission = datetime(now.year - 1, 9, 1)
    admission_date = datetime(last_admission.year - grade + 1, 9, 1)
    return admission_date


def hash_password(password, force=False):
    if not force:
        pass_check = app.config['ORGMEPHI_PASSWORD_POLICY'].test(password)
        if pass_check:
            raise WeakPassword(pass_check)
    hash_policy = app.config['ORGMEPHI_PASSLIB_CONTEXT']
    password_hash = hash_policy.hash(password)
    return password_hash


@app.route('/register', methods=['POST'])
@openapi
@catch_request_error
def register():
    values = request.openapi.body
    username = values['auth_info']['email']
    reg_type = user_types[values['register_type']]
    password_hash = hash_password(values['auth_info']['password'])

    user_data = values['personal_info']
    student_data = values['student_info']

    try:
        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, reg_type)
        add_personal_info(db.session, user, username, user_data['first_name'], user_data['second_name'],
                          user_data['middle_name'], user_data['date_of_birth'])

        if reg_type == UserTypeEnum.university:
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


@app.route('/register/internal', methods=['POST'])
@openapi
@jwt_required_role(['Admin', 'System'])
@catch_request_error
def register_internal():
    values = request.openapi.body
    username = values['username']
    password_hash = hash_password(values['password'], force=True)
    try:
        user = add_user(db.session, username, password_hash, UserRoleEnum.participant, UserTypeEnum.internal)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('username', username)
    except Exception:
        db.session.rollback()
        raise
    return make_response(user.serialize(), 200)


def validate_password(password, password_hash):
    hash_policy = app.config['ORGMEPHI_PASSLIB_CONTEXT']
    if not hash_policy.verify(password, password_hash):
        abort(401)


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


@app.route('/login', methods=['POST'])
@openapi
@catch_request_error
def login():
    values = request.openapi.body
    user = get_one_or_null(User, 'username', values['auth_credentials']['username'])

    if user is not None:
        validate_password(values['auth_credentials']['password'], user.password_hash)
    else:
        # align response times
        validate_password(values['auth_credentials']['password'],
                          '$pbkdf2-sha256$29000$h8DWeu8dg3CudQ4BAACg1A$JMTWWR9uLxzruMTaZObU8CJxMJoDTjJPwfL.aboeCIM')
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


@app.route('/refresh', methods=['POST'])
@openapi
@jwt_required(refresh=True)
@catch_request_error
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


@app.route('/logout', methods=['POST'])
@openapi
@jwt_required()
@catch_request_error
def logout():
    response = make_response({}, 200)
    unset_jwt_cookies(response)
    return response


def update_password(user_id, new_password, old_password, admin=False):
    user = get_or_raise(User, "id", user_id)
    if not admin:
        validate_password(old_password, user.password_hash)
    password_hash = hash_password(new_password, force=admin)
    user.password_hash = password_hash
    db.session.commit()
    return make_response({}, 200)


@app.route('/user/<int:user_id>/password', methods=['POST'])
@openapi
@jwt_required_role(['Admin'])
@catch_request_error
def change_password_admin(user_id):
    values = request.openapi.body
    return update_password(user_id, values['new_password'], None, True)


@app.route('/user/self/password', methods=['POST'])
@openapi
@jwt_required()
@catch_request_error
def change_password_self():
    values = request.openapi.body
    user_id = jwt_get_id()
    return update_password(user_id, values['new_password'], values['old_password'], False)


@app.route('/user/self', methods=['GET'])
@openapi
@jwt_required()
@catch_request_error
def get_user_self():
    user = get_or_raise(User, "id", jwt_get_id())
    return make_response(user.serialize(), 200)


@app.route('/user/<int:user_id>', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_user_admin(user_id):
    user = get_or_raise(User, "id", user_id)
    return make_response(user.serialize(), 200)


@app.route('/user/by-group/<int:group_id>', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_user_by_group(group_id):
    group = get_or_raise(Group, "id", group_id)
    users = [value.serialize() for value in group.users]
    return make_response({'users': users}, 200)


@app.route('/user/self/groups', methods=['GET'])
@openapi
@jwt_required()
@catch_request_error
def get_user_groups_self():
    user = get_or_raise(User, "id", jwt_get_id())
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)


@app.route('/user/<int:user_id>/groups', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_user_groups_admin(user_id):
    user = get_or_raise(User, "id", user_id)
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)


@app.route('/user/<int:user_id>/groups/add', methods=['POST'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def add_user_groups(user_id):
    values = request.openapi.body
    user = get_or_raise(User, "id", user_id)
    group = get_or_raise(Group, 'id', values['group_id'])
    if user in group.users:
        raise AlreadyExists('group.users', str(user_id))
    group.users.append(user)
    db.session.commit()
    return make_response({}, 200)


@app.route('/user/<int:user_id>/groups/remove', methods=['POST'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def remove_user_groups(user_id):
    values = request.openapi.body
    user = get_or_raise(User, "id", user_id)
    group = get_or_raise(Group, 'id', values['group_id'])
    if user not in group.users:
        raise NotFound('group.users', str(user_id))
    group.users.remove(user)
    db.session.commit()
    return make_response({}, 200)


@app.route('/group/all', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_groups_all():
    groups = get_all(Group)
    groups_dict = [grp.serialize() for grp in groups]
    return make_response({'groups': groups_dict}, 200)


@app.route('/group/<int:group_id>', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_group(group_id):
    group = get_or_raise(Group, 'id', group_id)
    return make_response(group.serialize(), 200)


@app.route('/group/add', methods=['POST'])
@openapi
@jwt_required_role(['Admin', 'System'])
@catch_request_error
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


@app.route('/group/<int:group_id>/delete', methods=['POST'])
@openapi
@jwt_required_role(['Admin', 'System'])
@catch_request_error
def delete_group_admin(group_id):
    group = get_or_raise(Group, 'id', group_id)
    db.session.delete(group)
    db.session.commit()
    return make_response({}, 200)


@app.route('/info/universities', methods=['GET'])
@openapi
@catch_request_error
def get_universities():
    universities = get_all(University)
    university_list = [uni.name for uni in universities]
    return make_response({'university_list': university_list}, 200)


@app.route('/info/countries', methods=['GET'])
@openapi
@catch_request_error
def get_countries():
    countries = get_all(Country)
    country_list = [country.name for country in countries]
    return make_response({'country_list': country_list}, 200)


@app.route('/user/all', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_user_all():
    users = get_all(User)
    user_list = [user.serialize() for user in users]
    return make_response({'users': user_list}, 200)


@app.route('/user/<int:user_id>/role', methods=['PUT'])
@openapi
@jwt_required_role(['Admin', 'System'])
@catch_request_error
def set_user_role(user_id):
    role = user_roles[request.openapi.body['role']]
    user = get_or_raise(User, 'id', user_id)
    user.role = role
    db.session.commit()
    return make_response({}, 200)


@app.route('/user/<int:user_id>/type', methods=['PUT'])
@openapi
@jwt_required_role(['Admin', 'System'])
@catch_request_error
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


@app.route('/user/self/personal', methods=['GET'])
@openapi
@jwt_required()
@catch_request_error
def get_user_info_self():
    user = get_or_raise(User, "id", jwt_get_id())
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


@app.route('/user/<int:user_id>/personal', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_user_info_admin(user_id):
    user = get_or_raise(User, "id", user_id)
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


@app.route('/user/<int:user_id>/personal', methods=['PATCH'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def set_user_info_admin(user_id):
    values = request.openapi.body
    user = get_or_raise(User, "id", user_id)
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


@app.route('/user/self/university', methods=['GET'])
@openapi
@jwt_required()
@catch_request_error
def get_university_info_self():
    user = get_or_raise(User, "id", jwt_get_id())
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


@app.route('/user/<int:user_id>/university', methods=['GET'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
def get_university_info_admin(user_id):
    user = get_or_raise(User, "id", user_id)
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


@app.route('/user/<int:user_id>/university', methods=['PATCH'])
@openapi
@jwt_required_role(['Admin', 'System', 'Creator'])
@catch_request_error
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
