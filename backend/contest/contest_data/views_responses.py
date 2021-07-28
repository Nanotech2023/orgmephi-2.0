import datetime

from flask import request, make_response

from contest_data.models_responses import *
from contest_data import app, db, openapi
from contest_data.errors import RequestError

work_status = {
    'NotChecked': ResponseStatusEnum.not_checked,
    'Accepted': ResponseStatusEnum.accepted,
    'Rejected': ResponseStatusEnum.rejected,
    'Appeal': ResponseStatusEnum.appeal,
    'Revision': ResponseStatusEnum.revision
}

work_status_reverse = {val: key for key, val in work_status.items()}

appeal_status = {
    'UnderReview': AppealStatusEnum.under_review,
    'AppealAccepted': AppealStatusEnum.appeal_accepted,
    'AppealRejected': AppealStatusEnum.appeal_rejected
}

appeal_status_reverse = {val: key for key, val in appeal_status.items()}

filetype_dict = {
    'txt': ResponseFiletypeEnum.txt,
    'pdf': ResponseFiletypeEnum.pdf,
    'jpg': ResponseFiletypeEnum.jpg,
    'doc': ResponseFiletypeEnum.doc,
    'docx': ResponseFiletypeEnum.docx,
    'png': ResponseFiletypeEnum.png,
    'gif': ResponseFiletypeEnum.gif,
    'odt': ResponseFiletypeEnum.odt
}

filetype_reverse = {val: key for key, val in filetype_dict.items()}


def catch_request_error(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except RequestError as err:
            return err.to_response()
    return wrapper


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/response:',
           methods=['GET'])
@openapi
@catch_request_error
def get_user_all_answers(olympiad_id, stage_id, contest_id, user_id):
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


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/answer/<int:answer_id>',
           methods=['GET'])
@openapi
@catch_request_error
def get_user_answer_by_id(olympiad_id, stage_id, contest_id, answer_id):
    # TODO Add Checking
    user_answer = ResponseAnswer.query.filter_by(anwer_id=answer_id).one()
    return make_response(
        {
            "user_answer": user_answer.answer,
            "filetype": user_answer.filetype
        }, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/task/<int:task_id>/user/self:',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_answer_for_task(olympiad_id, stage_id, contest_id, task_id):
    if request.method == 'GET':
        self_user_id = None  # TODO Get current user id
        user_work = Response.query.filter_by(user_id=self_user_id). \
            filter_by(contest_id=contest_id).one()
        user_answer = user_work.answers.filter_by(task_num=task_id).one()
        return make_response(
            {
                "user_answer": user_answer.answer,
                "filetype": filetype_reverse[user_answer.filetype]
            }, 200)
    elif request.method == 'POST':
        self_user_id = None  # TODO Get current user id
        # TODO Add Checking
        values = request.openapi.body
        answer = values['user_answer']
        filetype = values['filetype']
        user_work = Response.query.filter_by(user_id=self_user_id). \
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
                filetype=filetype_dict[filetype]
            )
            db.session.add(response_answer)
            db.session.commit()
        else:
            user_answer.answer = answer
            user_answer.filetype = filetype_dict[filetype]
            db.session.commit()
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/task/<int:task_id>/'
           'user/<int:user_id>:',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_answer_for_task_by_id(olympiad_id, stage_id, contest_id, task_id, user_id):
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
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/status',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_status_and_mark_for_response(olympiad_id, stage_id, contest_id):
    # TODO Add Checking
    if request.method == 'GET':
        self_user_id = None  # TODO Get current user id
        user_work = Response.query.filter_by(user_id=self_user_id). \
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
        self_user_id = None  # TODO Get current user id
        values = request.openapi.body
        status = values['status']
        if 'mark' in values:
            mark = values['mark']
        else:
            mark = None
        user_work = Response.query.filter_by(user_id=self_user_id). \
            filter_by(contest_id=contest_id).one()
        if mark is None:
            response_status = ResponseStatus(
                work_id=user_work.work_id,
                status=status
            )
        else:
            response_status = ResponseStatus(
                work_id=user_work.work_id,
                status=status,
                mark=mark
            )
        db.session.add(response_status)
        db.session.commit()
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/status',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_status_and_mark_for_response_by_id(olympiad_id, stage_id, contest_id, user_id):
    # TODO Add Checking
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
            response_status = ResponseStatus(
                work_id=user_work.work_id,
                status=status,
                mark=mark
            )
        db.session.add(response_status)
        db.session.commit()
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/status/history',
           methods=['GET'])
@openapi
@catch_request_error
def user_status_history_for_response(olympiad_id, stage_id, contest_id):
    # TODO Add Checking
    self_user_id = None  # TODO Get current user id
    user_work = Response.query.filter_by(user_id=self_user_id). \
        filter_by(contest_id=contest_id).one()
    status = user_work.statuses.order_by(ResponseStatus.timestamp.desc())
    history = []
    appeals = db.session.query(ResponseStatus, Appeal). \
        filter_by(ResponseStatus.status_id == Appeal.work_status).order_by(
        ResponseStatus.timestamp.desc())  # TODO fix query
    number = 0
    for elem in status:
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


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/'
           'user/<int:user_id>/status/history',
           methods=['GET'])
@openapi
@catch_request_error
def user_status_history_for_response(olympiad_id, stage_id, contest_id, user_id):
    # TODO Add Checking
    user_work = Response.query.filter_by(user_id=user_id). \
        filter_by(contest_id=contest_id).one()
    status = user_work.statuses.order_by(ResponseStatus.timestamp.desc())
    history = []
    appeals = db.session.query(ResponseStatus, Appeal). \
        filter_by(ResponseStatus.status_id == Appeal.work_status).order_by(
        ResponseStatus.timestamp.desc())  # TODO fix query
    number = 0
    for elem in status:
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


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/list/', methods=['GET'])
@openapi
@catch_request_error
def get_list_for_stage(olympiad_id, stage_id, contest_id):
    # TODO Add Checking
    users_in_contest = Response.query.filter_by(contest_id=contest_id).all()
    user_rows = []
    for elem in users_in_contest:
        first_name = None   # TODO Get additional info for users
        second_name = None
        middle_name = None
        mark = ResponseStatus.query.filter_by(work_id=elem.work_id).order_by(ResponseStatus.timestamp.desc()).one().mark
        user_rows.append(
            {
                'user_id': elem.user_id,
                'first_name': first_name,
                'second_name': second_name,
                'middle_name': middle_name,
                'mark': mark
            }
        )
    contest_name = None     # TODO get contest_name
    return make_response(
        {
            'contest_id': contest_id,
            'contest_name': contest_name,
            'userrow': user_rows
        }, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/appeal/last',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_response_appeal_info(olympiad_id, stage_id, contest_id):
    # TODO Add Checking
    if request.method == 'GET':
        self_user_id = None  # TODO Get current user id
        user_work = Response.query.filter_by(user_id=self_user_id). \
            filter_by(contest_id=contest_id).one()
        last_appeal = ResponseStatus.query.join(Appeal, ResponseStatus.status_id == Appeal.work_status). \
            filter(ResponseStatus.work_id == user_work.work_id). \
            order_by(ResponseStatus.timestamp.desc()).first()
        if last_appeal is None:
            pass  # TODO Exception no appeal
        return make_response(
            {
                'appeal_id': last_appeal.appeal_id,
                'status': last_appeal.work_status,
                'appeal_message': last_appeal.appeal_message,
                'appeal_response': last_appeal.appeal_response
            })
    elif request.method == 'POST':
        self_user_id = None  # TODO Get current user id
        values = request.openapi.body
        message = values['message']
        user_work = Response.query.filter_by(user_id=self_user_id). \
            filter_by(contest_id=contest_id).one()
        new_status = ResponseStatus(
            work_id=user_work.work_id,
            status=work_status['Appeal']
        )
        db.session.add(new_status)
        db.session.commit()
        appeal = Appeal(
            work_status=new_status.status_id,
            appeal_status=appeal_status['UnderReview'],
            appeal_message=message
        )
        db.session.add(appeal)
        db.session.commit()
        return make_response(
            {
                'appeal_id': appeal.appeal_id
            }, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/appeal/last',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_response_appeal_info_by_id(olympiad_id, stage_id, contest_id, user_id):
    # TODO Add Checking
    if request.method == 'GET':
        user_work = Response.query.filter_by(user_id=user_id). \
            filter_by(contest_id=contest_id).one()
        last_appeal = ResponseStatus.query.join(Appeal, ResponseStatus.status_id == Appeal.work_status). \
            filter(ResponseStatus.work_id == user_work.work_id). \
            order_by(ResponseStatus.timestamp.desc()).first()
        if last_appeal is None:
            pass  # TODO Exception no appeal
        return make_response(
            {
                'appeal_id': last_appeal.appeal_id,
                'status': appeal_status_reverse[last_appeal.work_status],
                'appeal_message': last_appeal.appeal_message,
                'appeal_response': last_appeal.appeal_response
            })
    elif request.method == 'POST':
        values = request.openapi.body
        message = values['message']
        user_work = Response.query.filter_by(user_id=user_id). \
            filter_by(contest_id=contest_id).one()
        new_status = ResponseStatus(
            work_id=user_work.work_id,
            status=work_status['Appeal']
        )
        db.session.add(new_status)
        db.session.commit()
        appeal = Appeal(
            work_status=new_status.status_id,
            appeal_status=appeal_status['UnderReview'],
            appeal_message=message
        )
        db.session.add(appeal)
        db.session.commit()
        return make_response(
            {
                'appeal_id': appeal.appeal_id
            }, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/appeal/<int:appeal_id>/reply',
           methods=['POST'])
@openapi
@catch_request_error
def reply_to_user_appeal(olympiad_id, stage_id, contest_id, appeal_id):
    # TODO Add Checking
    values = request.openapi.body
    message = values['message']
    accepted = values['accepted']
    if accepted:
        appeal_new_status = appeal_status['AppealAccepted']
        response_new_status = work_status['Accepted']
    else:
        appeal_new_status = appeal_status['AppealRejected']
        response_new_status = work_status['Rejected']
    appeal = Appeal.query.filter_by(appeal_id=appeal_id).first()
    appeal.response = message
    appeal.appeal_status = appeal_new_status
    db.session.commit()
    last_status = ResponseStatus.query.filter_by(status_id=appeal.work_status).one()
    if 'new_mark' in values and accepted:
        new_mark = values['new_mark']
    else:
        new_mark = last_status.mark
    new_response_status = ResponseStatus(
        work_id=last_status.work_id,
        status=response_new_status,
        mark=new_mark
    )
    db.session.add(new_response_status)
    db.session.commit()
    return make_response(
        {
            'appeal_id': appeal.appeal_id,
            'status': appeal_status_reverse[appeal.appeal_status],
            'appeal_message': appeal.appeal_message,
            'appeal_response': appeal.appeal_response
        }, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/appeal/<int:appeal_id>',
           methods=['GET'])
@openapi
@catch_request_error
def get_appeal_info_by_id(olympiad_id, stage_id, contest_id, appeal_id):
    # TODO Add Checking
    appeal = Appeal.query.filter_by(appeal_id=appeal_id).one()
    return make_response(
        {
            'appeal_id': appeal.appeal_id,
            'status': appeal_status_reverse[appeal.appeal_status],
            'appeal_message': appeal.appeal_message,
            'appeal_response': appeal.appeal_response
        }, 200)
