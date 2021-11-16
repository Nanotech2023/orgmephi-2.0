from .. import *
from ..tasks import *  # Fixtures
from datetime import datetime, timedelta


# noinspection DuplicatedCode
@pytest.fixture
def create_tasks_pool_for_responses(test_base_contests):
    from contest.tasks.models import TaskPool
    task_pools = [TaskPool(name=f'Test tasks pool {i}',
                           year=2021,
                           orig_task_points=20) for i in range(3)]
    for test_base_contest in test_base_contests:
        test_base_contest.task_pools = task_pools
    test_app.db.session.add_all(task_pools)
    test_app.db.session.commit()
    dict_ = {'base_contests': test_base_contests,
             'task_pools': task_pools}
    yield dict_


@pytest.fixture
def create_simple_contest(create_tasks_pool_for_responses):
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum, \
        ContestGroupRestrictionEnum, ContestGroupRestriction
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OnLineContest,
                     ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=create_tasks_pool_for_responses['base_contests'][i],
                                     visibility=True, start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=1),
                                     holding_type=holding_types[i % 3],
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=2),
                                     show_answer_after_contest=True,
                                     deadline_for_appeal=datetime.utcnow() + timedelta(minutes=45),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(8)]
    from user.models.auth import get_group_for_everyone
    everyone_group = get_group_for_everyone()
    for i in range(len(simple_contests)):
        base_contest = create_tasks_pool_for_responses['base_contests'][i % len(create_tasks_pool_for_responses)]
        base_contest.child_contests.extend(simple_contests)
    test_app.db.session.add_all(simple_contests)
    test_app.db.session.commit()
    group_restrictions = [ContestGroupRestriction(contest_id=simple_contests[i].contest_id, group_id=everyone_group.id,
                                                  restriction=ContestGroupRestrictionEnum.edit_user_status)
                          for i in range(len(simple_contests))]
    test_app.db.session.add_all(group_restrictions)
    test_app.db.session.commit()
    create_tasks_pool_for_responses['contests'] = simple_contests
    yield create_tasks_pool_for_responses


@pytest.fixture
def create_contest_tasks_for_responses(create_simple_contest):
    from contest.tasks.models import ContestTask
    for i in range(8):
        contest_tasks = [ContestTask(num=i,
                                     task_points=14
                                     ) for i in range(3)]
        for j in range(3):
            contest_tasks[j].task_pools = [create_simple_contest['task_pools'][j]]
        create_simple_contest['contests'][i].contest_tasks = contest_tasks
        test_app.db.session.add_all(contest_tasks)
    test_app.db.session.commit()
    yield create_simple_contest


@pytest.fixture
def create_olympiad_location(create_contest_tasks_for_responses):
    from contest.tasks.models.location import add_russia_location
    from user.models import Region, City
    region = Region(name='test')
    test_app.db.session.add(region)
    city = City(name='test')
    city.region = region
    test_app.db.session.add(city)
    location = add_russia_location(db_session=test_app.db.session, city_name='test',
                                   region_name='test', address='address')
    test_app.db.session.commit()
    create_contest_tasks_for_responses['location'] = location
    yield create_contest_tasks_for_responses


@pytest.fixture
def create_user_in_contest(create_olympiad_location, test_user_university):
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_university.id
    users_in_contests = [UserInContest(user_id=user_id,
                                       contest_id=create_olympiad_location.get('contests')[i].contest_id,
                                       show_results_to_user=False,
                                       user_status=UserStatusEnum.Participant,
                                       location_id=get_location_id(create_olympiad_location))
                         for i in range(8)]
    test_app.db.session.add_all(users_in_contests)
    test_app.db.session.commit()
    create_olympiad_location['users'] = users_in_contests
    yield create_olympiad_location


# noinspection DuplicatedCode
@pytest.fixture
def create_one_task(create_user_in_contest):
    from contest.tasks.models.tasks import PlainTask, TaskAnswerTypeEnum
    plain_tasks = [PlainTask(name='Test',
                             image_of_task=None,
                             recommended_answer='answer'
                             )
                   for _ in range(8)]

    create_user_in_contest['task_pools'][0].tasks = plain_tasks
    test_app.db.session.add_all(plain_tasks)
    test_app.db.session.commit()
    create_user_in_contest['plain_tasks'] = plain_tasks
    yield create_user_in_contest


@pytest.fixture
def create_two_tasks(create_one_task):
    from contest.tasks.models.tasks import RangeTask
    range_tasks = [RangeTask(name='Test',
                             image_of_task=None,
                             start_value=0.5,
                             end_value=0.7)
                   for _ in range(8)]
    create_one_task['task_pools'][1].tasks = range_tasks
    test_app.db.session.add_all(range_tasks)
    test_app.db.session.commit()
    create_one_task['range_tasks'] = range_tasks
    yield create_one_task


@pytest.fixture
def create_three_tasks(create_two_tasks):
    from contest.tasks.models.tasks import MultipleChoiceTask
    multiple_tasks = [MultipleChoiceTask(image_of_task=None)
                      for _ in range(8)]
    answers = [
        {
            "answer": "1",
            "is_right_answer": True
        },
        {
            "answer": "2",
            "is_right_answer": False
        },
        {
            "answer": "3",
            "is_right_answer": True
        }
    ]
    test_app.db.session.add_all(multiple_tasks)
    for i in range(8):
        multiple_tasks[i].answers = answers
    create_two_tasks['task_pools'][2].tasks = multiple_tasks
    test_app.db.session.commit()
    create_two_tasks['multiple_tasks'] = multiple_tasks
    yield create_two_tasks


@pytest.fixture
def create_user_response(create_three_tasks):
    from contest.responses.models import Response
    responses = [Response(user_id=get_user_id(create_three_tasks, i),
                          contest_id=get_contest_id(create_three_tasks, i))
                 for i in range(8)]
    test_app.db.session.add_all(responses)
    test_app.db.session.commit()
    from contest.tasks.util import try_to_generate_variant
    for i in range(8):
        try_to_generate_variant(contest_id=get_contest_id(create_three_tasks, i),
                                user_id=get_user_id(create_three_tasks, i))
    create_three_tasks['responses'] = responses
    test_app.db.session.commit()
    yield create_three_tasks


@pytest.fixture
def create_user_with_answers(create_user_response):
    from contest.responses.models import PlainAnswerText, RangeAnswer, MultipleChoiceAnswer
    plain_answers = ['answer', 'answer1', 'answer2']
    range_answers = [0.6, 0.2, 0.9]
    multiple_answers = [
        ['1', '2'],
        ['1', '3'],
        ['2', '3']
    ]
    from contest.responses.models import Response
    from contest.tasks.models import TaskTypeEnum
    for i in range(8):
        user_work_id = get_work_id(create_user_response, i)
        user_work = Response.query.filter_by(work_id=user_work_id).one_or_none()
        plain_id = get_task_id_by_variant_and_type(user_work.contest_id, user_work.user_id, TaskTypeEnum.PlainTask)
        range_id = get_task_id_by_variant_and_type(user_work.contest_id, user_work.user_id, TaskTypeEnum.RangeTask)
        multiple_id = get_task_id_by_variant_and_type(user_work.contest_id, user_work.user_id,
                                                      TaskTypeEnum.MultipleChoiceTask)
        plain_answer = PlainAnswerText(work_id=user_work_id,
                                       task_id=plain_id,
                                       answer_text=plain_answers[i % 3])
        range_answer = RangeAnswer(work_id=user_work_id,
                                   task_id=range_id,
                                   answer=range_answers[i % 3])
        multiple_answer = MultipleChoiceAnswer(work_id=user_work_id,
                                               task_id=multiple_id,
                                               answers=multiple_answers[i % 3])
        test_app.db.session.add(plain_answer)
        test_app.db.session.add(range_answer)
        test_app.db.session.add(multiple_answer)

    test_app.db.session.commit()
    yield create_user_response


def get_contest_id(array, index):
    return array['contests'][index].contest_id


def get_location_id(array):
    return array['location'].location_id


def get_variant_id(array, index):
    return array['variants'][index].variant_id


def get_user_id(array, index):
    return array['users'][index].user_id


def get_work_id(array, index):
    return array['responses'][index].work_id


def get_plain_task_id(array, index):
    return array['plain_tasks'][index].task_id


def get_range_task_id(array, index):
    return array['range_tasks'][index].task_id


def get_multiple_task_id(array, index):
    return array['multiple_tasks'][index].task_id


def get_task_id_by_variant_and_type(contest_id, user_id, task_type):
    from contest.tasks.models import UserInContest, ContestTaskInVariant, Task
    from common.util import db_get_one_or_none
    variant_id = UserInContest.query.filter_by(user_id=user_id,
                                               contest_id=contest_id).one_or_none().variant_id
    tasks = [task.base_task_id for task in ContestTaskInVariant.query.filter_by(variant_id=variant_id).all()]
    print(ContestTaskInVariant.query.all())
    print(tasks)
    for task_id in tasks:
        task = db_get_one_or_none(Task, 'task_id', task_id)
        print(task)
        print(task.task_type)
        if task.task_type == task_type:
            return task.task_id


def get_variant_by_num(contest_id, user_id):
    from contest.tasks.models import UserInContest, Variant
    from common.util import db_get_one_or_none
    variant_id = UserInContest.query.filter_by(user_id=user_id,
                                               contest_id=contest_id).one_or_none().variant_id
    variant = db_get_one_or_none(Variant, "variant_id", variant_id)
    return variant
