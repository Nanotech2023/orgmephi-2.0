from . import *


@pytest.fixture
def client(client_university):
    client_university.set_prefix('/messages/participant')
    yield client_university


@pytest.fixture
def user(test_user_university):
    yield test_user_university


def test_message_author(client, user, test_messages):
    for msg in test_messages:
        assert msg.thread.author == user


def test_get_categories(client, test_thread_categories):
    resp = client.get('/categories')
    assert resp.status_code == 200
    assert len(test_thread_categories) == len(resp.json['categories'])
    cat_names = {v.name for v in test_thread_categories}
    for category in resp.json['categories']:
        assert category['name'] in cat_names
        cat_names.remove(category['name'])


# noinspection DuplicatedCode
def test_get_threads_all(client, test_threads):
    resp = client.get('/threads')
    assert resp.status_code == 200
    cmp_thread_list(test_threads, resp.json)


# noinspection DuplicatedCode
def test_get_threads_no_permission(client, test_user_school, test_threads):
    client.fake_login(username=test_user_school.username, role=test_user_school.role.value, user_id=test_user_school.id)
    resp = client.get('/threads')
    assert resp.status_code == 200
    assert len(resp.json['threads']) == 0


def test_get_threads_count_only(client, test_threads):
    resp = client.get('/threads?only_count=true')
    assert resp.status_code == 200
    assert resp.json['count'] == len(test_threads)
    assert 'threads' not in resp.json


# noinspection DuplicatedCode
def test_get_all_offset(client, test_threads):
    offset = int(len(test_threads) / 2)
    offset_threads = test_threads[offset:]
    resp = client.get(f'/threads?offset={offset}')
    assert resp.status_code == 200
    cmp_thread_list(offset_threads, resp.json)


def test_get_all_limit(client, test_threads):
    limit = int(len(test_threads) / 2)
    limit_threads = test_threads[:limit]
    resp = client.get(f'/threads?limit={limit}')
    assert resp.status_code == 200
    cmp_thread_list(limit_threads, resp.json)


# noinspection DuplicatedCode
def test_get_all_by_resolved(client, test_threads):
    resolved = [v for v in test_threads if v.resolved]
    unresolved = [v for v in test_threads if not v.resolved]

    resp = client.get(f'/threads?resolved=true')
    assert resp.status_code == 200
    cmp_thread_list(resolved, resp.json)

    resp = client.get(f'/threads?resolved=false')
    assert resp.status_code == 200
    cmp_thread_list(unresolved, resp.json)


# noinspection DuplicatedCode
def test_get_all_by_answered(client, test_threads):
    answered = [v for v in test_threads if v.answered]
    unanswered = [v for v in test_threads if not v.answered]

    resp = client.get(f'/threads?answered=true')
    assert resp.status_code == 200
    cmp_thread_list(answered, resp.json)

    resp = client.get(f'/threads?answered=false')
    assert resp.status_code == 200
    cmp_thread_list(unanswered, resp.json)


# noinspection DuplicatedCode
def test_get_all_by_thread_type(client, test_threads):
    test_type = test_threads[0].thread_type
    filtered_threads = [v for v in test_threads if v.thread_type == test_type]

    resp = client.get(f'/threads?thread_type={test_type.value}')
    assert resp.status_code == 200
    cmp_thread_list(filtered_threads, resp.json)


# noinspection DuplicatedCode
def test_get_all_by_thread_category(client, test_threads):
    test_category = test_threads[0].category
    filtered_threads = [v for v in test_threads if v.category == test_category]

    resp = client.get(f'/threads?category_name={test_category.name}')
    assert resp.status_code == 200
    cmp_thread_list(filtered_threads, resp.json)


# noinspection DuplicatedCode
def test_get_all_by_contest(client, test_threads):
    test_contest = test_threads[0].related_contest
    filtered_threads = [v for v in test_threads if v.related_contest == test_contest]

    resp = client.get(f'/threads?contest_id={test_contest.contest_id}')
    assert resp.status_code == 200
    cmp_thread_list(filtered_threads, resp.json)


def test_create_thread(client, test_thread_categories, create_user_response):
    from messages.models import Thread
    work = create_user_response['responses'][0]
    request = {
        "category": test_thread_categories[0].name,
        "message": "Test",
        "related_contest": work.contest_id,
        "thread_type": "Appeal",
        "topic": "string"
    }
    resp = client.post('/thread', json=request)
    assert resp.status_code == 200
    assert work.status.value == 'Appeal'

    thr = Thread.query.filter_by(id=resp.json['id']).one_or_none()
    cmp_thread(thr, resp.json)

    assert len(thr.messages) == 1
    assert thr.messages[0].message == 'Test'


def test_create_thread_missing_contest(client, test_thread_categories, create_user_response):
    work = create_user_response['responses'][0]
    request = {
        "category": test_thread_categories[0].name,
        "message": "Test",
        "thread_type": "Contest",
        "topic": "string"
    }
    resp = client.post('/thread', json=request)
    assert resp.status_code == 400


def test_create_thread_quota(client, test_thread_categories, create_user_response):
    work = create_user_response['responses'][0]
    request = {
        "category": test_thread_categories[0].name,
        "message": "Test",
        "related_contest": work.contest_id,
        "thread_type": "Appeal",
        "topic": "string"
    }
    quota = test_app.config['ORGMEPHI_DAILY_THREAD_LIMIT']
    for _ in range(quota):
        resp = client.post('/thread', json=request)
        assert resp.status_code == 200

    resp = client.post('/thread', json=request)
    assert resp.status_code == 409


def test_get_thread(client, test_threads, test_messages):
    thread = test_threads[0]
    resp = client.get(f'/thread/{thread.id}')
    assert resp.status_code == 200
    cmp_thread(thread, resp.json)
    assert len(thread.messages) == len(resp.json['messages'])
    for msg in thread.messages:
        msg_data = next((v for v in resp.json['messages'] if v['message_id'] == msg.id))
        assert msg_data['post_time'] == msg.post_time.isoformat()
        assert msg_data['employee'] == msg.employee_id
        assert msg_data['message'] == msg.message


def test_get_thread_wrong_author(client, test_threads, test_messages, test_user_school):
    thread = test_threads[0]
    client.fake_login(username=test_user_school.username, role=test_user_school.role.value, user_id=test_user_school.id)
    resp = client.get(f'/thread/{thread.id}')
    assert resp.status_code == 404


def test_post_message(client, test_threads, test_messages):
    from messages.models import Thread
    thread = next((v for v in test_threads if not v.resolved))
    request = {'message': 'Test'}
    resp = client.post(f'/message/{thread.id}', json=request)
    assert resp.status_code == 200

    thr = Thread.query.filter_by(id=thread.id).one_or_none()
    msg = next((v for v in thr.messages if v.id == resp.json['message_id']))
    assert resp.json['post_time'] == msg.post_time.isoformat()
    assert resp.json['employee'] == msg.employee_id
    assert msg.employee_id is None
    assert resp.json['message'] == msg.message == 'Test'


def test_post_message_wrong_author(client, test_threads, test_messages, test_user_school):
    thread = next((v for v in test_threads if not v.resolved))
    client.fake_login(username=test_user_school.username, role=test_user_school.role.value, user_id=test_user_school.id)
    request = {'message': 'Test'}
    resp = client.post(f'/message/{thread.id}', json=request)
    assert resp.status_code == 404


def test_post_message_resolved(client, test_threads, test_messages):
    thread = next((v for v in test_threads if v.resolved))
    request = {'message': 'Test'}
    resp = client.post(f'/message/{thread.id}', json=request)
    assert resp.status_code == 409


def test_post_message_quota(client, test_threads, test_messages):
    thread = next((v for v in test_threads if not v.resolved))
    request = {'message': 'Test'}
    quota = test_app.config['ORGMEPHI_DAILY_MESSAGE_LIMIT']
    for _ in range(quota):
        resp = client.post(f'/message/{thread.id}', json=request)
        assert resp.status_code == 200
    resp = client.post(f'/message/{thread.id}', json=request)
    assert resp.status_code == 409
