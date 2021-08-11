from flask import request, make_response
from .models import *
from contest.tasks.models import CompositeContest
from common.errors import NotFound, InsufficientData
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_or_raise, db_get_list, db_get_one_or_none
import base64

db = get_current_db()
module = get_current_module()
app = get_current_app()


def get_user_in_contest_work(user_id, contest_id):
    user_work = Response.query.filter_by(**{"contest_id": contest_id,
                                            "user_id": user_id}).one_or_none()
    if user_work is None:
        raise NotFound(field='user_id / contest_id', value='{user_id} / {contest_id}'.format(user_id=user_id,
                                                                                             contest_id=contest_id))
    return user_work


def check_olympiad_and_stage(olympiad_id, stage_id, contest_id):
    olympiad = db_get_or_raise(CompositeContest, 'contest_id', olympiad_id)
    stages = olympiad.stages
    our_stage = next((stage for stage in stages if stage.stage_id == stage_id), None)
    if our_stage is None:
        raise NotFound('olympiad.stage', 'for stage %d' % stage_id)
    contests = our_stage.contests
    our_contest = next((contest for contest in contests if contest.contest_id == contest_id), None)
    if our_contest is None:
        raise NotFound('olympiad.stage.contest', 'for contest %d' % contest_id)


def user_answer_get(user_id, contest_id, task_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if user_work.answers is None:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    user_answer = user_work.answers.filter(ResponseAnswer.task_num == task_id).one_or_none()
    if user_answer is None:
        raise NotFound('response_answer', 'for task_id %d' % task_id)
    return {
        "user_answer":str(user_answer.answer)   # TODO return a FILE
    }


def user_answer_post(answer_file, filetype, user_id, contest_id, task_id):
    if answer_file is None:
        raise InsufficientData('answer', 'for user %d' % user_id)
    try:
        user_work = get_user_in_contest_work(user_id, contest_id)
    except NotFound:
        user_work = add_user_response(db.session, user_id, contest_id)
        response_status = add_response_status(user_work.work_id)
        user_work.statuses.append(response_status)
    user_answer = user_work.answers.filter(ResponseAnswer.task_num == task_id).one_or_none()
    if user_answer is None:
        response_answer = add_response_answer(user_work.work_id, task_id, answer_file, filetype)
        user_work.answers.append(response_answer)
    else:
        user_answer.update(answer_new=answer_file, filetype_new=filetype)
    db.session.commit()


def user_answer_status_get(user_id, contest_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    status = user_work.statuses[-1]
    return status.serialize()


def user_answer_status_post(values, user_id, contest_id):
    if 'status' in values:
        status = values['status']
    else:
        raise InsufficientData('status', 'for user %d' % user_id)
    if 'mark' in values:
        mark = values['mark']
    else:
        mark = None
    user_work = get_user_in_contest_work(user_id, contest_id)
    response_status = add_response_status(user_work.work_id, status, mark)
    user_work.statuses.append(response_status)
    db.session.commit()


def user_response_appeal_create(values, user_id, contest_id):
    if 'message' in values:
        message = values['message']
    else:
        raise InsufficientData('message', 'for user %d' % user_id)
    user_work = get_user_in_contest_work(user_id, contest_id)
    new_status = add_response_status(user_work.work_id, 'Appeal')
    user_work.statuses.append(new_status)
    appeal = add_response_appeal(new_status.status_id, message)
    new_status.appeal = appeal
    db.session.commit()
    return appeal.appeal_id


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/response',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def get_user_all_answers(olympiad_id, stage_id, contest_id, user_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
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


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/answer/<int:answer_id>',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def get_user_answer_by_id(olympiad_id, stage_id, contest_id, answer_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    user_answer = db_get_or_raise(ResponseAnswer, 'answer_id', answer_id)
    return make_response(
        {
            "user_answer": user_answer.answer,  # TODO BLOB not for json
            "filetype": user_answer.filetype.value
        }, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/task/<int:task_id>/user/self',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def user_answer_for_task(olympiad_id, stage_id, contest_id, task_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    self_user_id = jwt_get_id()
    user_answer = user_answer_get(self_user_id, contest_id, task_id)
    return make_response(user_answer, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/'
              'task/<int:task_id>/user/self/<string:filetype>', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def user_answer_for_task_post(olympiad_id, stage_id, contest_id, task_id, filetype):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    self_user_id = jwt_get_id()
    answer = request.data
    user_answer_post(answer, filetype, self_user_id, contest_id, task_id)
    return make_response({}, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/task/<int:task_id>/'
              'user/<int:user_id>', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def user_answer_for_task_by_id(olympiad_id, stage_id, contest_id, task_id, user_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    user_answer = user_answer_get(user_id, contest_id, task_id)
    return make_response(user_answer, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/task/<int:task_id>/'
              'user/<int:user_id>/<string:filetype>', methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def user_answer_for_task_by_id_post(olympiad_id, stage_id, contest_id, task_id, user_id, filetype):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    answer = request.data
    user_answer_post(answer, filetype, user_id, contest_id, task_id)
    return make_response({}, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/status',
              methods=['GET', 'POST'])
@jwt_required()
def user_status_and_mark_for_response(olympiad_id, stage_id, contest_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    self_user_id = jwt_get_id()
    if request.method == 'GET':
        return make_response(user_answer_status_get(self_user_id, contest_id), 200)
    elif request.method == 'POST':
        values = request.openapi.body
        user_answer_status_post(values, self_user_id, contest_id)
        return make_response({}, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/status',
              methods=['GET', 'POST'])
@jwt_required()
def user_status_and_mark_for_response_by_id(olympiad_id, stage_id, contest_id, user_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    if request.method == 'GET':
        return make_response(user_answer_status_get(user_id, contest_id), 200)
    elif request.method == 'POST':
        values = request.openapi.body
        user_answer_status_post(values, user_id, contest_id)
        return make_response({}, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/status/history',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def user_status_history_for_response(olympiad_id, stage_id, contest_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
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


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/'
              'user/<int:user_id>/status/history',
              methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator', 'Participant'])
def user_status_history_for_response_by_id(olympiad_id, stage_id, contest_id, user_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    user_work = get_user_in_contest_work(user_id, contest_id)
    status = user_work.statuses
    history = [elem.status_for_history() for elem in status]
    return make_response(
        {
            'user_id': user_id,
            'contest_id': contest_id,
            'history': history
        }, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/list/', methods=['GET'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def get_list_for_stage(olympiad_id, stage_id, contest_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    users_in_contest = db_get_list(Response, 'contest_id', contest_id)
    user_rows = [elem.prepare_for_list() for elem in users_in_contest]
    return make_response(
        {
            'contest_id': contest_id,
            'user_row': user_rows
        }, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/self/appeal',
              methods=['POST'])
@jwt_required()
def user_response_appeal(olympiad_id, stage_id, contest_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    self_user_id = jwt_get_id()
    values = request.openapi.body
    return make_response(
        {
            'appeal_id': user_response_appeal_create(values, self_user_id, contest_id)
        }, 200)


@module.route(
    '/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/user/<int:user_id>/appeal',
    methods=['POST'])
@jwt_required()
def user_response_appeal_by_id(olympiad_id, stage_id, contest_id, user_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    values = request.openapi.body
    return make_response(
        {
            'appeal_id': user_response_appeal_create(values, user_id, contest_id)
        }, 200)


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/appeal/<int:appeal_id>/reply',
              methods=['POST'])
@jwt_required_role(['Admin', 'System', 'Creator'])
def reply_to_user_appeal(olympiad_id, stage_id, contest_id, appeal_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
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


@module.route('/olympiad/<int:olympiad_id>/stage/<int:stage_id>/contest/<int:contest_id>/appeal/<int:appeal_id>',
              methods=['GET'])
@jwt_required()
def get_appeal_info_by_id(olympiad_id, stage_id, contest_id, appeal_id):
    check_olympiad_and_stage(olympiad_id, stage_id, contest_id)
    appeal = db_get_or_raise(Appeal, 'appeal_id', appeal_id)
    return make_response(appeal.serialize(), 200)
