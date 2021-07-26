import datetime

from flask import request, make_response

from contest_data.models_responses import *
from contest_data import app, db, openapi

work_status = {
    'NotChecked': ResponseStatusEnum.not_checked,
    'Accepted': ResponseStatusEnum.accepted,
    'Rejected': ResponseStatusEnum.rejected,
    'Appeal': ResponseStatusEnum.appeal,
    'Revision': ResponseStatusEnum.revision
}

work_status_reverse = {val: key for key, val in work_status.items()}


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
    try:  # TODO Add Checking
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            pass
    except Exception as err:  # TODO Add exception
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
            if user_work is None:
                user_work = Response(
                    user_id=user_id,
                    contest_id=contest_id
                )
                db.session.add(user_work)
                db.session.commit()
                response_status = ResponseStatus(
                    work_id=user_work.work_id,
                    status=work_status['NotChecked']
                )
                db.session.add(response_status)
                db.session.commit()
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


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/user/self/status',
           methods=['GET', 'POST'])
@openapi
def user_status_and_mark_for_response(olympiad_id, stage_id, contest_id):
    try:  # TODO Add Checking
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            pass
    except Exception as err:  # TODO Add exception
        pass


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/user/{user_id}/status',
           methods=['GET', 'POST'])
@openapi
def user_status_and_mark_for_response_by_id(olympiad_id, stage_id, contest_id, user_id):
    try:  # TODO Add Checking
        if request.method == 'GET':
            user_work = Response.query.filter_by(user_id=user_id). \
                filter_by(contest_id=contest_id).one()
            status = user_work.statuses.order_by(ResponseStatus.timestamp.desc()).first()
            if status.mark is None:
                return make_response(
                    {
                        "status": work_status_reverse[status.status]
                    }, 200)
            else:
                return make_response(
                    {
                        "status": work_status_reverse[status.status],
                        "mark": status.mark
                    }
                )
        elif request.method == 'POST':
            values = request.openapi.body
            status = values['status']
            if 'mark' in values:
                mark = values['mark']
            else:
                mark = None
            user_work = Response.query.filter_by(user_id=user_id). \
                filter_by(contest_id=contest_id).one()
            if mark is None:
                response_status = ResponseStatus(
                    work_id=user_work.work_id,
                    status=status
                )
            else:
                response_status= ResponseStatus(
                    work_id=user_work.work_id,
                    status=status,
                    mark=mark
                )
            db.session.add(response_status)
            db.session.commit()
    except Exception as err:  # TODO Add exception
        pass


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/user/self/status/history', methods=['GET'])
@openapi
def user_status_history_for_response(olympiad_id, stage_id, contest_id):
    try:  # TODO Add Checking
        pass
    except Exception as err:  # TODO Add exception
        pass


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/user/{user_id}/status/history', methods=['GET'])
@openapi
def user_status_history_for_response(olympiad_id, stage_id, contest_id, user_id):
    try:    # TODO Add Checking
        user_work = Response.query.filter_by(user_id=user_id). \
            filter_by(contest_id=contest_id).one()
        status = user_work.statuses.order_by(ResponseStatus.timestamp.desc())
        history = []
        appeals = db.session.query(ResponseStatus, Appeal). \
            filter(ResponseStatus.status_id == Appeal.work_status).order_by(ResponseStatus.timestamp.desc()) # TODO fix query
        number = 0
        for elem in status:     # TODO Add mark to api spec
            if appeals[number].work_status == elem.status_id:
                appeal = appeals.appeal_id
                number += 1
            else:
                appeal = None
            history.append(
                {
                    'status:': work_status_reverse[elem.status],
                    'datetime': elem.timestamp,
                    'appeal_id': appeal,
                    'mark': elem.mark
                }
            )
        return make_response(
            {
                'user_id': user_id,
                'contest_id': contest_id,
                'history': history
            }, 200)
    except Exception as err:    # TODO Add exception
        pass


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/list/', methods=['GET'])
@openapi
def get_list_for_stage(olympiad_id, stage_id, contest_id):
    try:     # TODO Add Checking
        pass
    except Exception as err:
        pass    # TODO Add exception


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/user/self/appeal/last',
           methods=['GET', 'POST'])
@openapi
def user_response_appeal_info(olympiad_id, stage_id, contest_id):
    try:    # TODO Add Checking
        if request.method == 'GET':
            pass
        elif request.method == 'POST':
            pass
    except Exception as err:
        pass    # TODO Add exception


@app.route('/olympiad/{olympiad_id}/stage/{stage_id}/contest/{contest_id}/user/{user_id}/appeal/last',
           methods=['GET', 'POST'])
@openapi
def user_response_appeal_info_by_id(olympiad_id, stage_id, contest_id, user_id):  # TODO change to commonAppealInfo
    try:    # TODO Add Checking
        if request.method == 'GET':
            user_work = Response.query.filter_by(user_id=user_id). \
                filter_by(contest_id=contest_id).one()
            last_appeal = ResponseStatus.query.join(Appeal, ResponseStatus.status_id == Appeal.work_status). \
                filter(ResponseStatus.work_id == user_work.work_id). \
                order_by(ResponseStatus.timestamp.desc()).first()
            if last_appeal is None:
                pass # TODO Exception no appeal
            return make_response(
                {
                    'appeal_id': last_appeal.appeal_id,
                    'status': last_appeal.work_status,
                    'appeal_message': last_appeal.appeal_message,
                    'appeal_response': last_appeal.appeal_response
                })
        elif request.method == 'POST':
            pass
    except Exception as err:
        pass    # TODO Add exception



