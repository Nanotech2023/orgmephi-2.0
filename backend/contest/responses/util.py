from messages.models import Thread, ThreadStatus
from .creator.views import db
from .model_schemas.schemas import PlainAnswerTextSchema, RangeAnswerSchema
from datetime import datetime, timedelta
from common.errors import NotFound, RequestError
from common.util import db_get_one_or_none
from contest.tasks.models import SimpleContest, RangeTask, MultipleChoiceTask, PlainTask, ContestHoldingTypeEnum, \
    UserInContest
from .models import Response, PlainAnswerText, RangeAnswer, MultipleChoiceAnswer, PlainAnswerFile, BaseAnswer, \
    answer_dict, work_status, add_user_response, add_plain_answer_file, add_plain_answer_text, add_range_answer, \
    add_multiple_answer
from ..tasks.util import validate_file_size

five_minutes = timedelta(minutes=5)


class OlympiadError(RequestError):
    """
    Olympiad bad timing
    """
    def __init__(self, message):
        """
        Create error object
        """
        super(OlympiadError, self).__init__(409)
        self.message = message

    def get_msg(self) -> str:
        return self.message


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
    user_answer = db_get_one_or_none(PlainAnswerFile, 'task_id', task_id)
    if user_answer is None:
        raise NotFound('plain_task_file', 'for task_id %d' % task_id)
    return user_answer


models_dict = {
    'PlainAnswerText': PlainAnswerText,
    'RangeAnswer': RangeAnswer,
    'MultipleChoiceAnswer': MultipleChoiceAnswer
}


def user_answer_get(user_id, contest_id, task_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if len(user_work.answers) == 0:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    base_answer: BaseAnswer = db_get_one_or_none(BaseAnswer, 'task_id', task_id)
    if base_answer is None:
        raise NotFound('answer', 'for task_id %d' % task_id)
    user_answer = db_get_one_or_none(models_dict.get(base_answer.answer_type), 'task_id', task_id)
    return user_answer


def check_task_type(task_id, task_type):
    task = None
    if task_type == answer_dict['Plain']:
        task = db_get_one_or_none(PlainTask, "task_id", task_id)
    elif task_type == answer_dict['RangeAnswer']:
        task = db_get_one_or_none(RangeTask, "task_id", task_id)
    elif task_type == answer_dict['MultipleChoiceAnswer']:
        task = db_get_one_or_none(MultipleChoiceTask, "task_id", task_id)
    if task is None:
        raise NotFound("response_answer", f'task_id - {task_id} for type {task_type.value}')


def finish_contest(user_work: Response):
    user_work.status = work_status['NotChecked']
    user_in_contest: UserInContest = UserInContest.query.filter_by(**{"contest_id": user_work.contest_id,
                                                                      "user_id": user_work.user_id}).one_or_none()
    user_in_contest.completed_the_contest = True
    db.session.commit()


def check_contest_time_left(contest_id):
    simple_contest: SimpleContest = db_get_one_or_none(SimpleContest, 'contest_id', contest_id)
    if datetime.utcnow() + simple_contest.contest_duration > simple_contest.end_date:
        raise OlympiadError("Olympiad is over")


def user_answer_post_file(answer_file, filetype, user_id, contest_id, task_id):
    try:
        user_work: Response = get_user_in_contest_work(user_id, contest_id)
        user_work.finish_time = datetime.utcnow()
    except NotFound:
        check_contest_time_left(contest_id)
        user_work = add_user_response(db.session, user_id, contest_id)
    check_contest_duration(user_work)
    user_work.finish_time = datetime.utcnow()
    validate_file_size(answer_file)
    user_answer = user_work.answers.filter(PlainAnswerFile.task_id == task_id).one_or_none()
    if user_answer is None:
        add_plain_answer_file(user_work.work_id, task_id, filetype=filetype, file=answer_file)
    else:
        user_answer.update(answer_new=answer_file, filetype_new=filetype)
    db.session.commit()


funcs_dict = {
    'PlainAnswerText': add_plain_answer_text,
    'RangeAnswer': add_range_answer,
    'MultipleChoiceAnswer': add_multiple_answer
}

schemas_dict = {
    'PlainAnswerText': PlainAnswerTextSchema,
    'RangeAnswer': RangeAnswerSchema
}


def user_answer_post(user_id, contest_id, task_id, values, answer_type):
    try:
        user_work: Response = get_user_in_contest_work(user_id, contest_id)
        user_work.finish_time = datetime.utcnow()
    except NotFound:
        check_contest_time_left(contest_id)
        user_work = add_user_response(db.session, user_id, contest_id)
    check_contest_duration(user_work)
    user_work.finish_time = datetime.utcnow()
    answer = db_get_one_or_none(models_dict.get(answer_type), 'task_id', task_id)
    if answer is None:
        funcs_dict.get(answer_type)(user_work.work_id, task_id, values)
    else:
        if answer_type != 'MultipleChoiceAnswer':
            schemas_dict.get(answer_type)(load_instance=True).load(values, session=db.session, instance=answer)
        else:
            update_multiple_answers(values['answers'], answer)
    db.session.commit()


def update_multiple_answers(answers, answer):
    answer.answers = [elem['answer'] for elem in answers]


def get_all_user_answers(user_id, contest_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if user_work.answers is None:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    answers = user_work.answers
    return {
        "user_id": user_work.user_id,
        "work_id": user_work.work_id,
        "contest_id": user_work.contest_id,
        "user_answers": answers
    }


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
    if user_work.status == work_status['NotChecked'] or time_spent + five_minutes > contest_duration:
        finish_contest(user_work)
        raise OlympiadError("Olympiad is over for current user")


def calculate_time_left(user_work: Response):
    contest_duration = db_get_one_or_none(SimpleContest, "contest_id", user_work.contest_id).contest_duration
    time_spent = datetime.utcnow() - user_work.start_time
    return contest_duration + user_work.time_extension - time_spent


def range_answer_check(answer: BaseAnswer):
    range_answer: RangeAnswer = db_get_one_or_none(RangeAnswer, 'answer_id', answer.answer_id)
    range_task: RangeTask = db_get_one_or_none(RangeTask, 'task_id', answer.task_id)
    if range_task.start_value <= range_answer.answer <= range_task.end_value:
        range_answer.mark = range_task.task_points  # TODO CHECK
    else:
        range_answer.mark = 0


def multiple_answer_check(answer: BaseAnswer):
    multiple_answer: MultipleChoiceAnswer = db_get_one_or_none(MultipleChoiceAnswer, 'answer_id', answer.answer_id)
    multiple_task: MultipleChoiceTask = db_get_one_or_none(MultipleChoiceTask, 'task_id', answer.task_id)
    user_answers = multiple_answer.answers
    answers = multiple_task.answers
    right_answers = [elem['answer'] for elem in answers if elem['is_right_answer']]
    count = 0
    for elem in user_answers:
        if elem.text in right_answers:
            count += 1
        else:
            count -= 1
    if count == len(right_answers):
        multiple_answer.mark = multiple_task.task_points
    else:
        multiple_answer.mark = 0


def check_user_work(user_work: Response):
    for answer in user_work.answers:
        if answer.answer_type == answer_dict['RangeAnswer']:
            range_answer_check(answer)
        elif answer.answer_type == answer_dict['MultipleChoiceAnswer']:
            multiple_answer_check(answer)
    user_work.status = work_status['Accepted']
    db.session.commit()


def is_contest_over(contest_id):
    simple_contest: SimpleContest = db_get_one_or_none(SimpleContest, 'contest_id', contest_id)
    time = simple_contest.end_date
    if simple_contest.holding_type == ContestHoldingTypeEnum.OfflineContest:
        raise OlympiadError("Olympiad is offline type")
    if datetime.utcnow() < time:
        raise OlympiadError("Olympiad is not over yet")
