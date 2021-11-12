from .. import *
from ..tasks import *  # Fixtures
from datetime import datetime, timedelta


@pytest.fixture
def create_simple_contest(test_base_contests):
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum, \
        ContestGroupRestrictionEnum, ContestGroupRestriction
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OnLineContest,
                     ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests[i],
                                     visibility=True, start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=1),
                                     holding_type=holding_types[i % 3],
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=2),
                                     deadline_for_appeal=datetime.utcnow() + timedelta(minutes=45),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(8)]
    from user.models.auth import get_group_for_everyone
    everyone_group = get_group_for_everyone()
    for i in range(len(simple_contests)):
        base_contest = test_base_contests[i % len(test_base_contests)]
        base_contest.child_contests.extend(simple_contests)
    test_app.db.session.add_all(simple_contests)
    test_app.db.session.commit()
    group_restrictions = [ContestGroupRestriction(contest_id=simple_contests[i].contest_id, group_id=everyone_group.id,
                                                  restriction=ContestGroupRestrictionEnum.edit_user_status)
                          for i in range(len(simple_contests))]
    test_app.db.session.add_all(group_restrictions)
    test_app.db.session.commit()
    dict_ = {'contests': simple_contests}
    yield dict_


@pytest.fixture
def create_olympiad_location(create_simple_contest):
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
    create_simple_contest['location'] = location
    yield create_simple_contest


@pytest.fixture
def create_user_in_contest(create_variant, test_user_university):
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_university.id
    users_in_contests = [UserInContest(user_id=user_id,
                                       contest_id=create_variant.get('contests')[i].contest_id,
                                       show_results_to_user=False,
                                       user_status=UserStatusEnum.Participant,
                                       variant_id=get_variant_id(create_variant, i),
                                       location_id=get_location_id(create_variant))
                         for i in range(8)]
    test_app.db.session.add_all(users_in_contests)
    test_app.db.session.commit()
    create_variant['users'] = users_in_contests
    yield create_variant


# noinspection DuplicatedCode
@pytest.fixture
def create_plain_task(create_user_in_contest):
    from contest.tasks.models.tasks import PlainTask
    plain_tasks = [PlainTask(num_of_task=1,
                             image_of_task=None,
                             task_points=11,
                             recommended_answer='answer')
                   for i in range(8)]
    test_app.db.session.add_all(plain_tasks)
    for i in range(8):
        create_user_in_contest.get('variants')[i].tasks.append(plain_tasks[i])
    test_app.db.session.commit()
    create_user_in_contest['plain_tasks'] = plain_tasks
    yield create_user_in_contest


@pytest.fixture
def create_user_response(create_user_in_contest):
    from contest.responses.models import Response
    responses = [Response(user_id=get_user_id(create_user_in_contest, i),
                          contest_id=get_contest_id(create_user_in_contest, i))
                 for i in range(8)]
    test_app.db.session.add_all(responses)
    test_app.db.session.commit()
    create_user_in_contest['responses'] = responses
    yield create_user_in_contest


# noinspection DuplicatedCode
@pytest.fixture
def create_one_task(create_user_response):
    from contest.tasks.models.tasks import PlainTask, TaskAnswerTypeEnum
    types = [TaskAnswerTypeEnum.Text, TaskAnswerTypeEnum.File]
    plain_tasks = [PlainTask(num_of_task=1,
                             image_of_task=None,
                             task_points=11,
                             recommended_answer='answer',
                             answer_type=types[i % 2])
                   for i in range(8)]
    test_app.db.session.add_all(plain_tasks)
    for i in range(8):
        create_user_response.get('variants')[i].tasks.append(plain_tasks[i])
    test_app.db.session.commit()
    create_user_response['plain_tasks'] = plain_tasks
    yield create_user_response


@pytest.fixture
def create_two_tasks(create_one_task):
    from contest.tasks.models.tasks import RangeTask
    range_tasks = [RangeTask(num_of_task=2,
                             image_of_task=None,
                             task_points=5,
                             start_value=0.5,
                             end_value=0.7)
                   for _ in range(8)]
    test_app.db.session.add_all(range_tasks)
    for i in range(8):
        create_one_task.get('variants')[i].tasks.append(range_tasks[i])
    test_app.db.session.commit()
    create_one_task['range_tasks'] = range_tasks
    yield create_one_task


@pytest.fixture
def create_three_tasks(create_two_tasks):
    from contest.tasks.models.tasks import MultipleChoiceTask
    multiple_tasks = [MultipleChoiceTask(num_of_task=3,
                                         image_of_task=None,
                                         task_points=7)
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
    for i in range(8):
        create_two_tasks.get('variants')[i].tasks.append(multiple_tasks[i])
    test_app.db.session.commit()
    create_two_tasks['multiple_tasks'] = multiple_tasks
    yield create_two_tasks


@pytest.fixture
def create_user_with_answers(create_three_tasks):
    from contest.responses.models import PlainAnswerText, RangeAnswer, MultipleChoiceAnswer
    plain_answers = ['answer', 'answer1', 'answer2']
    range_answers = [0.6, 0.2, 0.9]
    multiple_answers = [
        ['1', '2'],
        ['1', '3'],
        ['2', '3']
    ]
    for i in range(8):
        user_work_id = get_work_id(create_three_tasks, i)
        plain_answer = PlainAnswerText(work_id=user_work_id,
                                       task_id=get_plain_task_id(create_three_tasks, i),
                                       answer_text=plain_answers[i % 3])
        range_answer = RangeAnswer(work_id=user_work_id,
                                   task_id=get_range_task_id(create_three_tasks, i),
                                   answer=range_answers[i % 3])
        multiple_answer = MultipleChoiceAnswer(work_id=user_work_id,
                                               task_id=get_multiple_task_id(create_three_tasks, i),
                                               answers=multiple_answers[i % 3])
        test_app.db.session.add(plain_answer)
        test_app.db.session.add(range_answer)
        test_app.db.session.add(multiple_answer)

    test_app.db.session.commit()
    yield create_three_tasks


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
