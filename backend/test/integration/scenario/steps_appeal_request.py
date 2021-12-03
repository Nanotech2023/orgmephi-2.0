from . import *

def step_appeal_request_a(client, state):
    user = state.participants[0]
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/participant/categories')
    assert resp.status_code == 200
    assert state.msg_categories['request'] in [v['name'] for v in resp.json['categories']]

    request = {
        'category': state.msg_categories['request'],
        'thread_type': 'Appeal',
        'topic': 'Please recheck my work',
        'message': 'You checked my work wrong!',
        'related_contest': state.contest['contest_id']
    }

    resp = client.post('/messages/participant/thread', json=request)
    assert resp.status_code == 200

    client.logout('/user/auth/logout')


def step_appeal_request_b(client, state):
    user = state.participants[1]
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/participant/categories')
    assert resp.status_code == 200
    assert state.msg_categories['request'] in [v['name'] for v in resp.json['categories']]

    request = {
        'category': state.msg_categories['request'],
        'thread_type': 'Appeal',
        'topic': 'You are idiots',
        'message': 'My work is good. You are bad. Go eat dog food!',
        'related_contest': state.contest['contest_id']
    }

    resp = client.post('/messages/participant/thread', json=request)
    assert resp.status_code == 200

    client.logout('/user/auth/logout')


def step_answer(client, state):
    user = state.creator
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/creator/threads?resolved=False')
    assert resp.status_code == 200
    assert resp.json['count'] == 2

    user_a = resp.json['threads'][0]['author']
    user_b = resp.json['threads'][1]['author']

    state.appeal_accept = {'user_id': user_a}
    state.appeal_reject = {'user_id': user_b}

    client.logout('/user/auth/logout')


steps_appeal_request = [step_appeal_request_a, step_appeal_request_b, step_answer]
