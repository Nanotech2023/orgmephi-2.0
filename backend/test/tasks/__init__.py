from datetime import datetime, timedelta

from ..user import *  # Fixtures


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
                            winner_1_condition=(i % 10),
                            winner_2_condition=(i % 10),
                            winner_3_condition=(i % 10),
                            diploma_1_condition=(i % 10),
                            diploma_2_condition=(i % 10),
                            diploma_3_condition=(i % 10)) for i in range(8)]
    for i in range(len(contests)):
        olympiad_type = test_olympiad_types[i % len(test_olympiad_types)]
        olympiad_type.contests.extend(contests)
    test_app.db.session.add_all(contests)
    test_app.db.session.commit()
    yield contests


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
        base_contest = test_base_contests[i % len(test_base_contests)]
        base_contest.child_contests.extend(contests)
    test_app.db.session.add_all(contests)
    test_app.db.session.commit()
    yield contests


@pytest.fixture
def test_simple_contest(test_base_contests):
    from contest.tasks.models.olympiad import SimpleContest, ContestHoldingTypeEnum
    holding_types = [ContestHoldingTypeEnum.OnLineContest, ContestHoldingTypeEnum.OfflineContest]
    simple_contests = [SimpleContest(base_contest_id=test_base_contests[i],
                                     visibility=True, start_date=datetime.utcnow(),
                                     end_date=datetime.utcnow() + timedelta(hours=2),
                                     holding_type=holding_types[i % 2],
                                     contest_duration=timedelta(minutes=30),
                                     result_publication_date=datetime.utcnow() + timedelta(hours=3),
                                     end_of_enroll_date=datetime.utcnow() + timedelta(minutes=15))
                       for i in range(8)]
    for i in range(len(simple_contests)):
        base_contest = test_base_contests[i % len(test_base_contests)]
        base_contest.child_contests.extend(simple_contests)
    test_app.db.session.add_all(simple_contests)
    test_app.db.session.commit()
    yield simple_contests


@pytest.fixture
def test_stages(test_contests_composite, test_contests):
    from contest.tasks.models import Stage, StageConditionEnum

    stages = [Stage(stage_name=f'Test {i}', stage_num=i,
                    condition=StageConditionEnum.Or, this_stage_condition='Test')
              for i in range(8)]
    for i in range(len(stages)):
        test_contests_composite.stages.append(stages[i])
    test_app.db.session.add_all(stages)
    test_app.db.session.commit()
    yield stages


@pytest.fixture
def test_variant(test_simple_contest):
    from contest.tasks.models.contest import Variant
    variants = [Variant(contest_id=test_simple_contest[i].contest_id,
                        variant_number=i,
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
                             show_answer_after_contest=None,
                             task_points=10 + i,
                             recommended_answer='answer')
                   for i in range(8)]
    test_app.db.session.add_all(plain_tasks)
    for i in range(8):
        test_variant[0].tasks.append(plain_tasks[i])
    test_app.db.session.commit()
    yield plain_tasks
