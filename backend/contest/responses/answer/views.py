from flask import request, make_response
from contest.responses.models import *
from common.errors import NotFound
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_or_raise
from contest.responses.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


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


@module.route('/contest/<int:contest_id>/answer/<int:answer_id>', methods=['GET'])
def get_user_answer_by_id(contest_id, answer_id):
    user_answer = db_get_or_raise(ResponseAnswer, 'answer_id', answer_id)
    return make_response(
        {
            "user_answer": str(user_answer.answer),  # TODO BLOB not for json
            "filetype": user_answer.filetype.value
        }, 200)


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


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>', methods=['GET'])
def user_answer_for_task_by_id(contest_id, task_id, user_id):
    user_answer = user_answer_get(user_id, contest_id, task_id)
    return make_response(user_answer, 200)


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/<string:filetype>', methods=['POST'])
def user_answer_for_task_by_id_post(contest_id, task_id, user_id, filetype):
    answer = request.data
    user_answer_post(answer, filetype, user_id, contest_id, task_id)
    return make_response({}, 200)
