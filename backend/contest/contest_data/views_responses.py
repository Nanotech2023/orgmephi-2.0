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
            filter_by(contest_id=contest_id).one()
        answers = user_work.answers.all()
        user_answer = []
        for elem in answers:
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
    except Exception as err:  # TODO Add exception
        pass


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/answer/{answer_id}', methods=['GET'])
@openapi
def get_user_answer_by_id(olympiad_id, stage_id, contest_id, answer_id):
    try:
        # TODO Add Checking
        user_answer = ResponseAnswer.query.filter_by(anwer_id=answer_id).one()
        return make_response(
            {
                "user_answer": user_answer.answer,
                "filetype": user_answer.filetype
            }, 200)
    except Exception as err:  # TODO Add exception
        pass


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/task/{task_id}/user/self:',
           methods=['GET', 'POST'])
@openapi
def user_answer_for_task(olympiad_id, stage_id, contest_id, task_id):
    pass


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/task/{task_id}/user/{user_id}:',
           methods=['GET', 'POST'])
@openapi
def user_answer_for_task_by_id(olympiad_id, stage_id, contest_id, task_id, user_id):
    try:
        # TODO Add Checking
        if request.method == 'GET':
            user_work = Response.query.filter_by(user_id=user_id). \
                filter_by(contest_id=contest_id).one()
            user_answer = user_work.answers.filter_by(task_num=task_id).one()
            return make_response(
                {
                    "user_answer": user_answer.answer,
                    "filetype": user_answer.filetype
                }, 200)
        elif request.method == 'POST':
            # TODO Add Checking
            values = request.openapi.body
            answer = values['user_answer']
            filetype = values['filetype']
            user_work = Response.query.filter_by(user_id=user_id). \
                filter_by(contest_id=contest_id).one()
            user_answer = user_work.answers.filter_by(task_num=task_id).first()
            if user_answer is None:
                response_answer = ResponseAnswer(
                    work_id=user_work.work_id,
                    task_num=task_id,
                    answer=answer,
                    filetype=filetype
                )
                db.session.add(response_answer)
                db.session.commit()
            else:
                user_answer.answer = answer
                user_answer.filetype = filetype
                db.session.commit()
    except Exception as err:  # TODO Add exception
        pass
