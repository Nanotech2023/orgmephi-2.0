from .. import *
from datetime import datetime, timedelta


@pytest.fixture
def create_target_class():
    from contest.tasks.models.reference import TargetClass
    target_class = TargetClass(target_class='student')
    test_app.db.session.add(target_class)
    test_app.db.session.commit()
    yield [target_class]


@pytest.fixture
def create_olympiad_type(create_target_class):
    from contest.tasks.models.olympiad import add_olympiad_type
    olympiad_type = add_olympiad_type("string")
    test_app.db.session.add(olympiad_type)
    test_app.db.session.commit()
    create_target_class.append(olympiad_type)
    yield create_target_class


@pytest.fixture
def create_base_contest(create_olympiad_type):
    from contest.tasks.models.olympiad import add_base_contest, OlympiadSubjectEnum
    base_contest = add_base_contest(db_session=test_app.db.session,
                                    name='name',
                                    winner_1_condition=0.95,
                                    winner_2_condition=0.9,
                                    winner_3_condition=0.85,
                                    diploma_1_condition=0.8,
                                    diploma_2_condition=0.75,
                                    diploma_3_condition=0.7,
                                    olympiad_type_id=create_olympiad_type[1].olympiad_type_id,
                                    subject=OlympiadSubjectEnum.Physics,
                                    rules='rules',
                                    certificate_template='template',
                                    description='description')
    base_contest.target_classes.append(create_olympiad_type[0])
    test_app.db.session.commit()
    yield base_contest


@pytest.fixture
def create_simple_contest(create_base_contest):
    from contest.tasks.models.olympiad import add_simple_contest, ContestHoldingTypeEnum
    simple_contest = add_simple_contest(db_session=test_app.db.session, visibility=True,
                                        start_date=datetime.utcnow(),
                                        end_date=datetime.utcnow() + timedelta(hours=1),
                                        result_publication_date=datetime.utcnow() + timedelta(
                                            hours=2),
                                        holding_type=ContestHoldingTypeEnum.OnLineContest,
                                        contest_duration=timedelta(minutes=30),
                                        base_contest_id=create_base_contest.base_contest_id)
    test_app.db.session.commit()
    yield [simple_contest]


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
    create_simple_contest.append(location)
    yield create_simple_contest


@pytest.fixture
def create_variant(create_olympiad_location):
    from contest.tasks.models.contest import add_variant
    variant = add_variant(db_session=test_app.db.session, variant_number=1,
                          variant_description='description', contest_id=create_olympiad_location[0].contest_id)
    test_app.db.session.commit()
    create_olympiad_location.append(variant)
    yield create_olympiad_location


@pytest.fixture
def create_user_in_contest(create_variant, test_user_university):
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_university.id
    contest_id = get_contest_id(create_variant)
    location_id = get_location_id(create_variant)
    variant_id = get_variant_id(create_variant)
    user = UserInContest(user_id=user_id, contest_id=contest_id, show_results_to_user=False,
                         user_status=UserStatusEnum.Participant, variant_id=variant_id,
                         location_id=location_id)
    test_app.db.session.add(user)
    test_app.db.session.commit()
    create_variant.append(user_id)
    yield create_variant


@pytest.fixture
def create_plain_task(create_user_in_contest):
    from contest.tasks.models.tasks import add_plain_task
    plain_task = add_plain_task(db_session=test_app.db.session, num_of_task=1, recommended_answer='answer',
                                task_points=11)
    create_user_in_contest[2].tasks.append(plain_task)
    test_app.db.session.commit()
    create_user_in_contest.append(plain_task)
    yield create_user_in_contest


@pytest.fixture
def create_user_response(create_user_in_contest):
    from contest.responses.models import add_user_response
    response = add_user_response(test_app.db.session, user_id=get_user_id(create_user_in_contest),
                                 contest_id=get_contest_id(create_user_in_contest))
    test_app.db.session.commit()
    create_user_in_contest.append(response)
    yield create_user_in_contest


@pytest.fixture
def create_one_task(create_user_response):
    from contest.tasks.models.tasks import add_plain_task
    plain_task = add_plain_task(db_session=test_app.db.session, num_of_task=1, recommended_answer='answer',
                                task_points=11)
    create_user_response[2].tasks.append(plain_task)
    test_app.db.session.commit()
    create_user_response.append(plain_task)
    yield create_user_response


@pytest.fixture
def create_two_tasks(create_one_task):
    from contest.tasks.models.tasks import add_range_task
    range_task = add_range_task(db_session=test_app.db.session, num_of_task=2, start_value=0.5,
                                end_value=0.7, task_points=5)
    create_one_task[2].tasks.append(range_task)
    test_app.db.session.commit()
    create_one_task.append(range_task)
    yield create_one_task


@pytest.fixture
def create_three_tasks(create_two_tasks):
    from contest.tasks.models.tasks import add_multiple_task
    multiple_task = add_multiple_task(db_session=test_app.db.session, num_of_task=3, task_points=7)
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
    multiple_task.answers = answers
    create_two_tasks[2].tasks.append(multiple_task)
    test_app.db.session.commit()
    create_two_tasks.append(multiple_task)
    yield create_two_tasks


def get_contest_id(array):
    return array[0].contest_id


def get_location_id(array):
    return array[1].location_id


def get_variant_id(array):
    return array[2].variant_id


def get_user_id(array):
    return array[3]


def get_work_id(array):
    return array[4].work_id


def get_plain_task_id(array):
    return array[5].task_id


def get_range_task_id(array):
    return array[6].task_id


def get_multiple_task_id(array):
    return array[7].task_id
