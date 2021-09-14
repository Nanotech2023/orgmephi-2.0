from datetime import datetime, timedelta
from ..user import *


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
def test_olympiad_types():
    from contest.tasks.models import OlympiadType
    olympiad_types = [OlympiadType(olympiad_type=f'Test {i}') for i in range(8)]
    test_app.db.session.add_all(olympiad_types)
    test_app.db.session.commit()
    yield olympiad_types


@pytest.fixture
def test_olympiad_locations():
    from contest.tasks.models import OnlineOlympiadLocation, RussiaOlympiadLocation, \
        OtherOlympiadLocation
    online_olympiad_location = [
        OnlineOlympiadLocation(url=f'Test {i}') for i in range(2)
    ]
    russia_olympiad_location = [
        RussiaOlympiadLocation(city_name='Москва',
                               region_name='Московская обл.',
                               address=f'Test {i}') for i in range(2)
    ]
    other_olympiad_location = [
        OtherOlympiadLocation(country_name='Россия',
                              location=f'Test {i}') for i in range(2)
    ]
    test_app.db.session.add_all(online_olympiad_location + russia_olympiad_location + other_olympiad_location)
    test_app.db.session.commit()
    yield online_olympiad_location + russia_olympiad_location + other_olympiad_location


@pytest.fixture
def test_base_contests(test_olympiad_types):
    from contest.tasks.models import BaseContest, OlympiadSubjectEnum
    contests = [BaseContest(name=f'Test {i}', rules=f'Test{i}', description=f'Test {i}',
                            subject=OlympiadSubjectEnum.Math,
                            winner_1_condition=0.95,
                            winner_2_condition=0.9,
                            winner_3_condition=0.8,
                            diploma_1_condition=0.7,
                            diploma_2_condition=0.6,
                            diploma_3_condition=0.5) for i in range(8)]
    for i in range(len(contests)):
        olympiad_type = test_olympiad_types[i % len(test_olympiad_types)]
        olympiad_type.contests.extend(contests)
    test_app.db.session.add_all(contests)
    test_app.db.session.commit()
    yield contests


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
def test_simple_contest(test_base_contests_with_target):
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests_with_target[i].base_contest_id,
                                     visibility=True, start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=2),
                                     holding_type=holding_types[i % 2],
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=3),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(8)]
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


@pytest.fixture
def test_simple_contest_in_stage_1(test_base_contests_with_target, test_stages):
    from contest.tasks.models import Variant
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    other_stage = SimpleContest(visibility=True,
                                start_date=datetime.utcnow(),
                                end_date=datetime.utcnow() + timedelta(hours=4),
                                holding_type=holding_types[0],
                                contest_duration=timedelta(minutes=30),
                                result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
    test_app.db.session.add(other_stage)

    test_app.db.session.flush()

    simple_contests[1].previous_contest_id = other_stage.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    simple_contests[1].variants.append(Variant(variant_number=1, variant_description="3"))

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        variant_id=1,
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


@pytest.fixture
def test_simple_contest_in_stage_2(test_base_contests_with_target, test_stages):
    from contest.tasks.models import Variant
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest

    test_stages[0].stage_num = 1
    test_stages[1].stage_num = 1

    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    other_stage = SimpleContest(visibility=True,
                                start_date=datetime.utcnow(),
                                end_date=datetime.utcnow() + timedelta(hours=4),
                                holding_type=holding_types[0],
                                contest_duration=timedelta(minutes=30),
                                result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
    test_app.db.session.add(other_stage)

    test_app.db.session.flush()

    simple_contests[1].previous_contest_id = other_stage.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    simple_contests[1].variants.append(Variant(variant_number=1, variant_description="3"))

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        variant_id=1,
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


@pytest.fixture
def test_simple_contest_in_stage_3(test_base_contests_with_target, test_stages):
    from contest.tasks.models import Variant
    from contest.tasks.models.user import UserStatusEnum
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    from contest.tasks.models import UserInContest

    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(visibility=True,
                                     start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=4),
                                     holding_type=holding_types[i % 2],
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(2)]

    other_stage = SimpleContest(visibility=True,
                                start_date=datetime.utcnow(),
                                end_date=datetime.utcnow() + timedelta(hours=4),
                                holding_type=holding_types[0],
                                contest_duration=timedelta(minutes=30),
                                result_publication_date=datetime.utcnow() + timedelta(hours=6),
                                end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
    test_app.db.session.add(other_stage)

    test_app.db.session.flush()

    test_base_contests_with_target[0].child_contests.append(other_stage)

    simple_contests[1].previous_contest_id = other_stage.contest_id
    simple_contests[1].previous_participation_condition = UserStatusEnum.Participant

    simple_contests[1].variants.append(Variant(variant_number=1, variant_description="3"))

    uic = UserInContest(user_id=1,
                        show_results_to_user=True,
                        location_id=1,
                        variant_id=1,
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
def test_variant(test_simple_contest):
    from contest.tasks.models.contest import Variant
    variants = [Variant(variant_number=i,
                        variant_description='description')
                for i in range(8)]
    for i in range(len(variants)):
        test_simple_contest[0].variants.append(variants[i])
    test_app.db.session.add_all(variants)
    test_app.db.session.commit()
    yield variants


@pytest.fixture
def create_plain_task(test_variant):
    from contest.tasks.models.tasks import PlainTask
    plain_tasks = [PlainTask(num_of_task=i,
                             image_of_task=None,
                             show_answer_after_contest=True,
                             task_points=10 + i,
                             recommended_answer='answer')
                   for i in range(8)]
    test_app.db.session.add_all(plain_tasks)
    for i in range(7):
        test_variant[0].tasks.append(plain_tasks[i])

    test_variant[1].tasks.append(plain_tasks[7])
    test_app.db.session.commit()
    yield plain_tasks


@pytest.fixture
def create_range_task(test_variant):
    from contest.tasks.models.tasks import RangeTask
    range_tasks = [RangeTask(num_of_task=i,
                             image_of_task=None,
                             start_value=0.1,
                             end_value=0.5,
                             task_points=10 + i,
                             show_answer_after_contest=True, )
                   for i in range(8)]
    test_app.db.session.add_all(range_tasks)
    for i in range(8):
        test_variant[0].tasks.append(range_tasks[i])
    test_app.db.session.commit()
    yield range_tasks


@pytest.fixture
def create_multiple_task(test_variant):
    from contest.tasks.models.tasks import MultipleChoiceTask
    multiple_tasks = [MultipleChoiceTask(num_of_task=i,
                                         image_of_task=None,
                                         answers=[{
                                             'answer': '0',
                                             'is_right_answer': True
                                         }],
                                         task_points=10 + i,
                                         show_answer_after_contest=True, )
                      for i in range(8)]
    test_app.db.session.add_all(multiple_tasks)
    for i in range(8):
        test_variant[0].tasks.append(multiple_tasks[i])
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


@pytest.fixture
def test_simple_contest_with_users(test_simple_contest, test_variant, test_olympiad_locations,
                                   test_user_for_student_contest):
    from contest.responses.models import add_user_response, ResponseStatusEnum
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest = UserInContest(user_id=user_id,
                                    show_results_to_user=True,
                                    user_status=UserStatusEnum.Participant.value,
                                    variant_id=test_variant[0].variant_id,
                                    location_id=test_olympiad_locations[0].location_id)
    test_simple_contest[0].users.append(user_in_contest)

    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest[0].contest_id)
    user_work.work_status = ResponseStatusEnum.in_progress
    test_app.db.session.add(user_in_contest)
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest


@pytest.fixture
def test_simple_contest_with_users_no_variant(test_simple_contest, test_variant, test_olympiad_locations,
                                              test_user_for_student_contest):
    from contest.responses.models import add_user_response, ResponseStatusEnum
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest = UserInContest(user_id=user_id,
                                    show_results_to_user=True,
                                    user_status=UserStatusEnum.Participant.value,
                                    variant_id=152,
                                    location_id=test_olympiad_locations[0].location_id)
    test_simple_contest[0].users.append(user_in_contest)

    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest[0].contest_id)
    user_work.work_status = ResponseStatusEnum.in_progress
    test_app.db.session.add(user_in_contest)
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest


@pytest.fixture
def test_simple_contest_with_users_not_in_progress(test_simple_contest, test_variant, test_olympiad_locations,
                                                   test_user_for_student_contest):
    from contest.responses.models import add_user_response, ResponseStatusEnum
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest = UserInContest(user_id=user_id,
                                    show_results_to_user=True,
                                    user_status=UserStatusEnum.Participant.value,
                                    variant_id=test_variant[0].variant_id,
                                    location_id=test_olympiad_locations[0].location_id)
    test_simple_contest[0].users.append(user_in_contest)

    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest[0].contest_id)
    user_work.work_status = ResponseStatusEnum.not_checked
    test_app.db.session.add(user_in_contest)
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest


@pytest.fixture
def test_simple_contest_with_users_ended(test_simple_contest, test_variant, test_olympiad_locations,
                                         test_user_for_student_contest):
    from contest.responses.models import add_user_response, ResponseStatusEnum
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest = UserInContest(user_id=user_id,
                                    show_results_to_user=True,
                                    user_status=UserStatusEnum.Participant.value,
                                    variant_id=test_variant[0].variant_id,
                                    location_id=test_olympiad_locations[0].location_id)
    test_simple_contest[0].users.append(user_in_contest)

    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest[0].contest_id)
    user_work.work_status = ResponseStatusEnum.in_progress
    test_simple_contest[0].result_publication_date = datetime.utcnow()
    test_simple_contest[0].end_of_enroll_date = datetime.utcnow()
    test_app.db.session.add(user_in_contest)
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest


@pytest.fixture
def test_composite_contest_with_users(test_simple_contest_in_stage_1, test_variant, test_olympiad_locations,
                                      test_user_for_student_contest):
    from contest.responses.models import add_user_response, ResponseStatusEnum
    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_id = test_user_for_student_contest.id
    user_in_contest = UserInContest(user_id=user_id,
                                    show_results_to_user=True,
                                    user_status=UserStatusEnum.Participant.value,
                                    variant_id=test_variant[0].variant_id,
                                    location_id=test_olympiad_locations[0].location_id)
    test_simple_contest_in_stage_1[0].users.append(user_in_contest)

    user_work = add_user_response(test_app.db.session, user_id, test_simple_contest_in_stage_1[0].contest_id)
    user_work.work_status = ResponseStatusEnum.in_progress
    test_app.db.session.add(user_in_contest)
    test_app.db.session.add(user_work)

    test_app.db.session.commit()
    yield test_simple_contest_in_stage_1
