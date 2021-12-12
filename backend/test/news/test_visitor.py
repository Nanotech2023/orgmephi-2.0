from . import *


@pytest.fixture
def client(client_visitor):
    client_visitor.set_prefix('/news/visitor')
    yield client_visitor


# noinspection DuplicatedCode
def test_get_all(client, test_news_posted):
    resp = client.get('/news')
    assert resp.status_code == 200
    cmp_news_list(test_news_posted, resp.json)


def test_get_count_only(client, test_news_posted):
    resp = client.get('/news?only_count=true')
    assert resp.status_code == 200
    assert resp.json['count'] == len(test_news_posted)
    assert 'news' not in resp.json


# noinspection DuplicatedCode
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


# noinspection DuplicatedCode
def test_get_news_not_exists(client, test_news):
    max_id = max([v.id for v in test_news])
    resp = client.get(f'/news/{max_id + 1}')
    assert resp.status_code == 404


def test_get_image(client, test_news_posted):
    news = test_news_posted[0]
    resp = client.get(f'/news/{news.id}/image')
    assert resp.status_code == 200
    assert resp.content_type == 'image/jpeg'


def test_get_image_not_posted(client, test_news_not_posted):
    news = test_news_not_posted[0]
    resp = client.get(f'/news/{news.id}/image')
    assert resp.status_code == 404


# noinspection DuplicatedCode
def test_get_image_not_exists(client, test_news):
    max_id = max([v.id for v in test_news])
    resp = client.get(f'/news/{max_id + 1}/image')
    assert resp.status_code == 404


def test_get_image_none(client, test_news_posted):
    news = test_news_posted[0]
    with test_app.store_manager:
        news.image = None
    test_app.db.session.commit()
    resp = client.get(f'/news/{news.id}/image')
    assert resp.status_code == 404
