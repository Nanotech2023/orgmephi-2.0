from flask import request, make_response

from common import get_current_app, get_current_module
from common.errors import AlreadyExists
from common.util import db_get_one_or_none
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Olympiad types


@module.route('/olympiad_type/create', methods=['POST'])
def olympiad_type_create():
    values = request.openapi.body

    olympiad_type = values['olympiad_type']

    try:
        type_of_olympiad = db_get_one_or_none(OlympiadType, "olympiad_type", str(olympiad_type))
        if type_of_olympiad is not None:
            raise AlreadyExists('olympiad_type', olympiad_type)
        olympiad = add_olympiad_type(db.session,
                                     olympiad_type=olympiad_type)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response(
        {
            'olympiad_type_id': olympiad.olympiad_type_id
        }, 200)


@module.route('/olympiad_type/<int:id_olympiad_type>/remove', methods=['POST'])
def olympiad_type_remove(id_olympiad_type):
    """
    Remove olympiad type
    """
    try:
        olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
        db.session.delete(olympiad)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return make_response({}, 200)
