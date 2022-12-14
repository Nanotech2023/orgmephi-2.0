from datetime import datetime, timedelta

from common import get_current_db, get_current_app
from common.errors import NotFound, RequestError, AlreadyExists, PermissionDenied, TimeOver
from common.media_types import AnswerFile
from common.util import db_get_one_or_none, db_exists, db_get_or_raise, db_get_list
from contest.tasks.models import SimpleContest, RangeTask, MultipleChoiceTask, PlainTask, ContestHoldingTypeEnum, \
    UserInContest, ContestTask, Variant
from .model_schemas.schemas import PlainAnswerTextSchema, RangeAnswerSchema
from .models import Response, PlainAnswerText, RangeAnswer, MultipleChoiceAnswer, PlainAnswerFile, BaseAnswer, \
    answer_dict, add_user_response, add_plain_answer_file, add_plain_answer_text, add_range_answer, \
    add_multiple_answer, ResponseStatusEnum
from ..tasks.util import try_to_generate_variant

db = get_current_db()
app = get_current_app()


# Errors


class TimingError(RequestError):
    """
    Olympiad bad timing
    """

    def __init__(self, message):
        """
        Create error object
        """
        super(TimingError, self).__init__(409)
        self.message = message

    def get_msg(self) -> str:
        return self.message


class OlympiadError(RequestError):
    """
    Olympiad error
    """

    def __init__(self, message):
        """
        Create error object
        """
        super(OlympiadError, self).__init__(409)
        self.message = message

    def get_msg(self) -> str:
        return self.message


class RestrictionError(RequestError):
    """
    Restriction error
    """

    def __init__(self):
        """
        Create error object
        """
        super(RestrictionError, self).__init__(403)

    def get_msg(self) -> str:
        return "Your group is not allowed to do this"


# Dicts


models_dict = {
    'PlainAnswerText': PlainAnswerText,
    'PlainAnswerFile': PlainAnswerFile,
    'RangeAnswer': RangeAnswer,
    'MultipleChoiceAnswer': MultipleChoiceAnswer
}

funcs_dict = {
    'PlainAnswerText': add_plain_answer_text,
    'RangeAnswer': add_range_answer,
    'MultipleChoiceAnswer': add_multiple_answer
}

schemas_dict = {
    'PlainAnswerText': PlainAnswerTextSchema,
    'RangeAnswer': RangeAnswerSchema
}

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


# Getters


def get_user_in_contest_work(user_id, contest_id):
    user_work = Response.query.filter_by(**{"contest_id": contest_id,
                                            "user_id": user_id}).one_or_none()
    if user_work is None:
        raise NotFound(field='user_id , contest_id', value='{user_id} , {contest_id}'.format(user_id=user_id,
                                                                                             contest_id=contest_id))
    return user_work


def get_answer_by_task_id_and_work_id(model, task_id, work_id):
    user_answer = model.query.filter_by(**{"task_id": task_id,
                                           "work_id": work_id}).one_or_none()
    return user_answer


def user_answer_get(user_id, contest_id, task_id, answer_type=None):
    user_work = get_user_in_contest_work(user_id, contest_id)
    if len(user_work.answers.all()) == 0:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    base_answer: BaseAnswer = get_answer_by_task_id_and_work_id(BaseAnswer, task_id, user_work.work_id)
    if base_answer is None:
        raise NotFound('No answer', 'for task_id %d' % task_id)
    if answer_type is not None and base_answer.answer_type.value != answer_type:
        raise NotFound('Wrong type', 'for task_id %d' % task_id)
    user_answer = db_get_one_or_none(models_dict.get(base_answer.answer_type.value), 'answer_id', base_answer.answer_id)
    return user_answer


def get_all_user_answers(user_id, contest_id):
    user_work = get_user_in_contest_work(user_id, contest_id)
    answers = user_work.answers
    return {
        "user_id": user_work.user_id,
        "work_id": user_work.work_id,
        "contest_id": user_work.contest_id,
        "user_answers": answers
    }


def get_user_results_and_variant(user_id, contest_id):
    response = get_all_user_answers(user_id, contest_id)
    current_user = UserInContest.query.filter_by(user_id=user_id, contest_id=contest_id).one_or_none()
    variant = db_get_one_or_none(Variant, 'variant_id', current_user.variant_id)
    contest_tasks = variant.contest_tasks_in_variant[:]

    from contest.tasks.models import Task, ContestTask
    tasks_list = []
    for contest_task in contest_tasks:
        task = db_get_or_raise(Task, "task_id", contest_task.task_id)
        task_points = db_get_one_or_none(ContestTask, "contest_task_id", contest_task.contest_task_id).task_points
        tasks_list.append({
            'task_id': task.task_id,
            'task_type': task.task_type,
            'task_points': task_points
        })
    response["tasks_list"] = tasks_list
    return response


def get_mimetype(filetype):
    return mimetypes.get(filetype)


def get_variant_by_contest_and_user_id(contest_id, user_id):
    user_in_contest = UserInContest.query.filter_by(user_id=user_id,
                                                    contest_id=contest_id).one_or_none()
    if user_in_contest is None:
        raise NotFound("user_id, contest_id", f'{user_id}, {contest_id}')
    return user_in_contest.variant_id


# Checkers

def if_user_ended_his_response(user_id, contest_id):
    user_work: Response = get_user_in_contest_work(user_id, contest_id)
    if user_work.work_status == ResponseStatusEnum.in_progress or \
            user_work.work_status == ResponseStatusEnum.not_checked:
        raise OlympiadError("Olympiad is not over yet")


def check_task_type(task_id, task_type):
    task = None
    if task_type == answer_dict['PlainAnswerFile']:
        task = db_get_one_or_none(PlainTask, "task_id", task_id)
        if task is not None and task.answer_type.value != 'File':
            raise OlympiadError("Wrong answer type for Plain Task")
    elif task_type == answer_dict['PlainAnswerText']:
        task = db_get_one_or_none(PlainTask, "task_id", task_id)
        if task is not None and task.answer_type.value != 'Text':
            raise OlympiadError("Wrong answer type for Plain Task")
    elif task_type == answer_dict['RangeAnswer']:
        task = db_get_one_or_none(RangeTask, "task_id", task_id)
    elif task_type == answer_dict['MultipleChoiceAnswer']:
        task = db_get_one_or_none(MultipleChoiceTask, "task_id", task_id)
    if task is None:
        raise NotFound("response_answer", f'task_id - {task_id} for type {task_type.value}')


def check_time_publishing(contest_id):
    simple_contest: SimpleContest = db_get_one_or_none(SimpleContest, 'contest_id', contest_id)
    if datetime.utcnow() < simple_contest.result_publication_date:
        raise TimingError("The results have not yet been published")


def check_contest_time_left(contest_id):
    simple_contest: SimpleContest = db_get_one_or_none(SimpleContest, 'contest_id', contest_id)
    if simple_contest is None:
        raise NotFound(field='contest_id', value=contest_id)
    if datetime.utcnow() < simple_contest.start_date:
        raise TimingError("Olympiad haven't started yet")
    duration = simple_contest.contest_duration
    if datetime.utcnow() + duration > simple_contest.end_date:
        raise TimingError("Olympiad is over")


def check_contest_duration(user_work: Response):
    time_left = calculate_time_left(user_work, False)
    if user_work.work_status != ResponseStatusEnum.in_progress or \
            time_left + app.config['RESPONSE_EXTRA_MINUTES'] <= timedelta(seconds=0):
        finish_contest(user_work)
        raise TimingError("Olympiad is over for current user")


def is_contest_over(contest_id):
    simple_contest: SimpleContest = db_get_one_or_none(SimpleContest, 'contest_id', contest_id)
    time = simple_contest.end_date
    if simple_contest.holding_type == ContestHoldingTypeEnum.OfflineContest:
        raise OlympiadError("Olympiad is offline type")
    if datetime.utcnow() < time:
        raise TimingError("Olympiad is not over yet")


def is_all_checked(contest_id):
    from contest.responses.models import ResponseStatusEnum
    user_works_not_checked = Response.query.filter_by(contest_id=contest_id,
                                                      work_status=ResponseStatusEnum.not_checked).count()
    user_works_in_progress = Response.query.filter_by(contest_id=contest_id,
                                                      work_status=ResponseStatusEnum.in_progress).count()
    if user_works_in_progress != 0 or user_works_not_checked != 0:
        raise OlympiadError("Not all user responses checked")


def check_contest_type(contest_id):
    from contest.tasks.models.olympiad import ContestHoldingTypeEnum
    simple_contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    if simple_contest.holding_type == ContestHoldingTypeEnum.OfflineContest:
        raise OlympiadError("Olympiad is offline type")


def check_mark_for_task(mark, answer):
    if mark > answer.task_points:
        raise OlympiadError(f"Incorrect mark, max points is - {answer.task_points}")


def check_user_multiple_answers(answers, task_id):
    multiple_task: MultipleChoiceTask = db_get_one_or_none(MultipleChoiceTask, 'task_id', task_id)
    user_answers = [elem['answer'] for elem in answers]
    answers = set(elem['answer'] for elem in multiple_task.answers)
    for elem in user_answers:
        if elem not in answers:
            raise OlympiadError("Wrong answers for multiple type task")


def check_user_show_results(contest_id, user_id):
    from contest.tasks.util import get_user_in_contest_by_id_if_possible
    user_in_contest = get_user_in_contest_by_id_if_possible(contest_id, user_id)
    contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    if contest.show_result_after_finish:
        return
    if not user_in_contest.show_results_to_user:
        raise OlympiadError("Not allowed to see results")


def check_user_role(user_id):
    from user.models.auth import User, UserRoleEnum
    user: User = db_get_one_or_none(User, 'id', user_id)
    if user.role != UserRoleEnum.admin:
        raise PermissionDenied(['admin'])


def check_contest_restriction(user_id, contest_id, restriction_level):
    from contest.tasks.models.olympiad import restriction_range, ContestGroupRestriction, Contest
    from user.models.auth import User, UserRoleEnum, get_group_for_everyone
    user: User = db_get_or_raise(User, 'id', user_id)
    if user.role == UserRoleEnum.admin:
        return
    contest: Contest = db_get_or_raise(Contest, 'contest_id', contest_id)
    everyone = get_group_for_everyone()
    everyone_restriction = contest.group_restrictions.filter_by(group_id=everyone.id).first()
    if everyone_restriction is None:
        user_restrictions = [-1]
    else:
        user_restrictions = [restriction_range[everyone_restriction.restriction.value]]
    group_names = [group.name for group in user.groups]
    restrictions = contest.group_restrictions.filter(ContestGroupRestriction.group_name.in_(group_names)).all()
    user_restrictions = user_restrictions + [restriction_range[elem.restriction.value] for elem in restrictions]
    if restriction_range[restriction_level.value] > max(user_restrictions):
        raise RestrictionError()


def is_task_in_variant_by_number(task_id, variant_id):
    """
    Check if task in variant
    :param task_id: task id
    :param variant_id: id of current variant
    :return: boolean value if task in current variant
    """
    from contest.tasks.models import ContestTaskInVariant
    return ContestTaskInVariant.query.filter_by(variant_id=variant_id,
                                                task_id=task_id).one_or_none() is not None


def check_timing_for_mark_editing_and_appeal(contest_id, user_role):
    from user.models import UserRoleEnum
    contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    if user_role == UserRoleEnum.admin.value:
        return
    if datetime.utcnow() > contest.deadline_for_appeal:
        raise TimingError("The time for correcting the mark is out")


# Other funcs


def create_user_response(contest_id, user_id):
    try_to_generate_variant(contest_id, user_id)

    check_contest_time_left(contest_id)
    if not db_exists(db.session, UserInContest, filters={"contest_id": contest_id, "user_id": user_id}):
        raise NotFound(field='user_id , contest_id', value='{user_id} , {contest_id}'.format(user_id=user_id,
                                                                                             contest_id=contest_id))
    if not db_exists(db.session, Response, filters={"contest_id": contest_id, "user_id": user_id}):
        add_user_response(db.session, user_id, contest_id)
    else:
        raise AlreadyExists(field='user_id ,contest_id', value='{user_id} ,{contest_id}'.format(user_id=user_id,
                                                                                                contest_id=contest_id))
    db.session.commit()


def finish_contest(user_work: Response):
    user_work.work_status = ResponseStatusEnum.not_checked
    user_in_contest: UserInContest = UserInContest.query.filter_by(contest_id=user_work.contest_id,
                                                                   user_id=user_work.user_id).one_or_none()
    user_in_contest.completed_the_contest = True
    contest: SimpleContest = db_get_one_or_none(SimpleContest, 'contest_id', user_work.contest_id)
    if contest.show_result_after_finish:
        check_user_work(user_work)
    db.session.commit()


# noinspection DuplicatedCode
def user_answer_post_file(user_id, contest_id, task_id):
    if not is_task_in_variant_by_number(task_id, get_variant_by_contest_and_user_id(contest_id, user_id)):
        raise NotFound('contest_id, task_id', f'{contest_id}, {task_id}')
    user_work: Response = get_user_in_contest_work(user_id, contest_id)
    user_work.finish_time = datetime.utcnow()
    check_contest_duration(user_work)
    user_work.finish_time = datetime.utcnow()
    user_answer = user_work.answers.filter(PlainAnswerFile.task_id == task_id).one_or_none()
    if user_answer is None:
        user_answer = add_plain_answer_file(user_work.work_id, task_id)
    app.store_media('RESPONSE', user_answer, 'answer_content', AnswerFile)
    db.session.commit()


# noinspection DuplicatedCode
def user_answer_post(user_id, contest_id, task_id, values, answer_type):
    if not is_task_in_variant_by_number(task_id, get_variant_by_contest_and_user_id(contest_id, user_id)):
        raise NotFound('contest_id, task_id', f'{contest_id}, {task_id}')
    user_work: Response = get_user_in_contest_work(user_id, contest_id)
    user_work.finish_time = datetime.utcnow()
    check_contest_duration(user_work)
    user_work.finish_time = datetime.utcnow()
    user_answer = get_answer_by_task_id_and_work_id(models_dict.get(answer_type), task_id, user_work.work_id)
    if user_answer is None:
        funcs_dict.get(answer_type)(user_work.work_id, task_id, values)
    else:
        if answer_type != 'MultipleChoiceAnswer':
            schemas_dict.get(answer_type)(load_instance=True).load(values, session=db.session, instance=user_answer)
        else:
            update_multiple_answers(values['answers'], user_answer)
    db.session.commit()


def update_multiple_answers(answers, answer):
    answer.answers = [elem['answer'] for elem in answers]


def calculate_time_left(user_work: Response, only_positive_time=True):
    contest: SimpleContest = db_get_one_or_none(SimpleContest, "contest_id", user_work.contest_id)
    contest_duration = contest.contest_duration
    if user_work.work_status != ResponseStatusEnum.in_progress:
        return timedelta(seconds=0)
    time_spent = datetime.utcnow() - user_work.start_time
    if contest_duration == timedelta(seconds=0):
        time_left = contest.end_date - datetime.utcnow() + user_work.time_extension
    else:
        time_left = contest_duration + user_work.time_extension - time_spent
    if time_left < timedelta(seconds=0) and only_positive_time:
        time_left = timedelta(seconds=0)
        finish_contest(user_work)
        raise TimeOver("Time left")
    return time_left


def range_answer_check(answer: BaseAnswer):
    range_answer: RangeAnswer = db_get_one_or_none(RangeAnswer, 'answer_id', answer.answer_id)
    range_task: RangeTask = db_get_one_or_none(RangeTask, 'task_id', answer.task_id)
    if range_task.start_value <= range_answer.answer <= range_task.end_value:
        range_answer.mark = range_answer.task_points
    else:
        range_answer.mark = 0


def multiple_answer_check(answer: BaseAnswer):
    multiple_answer: MultipleChoiceAnswer = db_get_one_or_none(MultipleChoiceAnswer, 'answer_id', answer.answer_id)
    multiple_task: MultipleChoiceTask = db_get_one_or_none(MultipleChoiceTask, 'task_id', answer.task_id)
    user_answers = set(multiple_answer.answers)
    answers = multiple_task.answers
    right_answers = [elem['answer'] for elem in answers if elem['is_right_answer']]
    count = 0
    for elem in user_answers:
        if elem in right_answers:
            count += 1
        else:
            count -= 1
    if count == len(right_answers):
        multiple_answer.mark = multiple_answer.task_points
    else:
        multiple_answer.mark = 0


def check_user_work(user_work: Response):
    plain_count = 0
    for answer in user_work.answers:
        if answer.answer_type == answer_dict['RangeAnswer']:
            range_answer_check(answer)
        elif answer.answer_type == answer_dict['MultipleChoiceAnswer']:
            multiple_answer_check(answer)
        elif answer.answer_type == answer_dict['PlainAnswerText'] or \
                answer.answer_type == answer_dict['PlainAnswerFile']:
            plain_count += 1
    if plain_count == 0:
        user_work.work_status = ResponseStatusEnum.accepted
    db.session.commit()


def choose_status(percent, base_contest):
    from contest.tasks.models.olympiad import UserStatusEnum
    if percent >= base_contest.winner_1_condition:
        return UserStatusEnum.Winner_1
    elif percent >= base_contest.winner_2_condition:
        return UserStatusEnum.Winner_2
    elif percent >= base_contest.winner_3_condition:
        return UserStatusEnum.Winner_3
    elif percent >= base_contest.diploma_1_condition:
        return UserStatusEnum.Diploma_1
    elif percent >= base_contest.diploma_2_condition:
        return UserStatusEnum.Diploma_2
    elif percent >= base_contest.diploma_3_condition:
        return UserStatusEnum.Diploma_3
    else:
        return UserStatusEnum.Participant


def set_user_statuses(contest_id):
    from contest.tasks.models.tasks import Variant
    user_responses = db_get_list(Response, 'contest_id', contest_id)
    contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    base_contest = contest.base_contest
    for user_work in user_responses:
        user_in_contest: UserInContest = UserInContest.query.filter_by(contest_id=contest_id,
                                                                       user_id=user_work.user_id).one_or_none()
        variant: Variant = db_get_or_raise(Variant, 'variant_id', user_in_contest.variant_id)
        all_points = 0
        for contest_task_in_variant in variant.contest_tasks_in_variant:
            contest_task: ContestTask = db_get_or_raise(ContestTask,
                                                        'contest_task_id',
                                                        contest_task_in_variant.contest_task_id)
            all_points += contest_task.task_points
        percent = user_work.mark / all_points
        user_in_contest.user_status = choose_status(percent, base_contest)
    db.session.commit()


def get_all_user_responses(user_id):
    results = db_get_list(UserInContest, 'user_id', user_id)
    res = []
    for user_card in results:
        dict_ = {}
        try:
            user_work: Response = get_user_in_contest_work(user_card.user_id, user_card.contest_id)
            dict_['mark'] = user_work.mark
            dict_['status'] = user_work.status
        except NotFound:
            dict_['mark'] = 0
            dict_['status'] = ResponseStatusEnum.in_progress
        dict_['user_status'] = user_card.user_status
        contest = db_get_one_or_none(SimpleContest, 'contest_id', user_card.contest_id)
        dict_['contest_info'] = contest
        res.append(dict_)
    return {
        'results': res
    }
