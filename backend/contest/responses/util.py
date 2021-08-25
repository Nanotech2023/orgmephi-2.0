import bdb

from .models import *
import datetime
from common.errors import NotFound
from common.util import db_get_one_or_none
from contest.tasks.models import SimpleContest

five_minutes = datetime.timedelta(minutes=5)


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


def finish_contest(user_work: Response):
    user_work.status = work_status['NotChecked']
    db.session.commit()


def user_answer_post_file(answer_file, filetype, user_id, contest_id, task_id):
    try:
        user_work: Response = get_user_in_contest_work(user_id, contest_id)
        user_work.finish_time = datetime.utcnow()
    except NotFound:
        user_work = add_user_response(db.session, user_id, contest_id)
    flag, message = check_contest_duration(user_work)
    if flag:
        finish_contest(user_work)
        return message
    user_answer = user_work.answers.filter(PlainAnswer.task_id == task_id).one_or_none()
    if user_answer is None:
        add_plain_answer(user_work.work_id, task_id, filetype=filetype, file=answer_file)
    else:
        user_answer.update(answer_new=answer_file, filetype_new=filetype)
    db.session.commit()
    return message


def update_multiple_answers(answers, answer):
    answers = [MultipleUserAnswer(text=elem) for elem in answers]
    answer.answers = answers


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

    # TODO CHECK
def check_contest_duration(user_work: Response):
    contest_duration = db_get_one_or_none(SimpleContest, "contest_id", user_work.contest_id).contest_duration
    time_spent = datetime.utcnow() - user_work.start_time
    if user_work.status == work_status['NotChecked']:
        return 1, "Already finished"
    if time_spent + five_minutes > contest_duration:
        return 1, "No time left"
    return 0, "OK"
