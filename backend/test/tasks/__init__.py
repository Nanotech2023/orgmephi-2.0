from .. import *
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
    test_app.db.session.add_all(online_olympiad_location+russia_olympiad_location+other_olympiad_location)
    test_app.db.session.commit()
    yield online_olympiad_location+russia_olympiad_location+other_olympiad_location


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
