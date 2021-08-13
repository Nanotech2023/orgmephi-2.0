from flask import request, make_response
from contest.responses.models import *
from common.errors import NotFound, InsufficientData
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_or_raise
from contest.responses.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>', methods=['GET'])
def user_answer_for_task_by_id(contest_id, task_id, user_id):
    user_answer = user_answer_get(user_id, contest_id, task_id)
    return make_response(user_answer, 200)


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/<string:filetype>', methods=['POST'])
def user_answer_for_task_by_id_post(contest_id, task_id, user_id, filetype):
    answer = request.data
    user_answer_post(answer, filetype, user_id, contest_id, task_id)
    return make_response({}, 200)


@module.route('/contest/<int:contest_id>/user/<int:user_id>/response', methods=['GET'])
def get_user_all_answers(contest_id, user_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if user_work.answers is None:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    answers = user_work.answers
    user_answer = [elem.serialize() for elem in answers]
    return make_response(
        {
            "user_id": user_work.user_id,
            "work_id": user_work.work_id,
            "contest_id": user_work.contest_id,
            "user_answers": user_answer
        }, 200)


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status', methods=['GET', 'POST'])
def user_status_and_mark_for_response_by_id(contest_id, user_id):
    if request.method == 'GET':
        return make_response(user_answer_status_get(user_id, contest_id), 200)
    elif request.method == 'POST':
        values = request.openapi.body
        user_answer_status_post(values, user_id, contest_id)
        return make_response({}, 200)


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status/history', methods=['GET'])
def user_status_history_for_response_by_id(contest_id, user_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    status = user_work.statuses
    history = [elem.status_for_history() for elem in status]
    return make_response(
        {
            'user_id': user_id,
            'contest_id': contest_id,
            'history': history
        }, 200)


@module.route('/contest/<int:contest_id>/list/', methods=['GET'])
def get_list_for_stage(contest_id):
    users_in_contest = db_get_list(Response, 'contest_id', contest_id)
    user_rows = [elem.prepare_for_list() for elem in users_in_contest]
    return make_response(
        {
            'contest_id': contest_id,
            'user_row': user_rows
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
