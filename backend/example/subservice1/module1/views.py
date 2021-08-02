from flask import make_response

from example.subservice1.models import User

from common import get_current_module, get_current_db

module = get_current_module()
db = get_current_db()


@module.route('/add', methods=['POST'])
def add_user():
    user = User(name='string')
    db.session.add(user)
    db.session.commit()
    return make_response(user.serialize(), 200)
