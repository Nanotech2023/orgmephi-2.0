from flask import request, make_response
from contest.responses.models import *
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_list
from contest.responses.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/user/self/status', methods=['GET', 'POST'])
def user_status_and_mark_for_response(contest_id):
    self_user_id = jwt_get_id()
    if request.method == 'GET':
        return make_response(user_answer_status_get(self_user_id, contest_id), 200)
    elif request.method == 'POST':
        values = request.openapi.body
        user_answer_status_post(values, self_user_id, contest_id)
        return make_response({}, 200)


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status', methods=['GET', 'POST'])
def user_status_and_mark_for_response_by_id(contest_id, user_id):
    if request.method == 'GET':
        return make_response(user_answer_status_get(user_id, contest_id), 200)
    elif request.method == 'POST':
        values = request.openapi.body
        user_answer_status_post(values, user_id, contest_id)
        return make_response({}, 200)


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
