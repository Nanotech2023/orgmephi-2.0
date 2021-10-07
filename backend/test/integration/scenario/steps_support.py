from . import *

def step_create_categories(client, state):
    user = state.admin
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    categories = {'technical': 'Technical', 'question': 'Question', 'request': 'Request'}
    for category in categories.values():
        resp = client.post('/messages/admin/add_category', json={'name': category})
        assert resp.status_code == 204

    state.msg_categories = categories

    client.logout('/user/auth/logout')

def step_ask(client, state):
    user = state.participants[0]
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/participant/categories')
    assert resp.status_code == 200
    assert state.msg_categories['question'] in [v['name'] for v in resp.json['categories']]

    request = {
        'category': state.msg_categories['question'],
        'thread_type': 'Contest',
        'topic': 'Please help!',
        'message': 'When will the contest start',
        'related_contest': state.contest['contest_id']
    }

    resp = client.post('/messages/participant/thread', json=request)
    assert resp.status_code == 200

    state.support_message = {'id': resp.json['id']}

    client.logout('/user/auth/logout')


def step_answer(client, state):
    user = state.creator
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/creator/threads?resolved=False')
    assert resp.status_code == 200
    assert resp.json['count'] == 1
    thread_id = resp.json['threads'][0]['id']

    resp = client.get(f'/messages/creator/thread/{thread_id}')
    assert resp.status_code == 200
    assert len(resp.json['messages']) == 1

    resp = client.post(f'/messages/creator/message/{thread_id}', json={'message': 'Soon'})
    assert resp.status_code == 200

    resp = client.post(f'/messages/creator/thread_status/{thread_id}', json={'status': 'Closed'})
    assert resp.status_code == 200

    client.logout('/user/auth/logout')


def step_read(client, state):
    user = state.participants[0]
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/participant/threads')
    assert resp.status_code == 200
    assert resp.json['count'] == 1
    thread_id = resp.json['threads'][0]['id']

    assert thread_id == state.support_message['id']

    resp = client.get(f'/messages/participant/thread/{thread_id}')
    assert resp.status_code == 200
    assert len(resp.json['messages']) == 2

    client.logout('/user/auth/logout')


steps_support = [step_create_categories, step_ask, step_answer, step_read]
