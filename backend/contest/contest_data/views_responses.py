import datetime

from flask import request, make_response

from contest_data.models_responses import *
from contest_data import app, db, openapi
from contest_data.errors import RequestError, NotFound

def catch_request_error(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except RequestError as err:
            return err.to_response()
    return wrapper


def get_one_or_raise(entity, field, value):
    result = get_one_or_null(entity, field, value)
    if result is None:
        raise NotFound(field, value)
    return result


def get_user_in_contest_work(user_id, contest_id):
    user_work = Response.query.filter(user_id=user_id, contest_id=contest_id).one_or_none()
    if user_work is None:
        raise NotFound(field='user_id / contest_id', value='{user_id} / {contest_id}'.format(user_id=user_id,
                                                                                            contest_id=contest_id))
    return user_work


def get_user_info(user_id):     # TODO Get additional info for users
    return {}


def get_contest_name(contest_id):           # TODO get contest_name
    return ''


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/response:',
           methods=['GET'])
@openapi
@catch_request_error
def get_user_all_answers(olympiad_id, stage_id, contest_id, user_id):
    # TODO Add Checking olympiad_id, stage_id
    user_work = get_user_in_contest_work(user_id, contest_id)
    if user_work.answers is None:
        raise NotFound('user_response.answers', 'for user %d' %user_id)
    answers = user_work.answers.all()
    user_answer = []
    for elem in answers:
        user_answer.append(elem.all_answers_to_json())
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
    # TODO Add Checking olympiad_id, stage_id
    user_answer = get_one_or_raise(ResponseAnswer, 'answer_id', answer_id)
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
        # TODO Add Checking olympiad_id, stage_id
        self_user_id = None  # TODO Get current user id
        user_work = get_user_in_contest_work(user_id, contest_id)
        if user_work.answers is None:
            raise NotFound('user_response.answers', 'for user %d' % user_id)
        user_answer = user_work.answers.filter(task_num=task_id).one_or_none()
        if user_answer is None:
            raise NotFound('response_answer', 'for task_id %d' % task_id)
        return make_response(
            {
                "user_answer": user_answer.answer,
                "filetype": filetype_reverse[user_answer.filetype]
            }, 200)
    elif request.method == 'POST':
        self_user_id = None  # TODO Get current user id
        # TODO Add Checking olympiad_id, stage_id
        values = request.openapi.body
        answer = values['user_answer']
        filetype = values['filetype']
        try:
            user_work = get_user_in_contest_work(self_user_id, contest_id)
        except NotFound as err:
            user_work = add_user_response(db.session, self_user_id, contest_id)
            response_status = add_user_response_status(db.session, user_work.work_id)
        user_answer = user_work.answers.filter(task_num=task_id).one_or_none()
        if user_answer is None:
            response_answer = add_response_answer(db.session, user_work.work_id, task_id, answer, filetype)
        else:
            user_answer.update(answer_new=answer, filetype_new=filetype)
        db.session.commit()
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/task/<int:task_id>/'
           'user/<int:user_id>:',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_answer_for_task_by_id(olympiad_id, stage_id, contest_id, task_id, user_id):
    if request.method == 'GET':
        # TODO Add Checking olympiad_id, stage_id
        self_user_id = None  # TODO Get current user id
        user_work = get_user_in_contest_work(user_id, contest_id)
        if user_work.answers is None:
            raise NotFound('user_response.answers', 'for user %d' % user_id)
        user_answer = user_work.answers.filter(task_num=task_id).one_or_none()
        if user_answer is None:
            raise NotFound('response_answer', 'for task_id %d' % task_id)
        return make_response(
            {
                "user_answer": user_answer.answer,
                "filetype": filetype_reverse[user_answer.filetype]
            }, 200)
    elif request.method == 'POST':
        # TODO Add Checking olympiad_id, stage_id
        values = request.openapi.body
        answer = values['user_answer']
        filetype = values['filetype']
        try:
            user_work = get_user_in_contest_work(user_id, contest_id)
        except NotFound as err:
            user_work = add_user_response(db.session, user_id, contest_id)
            response_status = add_user_response_status(db.session, user_work.work_id)
        user_answer = user_work.answers.filter(task_num=task_id).one_or_none()
        if user_answer is None:
            response_answer = add_response_answer(db.session, user_work.work_id, task_id, answer, filetype)
        else:
            user_answer.update(answer_new=answer, filetype_new=filetype)
        db.session.commit()
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/status',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_status_and_mark_for_response(olympiad_id, stage_id, contest_id):
    if request.method == 'GET':
        # TODO Add Checking olympiad_id, stage_id
        self_user_id = None  # TODO Get current user id
        user_work = get_user_in_contest_work(self_user_id, contest_id)
        status = user_work.statuses.order_by(ResponseStatus.timestamp.desc()).first()
        return make_response(status.status_and_mark_to_json(), 200)
    elif request.method == 'POST':
        # TODO Add Checking olympiad_id, stage_id
        self_user_id = None  # TODO Get current user id
        values = request.openapi.body
        status = values['status']
        if 'mark' in values:
            mark = values['mark']
        else:
            mark = None
        user_work = get_user_in_contest_work(self_user_id, contest_id)
        response_status = add_response_status(db.session, user_work.work_id, status, mark)
        db.session.commit()
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/status',
           methods=['GET', 'POST'])
@openapi
@catch_request_error
def user_status_and_mark_for_response_by_id(olympiad_id, stage_id, contest_id, user_id):
    if request.method == 'GET':
        # TODO Add Checking olympiad_id, stage_id
        user_work = get_user_in_contest_work(user_id, contest_id)
        status = user_work.statuses.order_by(ResponseStatus.timestamp.desc()).first()
        return make_response(status.status_and_mark_to_json(), 200)
    elif request.method == 'POST':
        # TODO Add Checking olympiad_id, stage_id
        values = request.openapi.body
        status = values['status']
        if 'mark' in values:
            mark = values['mark']
        else:
            mark = None
        user_work = get_user_in_contest_work(user_id, contest_id)
        response_status = add_response_status(db.session, user_work.work_id, status, mark)
        db.session.commit()
        return make_response({}, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/status/history',
           methods=['GET'])
@openapi
@catch_request_error
def user_status_history_for_response(olympiad_id, stage_id, contest_id):
    # TODO Add Checking olympiad_id, stage_id
    self_user_id = None  # TODO Get current user id
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    status = user_work.statuses.order_by(ResponseStatus.timestamp.desc())
    history = get_status_history(db.session, user_work.work_id, status)
    return make_response(
        {
            'user_id': self_user_id,
            'contest_id': contest_id,
            'history': history
        }, 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/'
           'user/<int:user_id>/status/history',
           methods=['GET'])
@openapi
@catch_request_error
def user_status_history_for_response(olympiad_id, stage_id, contest_id, user_id):
    # TODO Add Checking olympiad_id, stage_id
    user_work = get_user_in_contest_work(user_id, contest_id)
    status = user_work.statuses.order_by(ResponseStatus.timestamp.desc())
    history = get_status_history(db.session, user_work.work_id, status)
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
    # TODO Add Checking olympiad_id, stage_id
    user_in_contest = get_list(Response, 'contest_id', contest_id)
    user_rows = []
    for elem in users_in_contest:
        user_info = get_user_info(user_id)
        mark = ResponseStatus.query.filter(work_id=elem.work_id).order_by(ResponseStatus.timestamp.desc()).one().mark
        user_info['mark'] = mark
        user_rows.append(user_info)
    contest_name = get_contest_name(contest_id)
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
    # TODO Add Checking olympiad_id, stage_id
    if request.method == 'GET':
        self_user_id = None  # TODO Get current user id
        user_work = get_user_in_contest_work(self_user_id, contest_id)
        last_appeal = ResponseStatus.query.join(Appeal, ResponseStatus.status_id == Appeal.work_status). \
            filter(ResponseStatus.work_id == user_work.work_id). \
            order_by(ResponseStatus.timestamp.desc()).one_or_none()
        if last_appeal is None:
            raise NotFound('appeal', 'for user {}'.format(self_user_id))
        return make_response(last_appeal.info_to_json(), 200)
    elif request.method == 'POST':
        self_user_id = None  # TODO Get current user id
        values = request.openapi.body
        message = values['message']
        user_work = get_user_in_contest_work(self_user_id, contest_id)
        new_status = add_response_status(db.session, user_work.work_id, 'Appeal')
        appeal = add_response_appeal(db.session, new_status.status_id, message)
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
    # TODO Add Checking olympiad_id, stage_id
    if request.method == 'GET':
        user_work = get_user_in_contest_work(user_id, contest_id)
        last_appeal = ResponseStatus.query.join(Appeal, ResponseStatus.status_id == Appeal.work_status). \
            filter(ResponseStatus.work_id == user_work.work_id). \
            order_by(ResponseStatus.timestamp.desc()).one_or_none()
        if last_appeal is None:
            raise NotFound('appeal', 'for user {}'.format(user_id))
        return make_response(last_appeal.info_to_json(), 200)
    elif request.method == 'POST':
        values = request.openapi.body
        message = values['message']
        user_work = get_user_in_contest_work(user_id, contest_id)
        new_status = add_response_status(db.session, user_work.work_id, 'Appeal')
        appeal = add_response_appeal(db.session, new_status.status_id, message)
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
    # TODO Add Checking olympiad_id, stage_id
    values = request.openapi.body
    message = values['message']
    accepted = values['accepted']
    if accepted:
        appeal_new_status = appeal_status['AppealAccepted']
        response_new_status = 'Accepted'
    else:
        appeal_new_status = appeal_status['AppealRejected']
        response_new_status = 'Rejected'
    appeal = Appeal.query.filter(appeal_id=appeal_id).one_or_none()
    if appeal is None:
        raise NotFound('appeal', 'by id {}'.format(appeal_id))
    appeal.reply_to_appeal(message, appeal_new_status)
    db.session.commit()
    last_status = ResponseStatus.query.filter(status_id=appeal.work_status).one()
    if 'new_mark' in values and accepted:
        new_mark = values['new_mark']
    else:
        new_mark = last_status.mark
    new_response_status = add_response_status(db.session, last_status.work_id, status=response_new_status,
                                              mark=new_mark)
    return make_response(appeal.info_to_json(), 200)


@app.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/appeal/<int:appeal_id>',
           methods=['GET'])
@openapi
@catch_request_error
def get_appeal_info_by_id(olympiad_id, stage_id, contest_id, appeal_id):
    # TODO Add Checking
    appeal = Appeal.query.filter(appeal_id=appeal_id).one_or_none()
    if appeal is None:
        raise NotFound('appeal', 'by id {}'.format(appeal_id))
    return make_response(appeal.info_to_json(), 200)
