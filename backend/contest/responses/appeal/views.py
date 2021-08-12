from flask import request, make_response
from contest.responses.models import *
from common.errors import InsufficientData
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_or_raise, db_get_one_or_none
from contest.responses.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/user/self/appeal', methods=['POST'])
def user_response_appeal(contest_id):
    self_user_id = jwt_get_id()
    values = request.openapi.body
    return make_response(
        {
            'appeal_id': user_response_appeal_create(values, self_user_id, contest_id)
        }, 200)


@module.route('/contest/<int:contest_id>/user/<int:user_id>/appeal', methods=['POST'])
def user_response_appeal_by_id(contest_id, user_id):
    values = request.openapi.body
    return make_response(
        {
            'appeal_id': user_response_appeal_create(values, user_id, contest_id)
        }, 200)


@module.route('/contest/<int:contest_id>/appeal/<int:appeal_id>/reply', methods=['POST'])
def reply_to_user_appeal(contest_id, appeal_id):
    values = request.openapi.body
    search = ['message', 'accepted']
    missing = [value for value in search if value not in values]
    if len(missing) > 0:
        raise InsufficientData(str(missing), 'for appeal %d' % appeal_id)
    message = values['message']
    accepted = values['accepted']
    if accepted:
        appeal_new_status = appeal_status['AppealAccepted']
        response_new_status = 'Accepted'
    else:
        appeal_new_status = appeal_status['AppealRejected']
        response_new_status = 'Rejected'
    appeal = db_get_or_raise(Appeal, 'appeal_id', appeal_id)
    appeal.reply_to_appeal(message, appeal_new_status)
    db.session.commit()
    last_status = db_get_one_or_none(ResponseStatus, 'status_id', appeal.work_status)
    if 'new_mark' in values and accepted:
        new_mark = values['new_mark']
    else:
        new_mark = last_status.mark
    new_response_status = add_response_status(last_status.work_id, status=response_new_status,
                                              mark=new_mark)
    db.session.add(new_response_status)
    db.session.commit()
    return make_response(appeal.serialize(), 200)


@module.route('/contest/<int:contest_id>/appeal/<int:appeal_id>', methods=['GET'])
def get_appeal_info_by_id(contest_id, appeal_id):
    appeal = db_get_or_raise(Appeal, 'appeal_id', appeal_id)
    return make_response(appeal.serialize(), 200)
