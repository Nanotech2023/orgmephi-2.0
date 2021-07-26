import datetime

from flask import request, make_response

from contest_data.models_responses import *
from contest_data import app, db, openapi


@app.route('/olympiad/<olympiad_id>/stage/<stage_id>/contest/<contest_id>/user/<user_id>/response:', methods=['GET'])
@openapi
def get_user_all_answers(olympiad_id, stage_id, contest_id, user_id):
    try:
        # TODO Add Checking
        user_work = Response.query.filter_by(user_id=user_id). \
            filter_by(contest_id=contest_id).first()
        user_work.answers.all()
        user_answer = []
        for elem in user_work:
            user_answer.append(
                {
                    'task_id': elem.task_num,
                    'answer_id': elem.answer_id
                }
            )
        return make_response(
                {
                    "user_id": user_work.user_id,
                    "work_id": user_work.work_id,
                    "contest_id": user_work.contest_id,
                    "user_answer": user_answer
                }, 200)
    except Exception as err:   # TODO Add exception
        pass


