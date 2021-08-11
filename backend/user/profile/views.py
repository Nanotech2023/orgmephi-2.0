from flask import request, make_response

from common.errors import NotFound
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise
from common.jwt_verify import jwt_required, jwt_get_id

from user.models import User

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/user', methods=['GET'])
def get_user_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    return make_response(user.serialize(), 200)


@module.route('/password', methods=['POST'])
def change_password_self():
    from user.util import update_password
    values = request.openapi.body
    user_id = jwt_get_id()
    return update_password(user_id, values['new_password'], values['old_password'], False)


@module.route('/personal', methods=['GET'])
def get_user_info_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.user_info is None:
        raise NotFound('user.personal_info', 'for user %d' % user.id)
    return make_response(user.user_info.serialize(), 200)


@module.route('/university', methods=['GET'])
def get_university_info_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    if user.student_info is None:
        raise NotFound('user.university_info', 'for user %d' % user.id)
    return make_response(user.student_info.serialize(), 200)


@module.route('/groups', methods=['GET'])
def get_user_groups_self():
    user = db_get_or_raise(User, "id", jwt_get_id())
    groups = [grp.serialize() for grp in user.groups]
    return make_response({'groups': groups}, 200)
