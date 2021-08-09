from flask import make_response

from example.subservice1.models import User

from common import get_current_module
from common.util import db_get_or_raise

module = get_current_module()


@module.route('/get/<int:user_id>', methods=['GET'])
def add_user(user_id):
    user = db_get_or_raise(User, 'id', user_id)
    return make_response(user.serialize(), 200)
