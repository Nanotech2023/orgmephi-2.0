from .models import *
from common.errors import NotFound, InsufficientData
from common.util import db_get_one_or_none


def get_user_in_contest_work(user_id, contest_id):
    user_work = Response.query.filter_by(**{"contest_id": contest_id,
                                            "user_id": user_id}).one_or_none()
    if user_work is None:
        raise NotFound(field='user_id , contest_id', value='{user_id} , {contest_id}'.format(user_id=user_id,
                                                                                             contest_id=contest_id))
    return user_work


def user_answer_get_file(user_id, contest_id, task_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if len(user_work.answers) == 0:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    user_answer = db_get_one_or_none(PlainAnswer, 'task_id', task_id)
    if user_answer is None:
        raise NotFound('response_answer', 'for task_id %d' % task_id)
    return user_answer


def user_answer_get(user_id, contest_id, task_id, model):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if len(user_work.answers) == 0:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    user_answer = db_get_one_or_none(model, 'task_id', task_id)
    if user_answer is None:
        raise NotFound('response_answer', 'for task_id %d' % task_id)
    return user_answer


def user_answer_post_file(answer_file, filetype, user_id, contest_id, task_id):
    try:
        user_work = get_user_in_contest_work(user_id, contest_id)
    except NotFound:
        user_work = add_user_response(db.session, user_id, contest_id)
    user_answer = user_work.answers.filter(PlainAnswer.task_id == task_id).one_or_none()
    if user_answer is None:
        add_plain_answer(user_work.work_id, task_id, filetype=filetype, file=answer_file)
    else:
        user_answer.update(answer_new=answer_file, filetype_new=filetype)
    db.session.commit()


def update_multiple_answers(answers, answer):
    answers = [MultipleUserAnswer(text=elem) for elem in answers]
    answer.answers = answers


def user_response_appeal_create(values, user_id, contest_id):
    message = values['message']
    user_work = get_user_in_contest_work(user_id, contest_id)
    user_work.status = work_status['Appeal']
    appeal = add_response_appeal(user_work.work_id)
    # TODO CREATE MESSAGE
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
