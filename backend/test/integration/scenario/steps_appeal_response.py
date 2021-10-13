from . import *


def step_appeal_answer(client, state):
    user = state.creator
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    user_a = state.appeal_accept['user_id']
    user_b = state.appeal_reject['user_id']

    resp = client.get('/messages/creator/threads?resolved=False&thread_type=Appeal')
    assert resp.status_code == 200
    assert resp.json['count'] == 2

    thr_a = None
    thr_b = None

    for thr in resp.json['threads']:
        if thr['author'] == user_a:
            thr_a = thr['id']
        elif thr['author'] == user_b:
            thr_b = thr['id']

    resp = client.get(f'/messages/creator/thread/{thr_a}')
    assert resp.status_code == 200
    assert len(resp.json['messages']) == 1

    resp = client.post(f'/messages/creator/message/{thr_a}', json={'message': 'Ok cool'})
    assert resp.status_code == 200

    resp = client.post(f'/messages/creator/thread_status/{thr_a}', json={'status': 'Accepted'})
    assert resp.status_code == 200

    resp = client.get(f'/messages/creator/thread/{thr_b}')
    assert resp.status_code == 200
    assert len(resp.json['messages']) == 1

    resp = client.post(f'/messages/creator/message/{thr_b}', json={'message': 'Rejected'})
    assert resp.status_code == 200

    resp = client.post(f'/messages/creator/thread_status/{thr_b}', json={'status': 'Rejected'})
    assert resp.status_code == 200


    client.logout('/user/auth/logout')


def step_appeal_read_a(client, state):
    user = state.participants[0]
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/participant/threads?thread_type=Appeal')
    assert resp.status_code == 200
    assert resp.json['count'] == 1
    thread_id = resp.json['threads'][0]['id']

    resp = client.get(f'/messages/participant/thread/{thread_id}')
    assert resp.status_code == 200
    assert len(resp.json['messages']) == 2
    assert resp.json['status'] == 'Accepted'

    client.logout('/user/auth/logout')


def step_appeal_read_b(client, state):
    user = state.participants[1]
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get('/messages/participant/threads?thread_type=Appeal')
    assert resp.status_code == 200
    assert resp.json['count'] == 1
    thread_id = resp.json['threads'][0]['id']

    resp = client.get(f'/messages/participant/thread/{thread_id}')
    assert resp.status_code == 200
    assert len(resp.json['messages']) == 2
    assert resp.json['status'] == 'Rejected'

    resp = client.post(f'/messages/participant/message/{thread_id}', json={'message': 'Go to shell'})
    assert resp.status_code == 409

    client.logout('/user/auth/logout')


steps_appeal_response = [step_appeal_answer, step_appeal_read_a, step_appeal_read_b]
