import pytest

from common.testing import get_test_app, OrgMephiTestingClient, reset_db

from news import module

# noinspection DuplicatedCode
test_app = get_test_app(module)


@pytest.fixture
def client():
    reset_db(test_app)
    with test_app.app.test_client() as client:
        yield OrgMephiTestingClient(client)


@pytest.fixture
def client_creator(client):
    client.fake_login(role='Creator')
    yield client


@pytest.fixture
def client_admin(client):
    client.fake_login(role='Admin')
    yield client


@pytest.fixture
def test_categories():
    from news.models import NewsCategory
    categories = [NewsCategory(name=f'Test category {i}') for i in range(2)]
    test_app.db.session.add_all(categories)
    test_app.db.session.commit()
    yield categories


@pytest.fixture
def test_contests():
    from contest.tasks.models import Contest, BaseContest, OlympiadType, OlympiadSubjectEnum, ContestTypeEnum, \
        ContestHoldingTypeEnum
    olympiad_type = OlympiadType(olympiad_type='test')
    base = BaseContest(name='test', rules='test', description='test', subject=OlympiadSubjectEnum.Math,
                       winning_condition=1.0, laureate_condition=1.0, target_classes=[11])
    olympiad_type.contests = [base]

    contests = [Contest(composite_type=ContestTypeEnum.Contest, holding_type=ContestHoldingTypeEnum.OfflineContest)
                for _ in range(4)]
    base.child_contests = contests
    test_app.db.session.add_all(contests)
    test_app.db.session.commit()
    yield contests


@pytest.fixture
def test_news(test_categories, test_contests):
    from news.models import News
    news = [News(title=f'Test news {i}', body=f'Test news {i}', posted=(i % 2 == 0),
                 category=test_categories[i % len(test_categories)], grade=(i % 4 + 8),
                 related_contest=test_contests[i % len(test_contests)], image=str.encode(f'{i}')) for i in range(8)]
    test_app.db.session.add_all(news)
    test_app.db.session.commit()
    yield news


@pytest.fixture
def test_news_posted(test_news):
    yield [v for v in test_news if v.posted]


@pytest.fixture
def test_news_not_posted(test_news):
    yield [v for v in test_news if not v.posted]


# noinspection Assert
def cmp_news(news, json, info=True):
    assert json['id'] == news.id
    assert json['category'] == news.category_name
    assert json['post_time'] == news.post_time.isoformat()
    assert json['posted'] == news.posted
    assert json['grade'] == news.grade
    assert json['title'] == news.title
    if info:
        assert 'body' not in json
    else:
        assert json['body'] == news.body


# noinspection Assert
def cmp_news_list(news_list, json, info=True):
    assert json['count'] == len(news_list)
    assert len(json['news']) == len(news_list)
    for news in news_list:
        resp_news = next((v for v in json['news'] if v['id'] == news.id))
        cmp_news(news, resp_news, info)