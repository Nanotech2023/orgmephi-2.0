from .models import *
from common.errors import NotFound, InsufficientData


def get_user_in_contest_work(user_id, contest_id):
    user_work = Response.query.filter_by(**{"contest_id": contest_id,
                                            "user_id": user_id}).one_or_none()
    if user_work is None:
        raise NotFound(field='user_id / contest_id', value='{user_id} / {contest_id}'.format(user_id=user_id,
                                                                                             contest_id=contest_id))
    return user_work


def user_answer_get(user_id, contest_id, task_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if user_work.answers is None:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    user_answer = user_work.answers.filter(ResponseAnswer.task_id == task_id).one_or_none()
    if user_answer is None:
        raise NotFound('response_answer', 'for task_id %d' % task_id)
    return user_answer


def user_answer_post(answer_file, filetype, user_id, contest_id, task_id):
    if answer_file is None:
        raise InsufficientData('answer', 'for user %d' % user_id)
    try:
        user_work = get_user_in_contest_work(user_id, contest_id)
    except NotFound:
        user_work = add_user_response(db.session, user_id, contest_id)
        response_status = add_response_status(user_work.work_id)
        user_work.statuses.append(response_status)
    user_answer = user_work.answers.filter(ResponseAnswer.task_id == task_id).one_or_none()
    if user_answer is None:
        response_answer = add_response_answer(user_work.work_id, task_id, answer_file, filetype)
        user_work.answers.append(response_answer)
    else:
        user_answer.update(answer_new=answer_file, filetype_new=filetype)
    db.session.commit()


def user_answer_status_get(user_id, contest_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    status = user_work.statuses[-1]
    return status


def user_answer_status_post(values, user_id, contest_id):
    if 'mark' in values:
        mark = values['mark']
    else:
        mark = None
    status = values['status'].value
    user_work = get_user_in_contest_work(user_id, contest_id)
    response_status = add_response_status(user_work.work_id, status, mark)
    user_work.statuses.append(response_status)
    db.session.commit()


def user_response_appeal_create(values, user_id, contest_id):
    message = values['message']
    user_work = get_user_in_contest_work(user_id, contest_id)
    new_status = add_response_status(user_work.work_id, 'Appeal')
    user_work.statuses.append(new_status)
    appeal = add_response_appeal(new_status.status_id, message)
    new_status.appeal = appeal
    db.session.commit()
    return appeal


def get_mimetype(filetype):
    mimetypes = {
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'git': 'image/gif',
        'txt': 'text/plain',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'odt': 'application/vnd.oasis.opendocument.text'
    }
    return mimetypes.get(filetype)
