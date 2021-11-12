import io
from datetime import datetime, timedelta

from ..user import *


@pytest.fixture
def create_group_for_everyone():
    from user.models.auth import Group
    everyone_group = Group(name='Everyone')
    test_app.db.session.add(everyone_group)
    test_app.db.session.commit()
    yield everyone_group


@pytest.fixture
def test_target_class():
    from contest.tasks.models.reference import TargetClass
    target_classes = [TargetClass(target_class='8'),
                      TargetClass(target_class='9'),
                      TargetClass(target_class='10'),
                      TargetClass(target_class='11'),
                      TargetClass(target_class='student')]
    test_app.db.session.add_all(target_classes)
    test_app.db.session.commit()
    yield target_classes


@pytest.fixture
def test_olympiad_types(create_group_for_everyone):
    from contest.tasks.models import OlympiadType
    olympiad_types = [OlympiadType(olympiad_type=f'Test {i}') for i in range(8)]
    test_app.db.session.add_all(olympiad_types)
    test_app.db.session.commit()
    yield olympiad_types


@pytest.fixture
def test_olympiad_locations(test_city, test_country_native):
    from contest.tasks.models import OnlineOlympiadLocation, RussiaOlympiadLocation, \
        OtherOlympiadLocation
    online_olympiad_location = [
        OnlineOlympiadLocation(url=f'Test {i}') for i in range(2)
    ]
    russia_olympiad_location = [
        RussiaOlympiadLocation(city_name=f'{test_city.name}',
                               region_name=f'{test_city.region_name}',
                               address=f'Test {i}') for i in range(2)
    ]
    other_olympiad_location = [
        OtherOlympiadLocation(country_name=f'{test_country_native.name}',
                              location=f'Test {i}') for i in range(2)
    ]
    test_app.db.session.add_all(online_olympiad_location + russia_olympiad_location + other_olympiad_location)
    test_app.db.session.commit()
    yield online_olympiad_location + russia_olympiad_location + other_olympiad_location


@pytest.fixture
def test_base_contests(test_olympiad_types, test_certificate_type):
    from contest.tasks.models import BaseContest, OlympiadSubjectEnum, OlympiadLevelEnum
    contests = [BaseContest(name=f'Test {i}', rules=f'Test{i}', description=f'Test {i}',
                            subject=OlympiadSubjectEnum.Math,
                            level=OlympiadLevelEnum.Level1,
                            winner_1_condition=0.95,
                            winner_2_condition=0.9,
                            winner_3_condition=0.8,
                            diploma_1_condition=0.7,
                            diploma_2_condition=0.6,
                            diploma_3_condition=0.5,
                            certificate_type_id=test_certificate_type.certificate_type_id) for i in range(8)]
    for i in range(len(contests)):
        olympiad_type = test_olympiad_types[i % len(test_olympiad_types)]
        olympiad_type.contests.extend(contests)
    test_app.db.session.add_all(contests)
    test_app.db.session.commit()
    yield contests


@pytest.fixture
def test_create_tasks_pool(test_base_contests):
    from contest.tasks.models import TaskPool
    task_pools = [TaskPool(name=f'Test tasks pool {i}',
                           year=2021,
                           orig_task_points=20) for i in range(3)]
    for test_base_contest in test_base_contests:
        test_base_contest.task_pools = task_pools
    test_app.db.session.add_all(task_pools)
    test_app.db.session.commit()
    yield task_pools


@pytest.fixture
def test_create_contest_tasks(test_simple_contest, test_create_tasks_pool):
    from contest.tasks.models import ContestTask
    contest_tasks = [ContestTask(num=i,
                                 task_points=14,
                                 task_pool_ids=[test_create_tasks_pool[i].task_pool_id]
                                 ) for i in range(3)]
    test_simple_contest.contest_tasks = contest_tasks

    test_app.db.session.add_all(contest_tasks)
    test_app.db.session.commit()
    yield contest_tasks


@pytest.fixture
def test_base_contests_with_target(test_base_contests, test_target_class):
    for contest in test_base_contests:
        contest.target_classes.append(test_target_class[0])
        if contest.base_contest_id != 2:
            contest.target_classes.append(test_target_class[4])
    test_app.db.session.commit()
    yield test_base_contests


@pytest.fixture
def test_contests(test_base_contests):
    from contest.tasks.models import Contest, ContestTypeEnum, ContestHoldingTypeEnum

    contests = [Contest(composite_type=ContestTypeEnum.Contest, holding_type=ContestHoldingTypeEnum.OfflineContest)
                for _ in range(8)]
    for i in range(len(contests)):
        base_contest = test_base_contests[i % len(test_base_contests)]
        base_contest.child_contests.extend(contests)
    test_app.db.session.add_all(contests)
    test_app.db.session.commit()
    yield contests


@pytest.fixture
def test_contests_composite(test_base_contests):
    from contest.tasks.models import CompositeContest, ContestTypeEnum, ContestHoldingTypeEnum

    contests = [
        CompositeContest(composite_type=ContestTypeEnum.CompositeContest,
                         holding_type=ContestHoldingTypeEnum.OfflineContest,
                         )
        for _ in range(8)]
    for i in range(len(contests)):
        test_base_contests[0].child_contests.append(contests[i])
    test_app.db.session.add_all(contests)
    test_app.db.session.commit()
    yield contests


@pytest.fixture
def test_simple_contest(test_base_contests_with_target, test_olympiad_locations):
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests_with_target[i].base_contest_id,
                                     visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=2),
                                     holding_type=holding_types[i % 2],
                                     regulations=f'Test {i}',
                                     show_answer_after_contest=True,
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=3),
                                     deadline_for_appeal=datetime.utcnow() + timedelta(minutes=45),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(7)]
    simple_contests.append(SimpleContest(
        base_contest_id=test_base_contests_with_target[7].base_contest_id,
        visibility=True,
        show_answer_after_contest=True,
        start_date=datetime(2007, 10, 6, 16, 29, 43, 79043),
        end_date=datetime(2007, 12, 6, 16, 29, 43, 79043),
        holding_type=holding_types[7 % 2],
        regulations=f'Test {7}',
        contest_duration=timedelta(minutes=30),
        result_publication_date=datetime(2007, 12, 6, 16, 29, 43, 79043),
        end_of_enroll_date=datetime(2007, 11, 6, 16, 29, 43, 79043)))
    simple_contests[3].previous_contest_id = 1
    simple_contests[3].previous_participation_condition = UserStatusEnum.Winner_1
    test_app.db.session.add_all(simple_contests)
    test_app.db.session.commit()
    yield simple_contests


@pytest.fixture
def test_simple_contest_with_location(test_simple_contest, test_olympiad_locations):
    for contest in test_simple_contest:
        contest.locations.append(test_olympiad_locations[0])
        contest.locations.append(test_olympiad_locations[1])
    yield test_simple_contest


# noinspection DuplicatedCode
@pytest.fixture
def test_stages(test_contests_composite, test_contests):
    from contest.tasks.models import Stage, StageConditionEnum

    stages = [Stage(stage_name=f'Test {i}', stage_num=i,
                    condition=StageConditionEnum.Or, this_stage_condition='Test')
              for i in range(8)]
    for i in range(len(stages)):
        test_contests_composite[0].stages.append(stages[i])
    test_app.db.session.add_all(stages)
    test_app.db.session.commit()
    yield stages


# noinspection DuplicatedCode
@pytest.fixture
def test_stages_and(test_contests_composite, test_contests):
    from contest.tasks.models import Stage, StageConditionEnum

    stages = [Stage(stage_name=f'Test {i}', stage_num=i,
                    condition=StageConditionEnum.And, this_stage_condition='Test')
              for i in range(8)]
    for i in range(len(stages)):
        test_contests_composite[0].stages.append(stages[i])
    test_app.db.session.add_all(stages)
    test_app.db.session.commit()
    yield stages


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_in_stage_1(test_base_contests_with_target, test_stages, test_olympiad_locations):
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                     visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     show_answer_after_contest=True,
                                     regulations=f'Test {i}',
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    for contest in simple_contests:
        contest.locations = [test_olympiad_locations[0]]

    other_stage = SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                visibility=True,
                                show_answer_after_contest=True,
                                start_date=datetime.utcnow(),
                                end_date=datetime.utcnow() + timedelta(hours=4),
                                holding_type=holding_types[0],
                                regulations=f'Test',
                                contest_duration=timedelta(minutes=30),
                                result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
    test_app.db.session.add(other_stage)

    other_stage.locations = [test_olympiad_locations[0]]
    test_app.db.session.flush()

    simple_contests[1].previous_contest_id = other_stage.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        user_status=UserStatusEnum.Participant)
    test_app.db.session.add(uic)
    other_stage.users.append(uic)

    for i in range(len(simple_contests)):
        test_stages[0].contests.append(simple_contests[i])

    test_stages[1].contests.append(other_stage)
    test_app.db.session.add_all(simple_contests)
    simple_contests.append(other_stage)
    test_app.db.session.commit()
    yield simple_contests


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_in_stage_2_contest_in_stage(test_base_contests_with_target, test_stages,
                                                    test_olympiad_locations):
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                     visibility=True,
                                     show_answer_after_contest=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     regulations=f'Test',
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    for contest in simple_contests:
        contest.locations.append(test_olympiad_locations[0])
        contest.locations.append(test_olympiad_locations[1])

    contest_in_other_stage_1 = SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                             contest_id=999,
                                             visibility=True,
                                             show_answer_after_contest=True,
                                             start_date=datetime.utcnow(),
                                             end_date=datetime.utcnow() + timedelta(hours=4),
                                             holding_type=holding_types[0],
                                             contest_duration=timedelta(minutes=30),
                                             regulations=f'Test',
                                             result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                             deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                             end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))

    contest_in_other_stage_2 = SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                             contest_id=1000,
                                             visibility=True,
                                             start_date=datetime.utcnow(),
                                             end_date=datetime.utcnow() + timedelta(hours=4),
                                             holding_type=holding_types[0],
                                             contest_duration=timedelta(minutes=30),
                                             regulations=f'Test',
                                             show_answer_after_contest=True,
                                             result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                             deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                             end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15),
                                             previous_contest_id=999,
                                             previous_participation_condition=UserStatusEnum.Participant)

    contest_in_other_stage_2.locations.append(test_olympiad_locations[0])
    contest_in_other_stage_1.locations.append(test_olympiad_locations[0])
    test_app.db.session.add(contest_in_other_stage_1)
    test_app.db.session.add(contest_in_other_stage_2)

    simple_contests[1].previous_contest_id = contest_in_other_stage_2.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        user_status=UserStatusEnum.Participant)
    test_app.db.session.add(uic)
    contest_in_other_stage_2.users.append(uic)

    for i in range(len(simple_contests)):
        test_stages[0].contests.append(simple_contests[i])

    test_stages[1].contests.append(contest_in_other_stage_2)
    test_app.db.session.add_all(simple_contests)
    simple_contests.append(contest_in_other_stage_2)
    test_app.db.session.commit()
    yield simple_contests


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_in_stage_and(test_base_contests_with_target, test_stages_and, test_olympiad_locations):
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                     visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     regulations=f'Test',
                                     contest_duration=timedelta(minutes=30),
                                     show_answer_after_contest=True,
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    other_stage = SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                visibility=True,
                                start_date=datetime.utcnow(),
                                end_date=datetime.utcnow() + timedelta(hours=4),
                                holding_type=holding_types[0],
                                regulations=f'Test',
                                show_answer_after_contest=True,
                                contest_duration=timedelta(minutes=30),
                                result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
    test_app.db.session.add(other_stage)

    test_app.db.session.flush()

    for contest in simple_contests:
        contest.locations.append(test_olympiad_locations[0])

    simple_contests[1].previous_contest_id = other_stage.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        user_status=UserStatusEnum.Participant)
    test_app.db.session.add(uic)
    other_stage.users.append(uic)

    for i in range(len(simple_contests)):
        test_stages_and[0].contests.append(simple_contests[i])

    test_stages_and[1].contests.append(other_stage)
    test_app.db.session.add_all(simple_contests)
    simple_contests.append(other_stage)
    other_stage.locations.append(test_olympiad_locations[0])
    test_app.db.session.commit()
    yield simple_contests


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_in_stage_2(test_base_contests_with_target, test_stages, test_olympiad_locations):
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest

    test_stages[0].stage_num = 1
    test_stages[1].stage_num = 1

    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                     visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     regulations=f'Test',
                                     show_answer_after_contest=True,
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    for contest in simple_contests:
        contest.locations.append(test_olympiad_locations[0])

    other_stage = SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                visibility=True,
                                start_date=datetime.utcnow(),
                                end_date=datetime.utcnow() + timedelta(hours=4),
                                holding_type=holding_types[0],
                                regulations=f'Test',
                                show_answer_after_contest=True,
                                contest_duration=timedelta(minutes=30),
                                result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
    test_app.db.session.add(other_stage)

    other_stage.locations.append(test_olympiad_locations[0])

    test_app.db.session.flush()

    simple_contests[1].previous_contest_id = other_stage.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        user_status=UserStatusEnum.Participant)
    test_app.db.session.add(uic)
    other_stage.users.append(uic)

    for i in range(len(simple_contests)):
        test_stages[0].contests.append(simple_contests[i])

    simple_contests.append(other_stage)

    test_stages[1].contests.append(other_stage)
    test_app.db.session.add_all(simple_contests)
    test_app.db.session.commit()
    yield simple_contests


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_in_stage_3(test_base_contests_with_target, test_stages, test_olympiad_locations):
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest

    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                     visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     regulations=f'Test',
                                     show_answer_after_contest=True,
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    for contest in simple_contests:
        contest.locations.append(test_olympiad_locations[0])
    other_stage = SimpleContest(base_contest_id=test_base_contests_with_target[0].base_contest_id,
                                visibility=True,
                                start_date=datetime.utcnow(),
                                show_answer_after_contest=True,
                                end_date=datetime.utcnow() + timedelta(hours=4),
                                holding_type=holding_types[0],
                                regulations=f'Test',
                                contest_duration=timedelta(minutes=30),
                                result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                deadline_for_appeal=datetime.utcnow() + timedelta(hours=2),
                                end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
    test_app.db.session.add(other_stage)
    other_stage.locations.append(test_olympiad_locations[0])

    test_app.db.session.flush()

    test_base_contests_with_target[0].child_contests.append(other_stage)

    simple_contests[1].previous_contest_id = other_stage.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        user_status=UserStatusEnum.Participant)
    test_app.db.session.add(uic)
    other_stage.users.append(uic)

    for i in range(len(simple_contests)):
        test_stages[0].contests.append(simple_contests[i])

    test_app.db.session.add_all(simple_contests)
    test_app.db.session.add(other_stage)
    test_app.db.session.commit()
    yield simple_contests


@pytest.fixture
def create_plain_task(test_create_tasks_pool):
    from contest.tasks.models.tasks import PlainTask
    plain_tasks = [PlainTask(name='Test',
                             image_of_task=None,
                             recommended_answer='answer')
                   for _ in range(8)]

    test_create_tasks_pool[0].tasks = plain_tasks
    test_app.db.session.add_all(plain_tasks)

    test_app.db.session.commit()
    yield plain_tasks


@pytest.fixture
def create_range_task(test_create_tasks_pool):
    from contest.tasks.models.tasks import RangeTask
    range_tasks = [RangeTask(name='Test',
                             image_of_task=None,
                             start_value=0.1,
                             end_value=0.5)
                   for _ in range(8)]
    test_create_tasks_pool[1].tasks = range_tasks
    test_app.db.session.add_all(range_tasks)
    test_app.db.session.commit()
    yield range_tasks


@pytest.fixture
def create_multiple_task(test_create_tasks_pool):
    from contest.tasks.models.tasks import MultipleChoiceTask
    multiple_tasks = [MultipleChoiceTask(name='Test',
                                         image_of_task=None,
                                         answers=[{
                                             'answer': '0',
                                             'is_right_answer': True
                                         }])
                      for _ in range(8)]
    test_create_tasks_pool[2].tasks = multiple_tasks
    test_app.db.session.add_all(multiple_tasks)
    test_app.db.session.commit()
    yield multiple_tasks


@pytest.fixture
def test_user_for_student_contest(test_city, test_university, test_user_university):
    from user.models import StudentInfo, UserInfo, Location, GenderEnum, Document, UserLimitations, DocumentTypeEnum, \
        StudentUniversityKnown, LocationRussia
    student_info = StudentInfo(admission_year=datetime.utcnow() + timedelta(hours=40))
    student_info.university = StudentUniversityKnown(university=test_university)
    location = Location()
    user_info = UserInfo(
        location_id=location.id,
        email="11@gmail.com",
        phone="89999999999",
        first_name="test",
        middle_name="test",
        second_name="test",
        date_of_birth=datetime.utcnow(),
        place_of_birth="test",
        gender=GenderEnum.male
    )
    user_info.dwelling = LocationRussia(city=test_city)
    user_info.document = Document(
        document_type=DocumentTypeEnum.rf_passport,
        series="444",
        number="444",
        issuer="444",
        issue_date=datetime.utcnow() + timedelta(hours=40),
        rf_code="4444444")
    user_info.limitations = UserLimitations(hearing=False,
                                            sight=False,
                                            movement=False)
    test_app.db.session.add(student_info)
    test_app.db.session.add(user_info)
    test_user_university.student_info = student_info
    test_user_university.user_info = user_info
    test_app.db.session.commit()
    yield test_user_university


@pytest.fixture
def test_user_for_student_contest_none(test_city, test_university, test_user_university):
    from user.models import StudentInfo, StudentUniversityKnown
    student_info = StudentInfo(admission_year=datetime.utcnow() + timedelta(hours=40))
    student_info.university = StudentUniversityKnown(university=test_university)
    user_info = None
    test_app.db.session.add(student_info)
    test_user_university.student_info = student_info
    test_user_university.user_info = user_info
    test_app.db.session.commit()
    yield test_user_university


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_with_users(test_simple_contest_with_location, test_olympiad_locations,
                                   test_user_for_student_contest):
    from contest.responses.models import add_user_response
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest_ = UserInContest(user_id=user_id,
                                     show_results_to_user=True,
                                     user_status=UserStatusEnum.Participant.value,
                                     location_id=test_olympiad_locations[0].location_id)
    test_simple_contest_with_location[0].users.append(user_in_contest_)

    test_app.db.session.add(user_in_contest_)
    test_app.db.session.commit()
    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest_with_location[0].contest_id)
    test_app.db.session.add(user_work)
    test_app.db.session.commit()

    yield test_simple_contest_with_location


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_with_users_no_variant(test_simple_contest_with_location, test_olympiad_locations,
                                              test_user_for_student_contest):
    from contest.responses.models import add_user_response
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest_ = UserInContest(user_id=user_id,
                                     show_results_to_user=True,
                                     user_status=UserStatusEnum.Participant.value,
                                     location_id=test_olympiad_locations[0].location_id)
    test_simple_contest_with_location[0].users.append(user_in_contest_)

    test_app.db.session.add(user_in_contest_)
    test_app.db.session.commit()

    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest_with_location[0].contest_id)
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest_with_location


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_with_users_not_in_progress(test_simple_contest, test_olympiad_locations,
                                                   test_user_for_student_contest):
    from contest.responses.models import add_user_response, ResponseStatusEnum
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest_ = UserInContest(user_id=user_id,
                                     show_results_to_user=True,
                                     user_status=UserStatusEnum.Participant.value,
                                     location_id=test_olympiad_locations[0].location_id)
    test_simple_contest[0].users.append(user_in_contest_)

    test_app.db.session.add(user_in_contest_)
    test_app.db.session.commit()
    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest[0].contest_id)

    user_work.work_status = ResponseStatusEnum.not_checked
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest


# noinspection DuplicatedCode
@pytest.fixture
def test_simple_contest_with_users_ended(test_simple_contest, test_olympiad_locations,
                                         test_user_for_student_contest):
    from contest.responses.models import add_user_response
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest_ = UserInContest(user_id=user_id,
                                     show_results_to_user=True,
                                     user_status=UserStatusEnum.Participant.value,
                                     location_id=test_olympiad_locations[0].location_id)
    test_simple_contest[0].users.append(user_in_contest_)

    test_app.db.session.add(user_in_contest_)
    test_app.db.session.commit()
    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest[0].contest_id)

    test_simple_contest[0].result_publication_date = datetime.utcnow()
    test_simple_contest[0].end_of_enroll_date = datetime.utcnow()
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest


# noinspection DuplicatedCode
@pytest.fixture
def test_composite_contest_with_users(test_simple_contest_in_stage_1, test_olympiad_locations,
                                      test_user_for_student_contest):
    from contest.responses.models import add_user_response
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest = UserInContest(user_id=user_id,
                                    show_results_to_user=True,
                                    user_status=UserStatusEnum.Participant.value,
                                    location_id=test_olympiad_locations[0].location_id)
    test_simple_contest_in_stage_1[0].users.append(user_in_contest)

    test_app.db.session.add(user_in_contest)
    test_app.db.session.commit()
    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest_in_stage_1[0].contest_id)

    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest_in_stage_1


@pytest.fixture
def test_certificate_type():
    from contest.tasks.models.certificate import CertificateType, Certificate
    from common.media_types import CertificateImage
    from contest.tasks.models import UserStatusEnum

    cert_type = CertificateType(name='test', description='test')

    now = datetime.utcnow()
    academic_year = now.year if now.month >= 9 else now.year - 1

    certs = [Certificate(certificate_category=status, certificate_year=academic_year, text_x=0, text_y=20,
                         text_width=100, max_lines=2)
             for status in UserStatusEnum]
    for cert in certs:
        test_app.io_to_media('CERTIFICATE', cert, 'certificate_image', io.BytesIO(test_image), CertificateImage)

    cert_type.certificates = certs
    test_app.db.session.add(cert_type)
    test_app.db.session.commit()

    yield cert_type
