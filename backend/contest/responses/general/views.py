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


@module.route('/contest/<int:contest_id>/appeal/<int:appeal_id>', methods=['GET'])
def get_appeal_info_by_id(contest_id, appeal_id):
    appeal = db_get_or_raise(Appeal, 'appeal_id', appeal_id)
    return make_response(appeal.serialize(), 200)
