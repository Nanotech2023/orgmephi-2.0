from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('/messages/creator')
    yield client_creator


# noinspection DuplicatedCode
def test_get_threads_all(client, test_threads):
    resp = client.get('/threads')
    assert resp.status_code == 200
    cmp_thread_list(test_threads, resp.json)


# noinspection DuplicatedCode
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


# noinspection DuplicatedCode
def test_post_message(client, test_user_creator, test_threads, test_messages):
    from messages.models import Thread
    thread = next((v for v in test_threads if not v.resolved))
    thread.messages[-1].employee_id = None
    test_app.db.session.commit()
    update_time = thread.update_time
    assert not thread.answered
    request = {'message': 'Test'}
    resp = client.post(f'/message/{thread.id}', json=request)
    assert resp.status_code == 200

    thr = Thread.query.filter_by(id=thread.id).one_or_none()
    msg = next((v for v in thr.messages if v.id == resp.json['message_id']))
    assert resp.json['post_time'] == msg.post_time.isoformat()
    assert resp.json['employee'] == msg.employee_id == test_user_creator.id
    assert resp.json['message'] == msg.message == 'Test'
    assert thr.answered
    assert thr.update_time > update_time


# noinspection DuplicatedCode
def test_post_message_resolved(client, test_user_creator, test_threads, test_messages):
    from messages.models import Thread
    thread = next((v for v in test_threads if v.resolved))
    request = {'message': 'Test'}
    resp = client.post(f'/message/{thread.id}', json=request)
    assert resp.status_code == 200

    thr = Thread.query.filter_by(id=thread.id).one_or_none()
    msg = next((v for v in thr.messages if v.id == resp.json['message_id']))
    assert resp.json['post_time'] == msg.post_time.isoformat()
    assert resp.json['employee'] == msg.employee_id == test_user_creator.id
    assert resp.json['message'] == msg.message == 'Test'


def test_update_status(client, test_user_creator, test_threads, test_messages):
    from messages.models import ThreadType, ThreadStatus, Thread
    thread = next((v for v in test_threads if not v.resolved and v.thread_type != ThreadType.appeal))
    request = {'status': ThreadStatus.closed.value}
    resp = client.post(f'/thread_status/{thread.id}', json=request)
    assert resp.status_code == 200

    thr = Thread.query.filter_by(id=thread.id).one_or_none()
    assert thr.status == ThreadStatus.closed


def test_update_status_appeal(client, test_user_creator, test_threads, test_messages):
    from messages.models import ThreadType, ThreadStatus
    thread = next((v for v in test_threads if not v.resolved and v.thread_type == ThreadType.appeal))
    request = {'status': ThreadStatus.closed.value}
    resp = client.post(f'/thread_status/{thread.id}', json=request)
    assert resp.status_code == 409
