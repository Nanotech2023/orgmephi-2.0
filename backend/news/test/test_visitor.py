import pytest

from common.testing import get_test_app, OrgMephiTestingClient, reset_db

from news.visitor import module

# noinspection DuplicatedCode
test_app = get_test_app(module)


@pytest.fixture
def client():
    reset_db(test_app)
    with test_app.app.test_client() as client:
        yield OrgMephiTestingClient(client)


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


def cmp_news_list(news_list, json, info=True):
    assert json['count'] == len(news_list)
    assert len(json['news']) == len(news_list)
    for news in news_list:
        resp_news = next((v for v in json['news'] if v['id'] == news.id))
        cmp_news(news, resp_news, info)


def test_get_all(client, test_news_posted):
    resp = client.get('/news')
    assert resp.status_code == 200
    cmp_news_list(test_news_posted, resp.json)


def test_get_count_only(client, test_news_posted):
    resp = client.get('/news?only_count=true')
    assert resp.status_code == 200
    assert resp.json['count'] == len(test_news_posted)
    assert 'news' not in resp.json


def test_get_all_offset(client, test_news_posted):
    offset = int(len(test_news_posted) / 2)
    offset_news = test_news_posted[offset:]
    resp = client.get(f'/news?offset={offset}')
    assert resp.status_code == 200
    cmp_news_list(offset_news, resp.json)


def test_get_all_limit(client, test_news_posted):
    limit = int(len(test_news_posted) / 2)
    limit_news = test_news_posted[:limit]
    resp = client.get(f'/news?limit={limit}')
    assert resp.status_code == 200
    cmp_news_list(limit_news, resp.json)


def test_get_all_by_category(client, test_news_posted):
    category = test_news_posted[0].category
    filtered_news = [v for v in test_news_posted if v.category == category]
    resp = client.get(f'/news?category_name={category.name}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_all_by_grade(client, test_news_posted):
    grade = test_news_posted[0].grade
    filtered_news = [v for v in test_news_posted if v.grade == grade]
    resp = client.get(f'/news?grade={grade}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_all_by_title_full(client, test_news_posted):
    title = test_news_posted[0].title
    filtered_news = [v for v in test_news_posted if v.title == title]
    resp = client.get(f'/news?title={title}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_all_by_title_partial(client, test_news_posted):
    title = 'Test'
    resp = client.get(f'/news?title={title}')
    assert resp.status_code == 200
    cmp_news_list(test_news_posted, resp.json)


def test_get_all_by_contest(client, test_news_posted):
    contest = test_news_posted[0].related_contest
    filtered_news = [v for v in test_news_posted if v.related_contest == contest]
    resp = client.get(f'/news?contest_id={contest.contest_id}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_news(client, test_news_posted):
    news = test_news_posted[0]
    resp = client.get(f'/news/{news.id}')
    assert resp.status_code == 200
    cmp_news(news, resp.json, False)


def test_get_news_not_posted(client, test_news_not_posted):
    news = test_news_not_posted[0]
    resp = client.get(f'/news/{news.id}')
    assert resp.status_code == 404


def test_get_news_not_exists(client, test_news):
    max_id = max([v.id for v in test_news])
    resp = client.get(f'/news/{max_id + 1}')
    assert resp.status_code == 404


def test_get_image(client, test_news_posted):
    news = test_news_posted[0]
    resp = client.get(f'/news/{news.id}/image')
    assert resp.status_code == 200
    assert resp.data == news.image


def test_get_image_not_posted(client, test_news_not_posted):
    news = test_news_not_posted[0]
    resp = client.get(f'/news/{news.id}/image')
    assert resp.status_code == 404


def test_get_image_not_exists(client, test_news):
    max_id = max([v.id for v in test_news])
    resp = client.get(f'/news/{max_id + 1}/image')
    assert resp.status_code == 404


def test_get_image_none(client, test_news_posted):
    news = test_news_posted[0]
    news.image = None
    test_app.db.session.commit()
    resp = client.get(f'/news/{news.id}/image')
    assert resp.status_code == 409
