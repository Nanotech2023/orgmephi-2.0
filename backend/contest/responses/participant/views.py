from flask import request, make_response
from contest.responses.models import *
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_list
from contest.responses.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self', methods=['GET'])
def user_answer_for_task(contest_id, task_id):
    self_user_id = jwt_get_id()
    user_answer = user_answer_get(self_user_id, contest_id, task_id)
    return make_response(user_answer, 200)


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/<string:filetype>', methods=['POST'])
def user_answer_for_task_post(contest_id, task_id, filetype):
    self_user_id = jwt_get_id()
    answer = request.data
    user_answer_post(answer, filetype, self_user_id, contest_id, task_id)
    return make_response({}, 200)


@module.route('/contest/<int:contest_id>/answer/<int:answer_id>', methods=['GET'])
def get_user_answer_by_id(contest_id, answer_id):
    user_answer = db_get_or_raise(ResponseAnswer, 'answer_id', answer_id)
    return make_response(
        {
            "user_answer": str(user_answer.answer),  # TODO BLOB not for json
            "filetype": user_answer.filetype.value
        }, 200)


@module.route('/contest/<int:contest_id>/user/self/status', methods=['GET'])
def user_status_and_mark_for_response(contest_id):
    self_user_id = jwt_get_id()
    return make_response(user_answer_status_get(self_user_id, contest_id), 200)


@module.route('/contest/<int:contest_id>/user/self/status/history', methods=['GET'])
def user_status_history_for_response(contest_id):
    self_user_id = jwt_get_id()
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    status = user_work.statuses
    history = [elem.status_for_history() for elem in status]
    return make_response(
        {
            'user_id': self_user_id,
            'contest_id': contest_id,
            'history': history
        }, 200)

@module.route('/contest/<int:contest_id>/user/self/appeal', methods=['POST'])
def user_response_appeal(contest_id):
    self_user_id = jwt_get_id()
    values = request.openapi.body
    return make_response(
        {
            'appeal_id': user_response_appeal_create(values, self_user_id, contest_id)
        }, 200)


@module.route('/contest/<int:contest_id>/appeal/<int:appeal_id>', methods=['GET'])
def get_appeal_info_by_id(contest_id, appeal_id):
    appeal = db_get_or_raise(Appeal, 'appeal_id', appeal_id)
    return make_response(appeal.serialize(), 200)
