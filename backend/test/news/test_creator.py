from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('/news/creator')
    yield client_creator


def test_list_categories(client, test_categories):
    resp = client.get('/categories')
    assert resp.status_code == 200
    assert len(resp.json['categories']) == len(test_categories)
    assert set([v.name for v in test_categories]) == set([v['name'] for v in resp.json['categories']])


# noinspection DuplicatedCode
def test_get_all(client, test_news):
    resp = client.get('/news')
    assert resp.status_code == 200
    cmp_news_list(test_news, resp.json)


def test_get_count_only(client, test_news):
    resp = client.get('/news?only_count=true')
    assert resp.status_code == 200
    assert resp.json['count'] == len(test_news)
    assert 'news' not in resp.json


# noinspection DuplicatedCode
def test_get_all_offset(client, test_news):
    offset = int(len(test_news) / 2)
    offset_news = test_news[offset:]
    resp = client.get(f'/news?offset={offset}')
    assert resp.status_code == 200
    cmp_news_list(offset_news, resp.json)


def test_get_all_limit(client, test_news):
    limit = int(len(test_news) / 2)
    limit_news = test_news[:limit]
    resp = client.get(f'/news?limit={limit}')
    assert resp.status_code == 200
    cmp_news_list(limit_news, resp.json)


def test_get_all_by_category(client, test_news):
    category = test_news[0].category
    filtered_news = [v for v in test_news if v.category == category]
    resp = client.get(f'/news?category_name={category.name}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_all_by_grade(client, test_news):
    grade = test_news[0].grade
    filtered_news = [v for v in test_news if v.grade == grade]
    resp = client.get(f'/news?grade={grade}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_all_by_title_full(client, test_news):
    title = test_news[0].title
    filtered_news = [v for v in test_news if v.title == title]
    resp = client.get(f'/news?title={title}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_all_by_title_partial(client, test_news):
    title = 'Test'
    resp = client.get(f'/news?title={title}')
    assert resp.status_code == 200
    cmp_news_list(test_news, resp.json)


def test_get_all_by_contest(client, test_news):
    contest = test_news[0].related_contest
    filtered_news = [v for v in test_news if v.related_contest == contest]
    resp = client.get(f'/news?contest_id={contest.contest_id}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_all_by_posted(client, test_news):
    posted = test_news[0].posted
    filtered_news = [v for v in test_news if v.posted == posted]
    resp = client.get(f'/news?posted={posted}')
    assert resp.status_code == 200
    cmp_news_list(filtered_news, resp.json)


def test_get_news(client, test_news):
    news = test_news[0]
    resp = client.get(f'/news/{news.id}')
    assert resp.status_code == 200
    cmp_news(news, resp.json, False)


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


# noinspection DuplicatedCode
def test_create_news(client, test_categories):
    category = test_categories[0]
    request = {
        'category': category.name,
        'title': 'Test'
    }
    resp = client.post('/news', json=request)
    assert resp.status_code == 200
    news_post = resp.json
    resp = client.get(f'/news/{news_post["id"]}')
    assert resp.status_code == 200
    news_get = resp.json

    assert news_post['id'] == news_get['id']
    assert news_post['category'] == news_get['category'] == category.name
    assert news_post['post_time'] == news_get['post_time']
    assert news_post['posted'] == news_get['posted']
    assert not news_post['posted']
    assert news_post['grade'] == news_get['grade']
    assert news_post['grade'] is None
    assert news_post['title'] == news_get['title'] == 'Test'
    assert news_post['body'] == news_get['body']
    assert news_post['body'] is None
    assert news_post['related_contest'] == news_get['related_contest']
    assert news_post['related_contest'] is None


# noinspection DuplicatedCode
def test_edit_news(client, test_categories, test_contests):
    category = test_categories[0]
    contest = test_contests[0]
    request_create = {
        'category': category.name,
        'title': 'Test'
    }
    request_edit = {
        'grade': 11,
        'body': 'Test',
        'related_contest': contest.contest_id
    }
    resp = client.post('/news', json=request_create)
    resp = client.patch(f'/news/{resp.json["id"]}', json=request_edit)
    assert resp.status_code == 200
    news_post = resp.json
    resp = client.get(f'/news/{news_post["id"]}')
    assert resp.status_code == 200
    news_get = resp.json

    assert news_post['id'] == news_get['id']
    assert news_post['category'] == news_get['category'] == category.name
    assert news_post['post_time'] == news_get['post_time']
    assert news_post['posted'] == news_get['posted']
    assert not news_post['posted']
    assert news_post['grade'] == news_get['grade'] == 11
    assert news_post['title'] == news_get['title'] == 'Test'
    assert news_post['body'] == news_get['body'] == 'Test'
    assert news_post['related_contest'] == news_get['related_contest'] == contest.contest_id


def test_post_image(client, test_categories, test_contests):
    category = test_categories[0]
    request_create = {
        'category': category.name,
        'title': 'Test'
    }
    resp = client.post('/news', json=request_create)
    news_id = resp.json['id']
    resp = client.post(f'/news/{news_id}/image', data=test_image)
    assert resp.status_code == 204
    resp = client.get(f'/news/{news_id}/image')
    assert resp.status_code == 200
    assert resp.content_type == 'image/jpeg'


def test_post_image_none(client, test_categories, test_contests):
    category = test_categories[0]
    request_create = {
        'category': category.name,
        'title': 'Test'
    }
    resp = client.post('/news', json=request_create)
    news_id = resp.json['id']
    resp = client.post(f'/news/{news_id}/image')
    assert resp.status_code == 400


def test_post_news(client, test_categories):
    category = test_categories[0]
    request_create = {
        'category': category.name,
        'title': 'Test'
    }
    resp = client.post('/news', json=request_create)
    news_id = resp.json['id']
    resp = client.post(f'/news/{news_id}/post')
    assert resp.status_code == 204
    resp = client.get(f'/news/{news_id}')
    assert resp.status_code == 200
    assert resp.json['posted']


def test_hide_news(client, test_categories):
    category = test_categories[0]
    request_create = {
        'category': category.name,
        'title': 'Test'
    }
    resp = client.post('/news', json=request_create)
    news_id = resp.json['id']
    client.post(f'/news/{news_id}/post')
    resp = client.post(f'/news/{news_id}/hide')
    assert resp.status_code == 204
    resp = client.get(f'/news/{news_id}')
    assert resp.status_code == 200
    assert not resp.json['posted']
