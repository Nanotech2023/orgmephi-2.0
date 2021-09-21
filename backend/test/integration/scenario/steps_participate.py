from . import *
from datetime import datetime, timedelta


# noinspection DuplicatedCode
def step_response_to_contest_a(client, state):
    user = state.participants[0]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.post(f'contest/responses/participant'
                       f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 200

    resp = client.get(f'contest/tasks/participant'
                      f'/contest/{contest_id}/variant/self')
    assert resp.status_code == 200

    var_id = resp.json['variant_id']
    resp = client.get(f'contest/tasks/participant'
                      f'/contest/{contest_id}/tasks/self')
    assert resp.status_code == 200
    tasks_list = resp.json['tasks_list']

    for task in tasks_list:
        task_type = task['task_type']
        task_id = task['task_id']
        if task_type == 'PlainTask':
            request = {
                "answer_text": f'Test recommendation {var_id - 1}'
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/plain', json=request)
            assert resp.status_code == 200
        elif task_type == 'RangeTask':
            request = {
                "answer": 0.5
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/range', json=request)
            assert resp.status_code == 200
        elif task_type == 'MultipleChoiceTask':
            request = {
                "answers": [
                    {"answer": task['answers'][1]['answer']},
                    {"answer": task['answers'][3]['answer']}
                ]
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/multiple', json=request)
            assert resp.status_code == 200

    resp = client.get(f'contest/responses/participant/contest/{contest_id}/user/self/time')
    assert resp.status_code == 200
    assert resp.json['time'] < 14400

    resp = client.post(f'contest/responses/participant/contest/{contest_id}/user/self/finish')
    assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_response_to_contest_b(client, state):
    user = state.participants[1]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.post(f'contest/responses/participant'
                       f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 200

    resp = client.get(f'contest/tasks/participant'
                      f'/contest/{contest_id}/tasks/self')
    assert resp.status_code == 200
    tasks_list = resp.json['tasks_list']

    for task in tasks_list:
        task_type = task['task_type']
        task_id = task['task_id']
        if task_type == 'PlainTask':
            request = {
                "answer_text": f'False Answer'
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/plain', json=request)
            assert resp.status_code == 200
        elif task_type == 'RangeTask':
            request = {
                "answer": 0.5
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/range', json=request)
            assert resp.status_code == 200
        elif task_type == 'MultipleChoiceTask':
            request = {
                "answers": [
                    {"answer": task['answers'][1]['answer']},
                    {"answer": task['answers'][3]['answer']}
                ]
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/multiple', json=request)
            assert resp.status_code == 200

    resp = client.get(f'contest/responses/participant/contest/{contest_id}/user/self/time')
    assert resp.status_code == 200
    assert resp.json['time'] < 14400

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_response_to_contest_c(client, state):
    user = state.participants[2]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.post(f'contest/responses/participant'
                       f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 200

    resp = client.get(f'contest/tasks/participant'
                      f'/contest/{contest_id}/tasks/self')
    assert resp.status_code == 200
    tasks_list = resp.json['tasks_list']

    for task in tasks_list:
        task_type = task['task_type']
        task_id = task['task_id']
        if task_type == 'PlainTask':
            request = {
                "answer_text": f'False Answer'
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/plain', json=request)
            assert resp.status_code == 200
        elif task_type == 'RangeTask':
            request = {
                "answer": 1.8
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/range', json=request)
            assert resp.status_code == 200
        elif task_type == 'MultipleChoiceTask':
            request = {
                "answers": [
                    {"answer": task['answers'][0]['answer']},
                    {"answer": task['answers'][2]['answer']}
                ]
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/multiple', json=request)
            assert resp.status_code == 200

    resp = client.get(f'contest/responses/participant/contest/{contest_id}/user/self/time')
    assert resp.status_code == 200
    assert resp.json['time'] < 14400

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_response_to_contest_d(client, state):
    user = state.participants[3]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.post(f'contest/responses/participant'
                       f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 200

    resp = client.get(f'contest/tasks/participant'
                      f'/contest/{contest_id}/tasks/self')
    assert resp.status_code == 200
    tasks_list = resp.json['tasks_list']

    for task in tasks_list:
        task_type = task['task_type']
        task_id = task['task_id']
        if task_type == 'PlainTask':
            request = {
                "answer_text": f'False Answer'
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/plain', json=request)
            assert resp.status_code == 200
        elif task_type == 'RangeTask':
            request = {
                "answer": 0.4
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/range', json=request)
            assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


def step_creator_time_change(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200

    request = {
        'end_date': f'{datetime.utcnow() - timedelta(minutes=15)}'
    }
    resp = client.patch(f'contest/tasks/editor/base_olympiad/{state.base_olympiad["base_contest_id"]}'
                        f'/olympiad/{state.contest["contest_id"]}', json=request)
    assert resp.status_code == 200

    request = {
        'time': 3600
    }
    resp = client.post(f'contest/responses/creator'
                       f'/contest/{state.contest["contest_id"]}/user/{state.participants[3]["id"]}/time',
                       json=request)
    assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_response_to_contest_c_change(client, state):
    user = state.participants[2]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get(f'contest/tasks/participant'
                      f'/contest/{contest_id}/tasks/self')
    assert resp.status_code == 200
    tasks_list = resp.json['tasks_list']

    for task in tasks_list:
        task_type = task['task_type']
        task_id = task['task_id']
        if task_type == 'PlainTask':
            request = {
                "answer_text": f'Not Right Answer'
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/plain', json=request)
            assert resp.status_code == 409
            break

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_response_to_contest_d_change(client, state):
    user = state.participants[3]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get(f'contest/tasks/participant'
                      f'/contest/{contest_id}/tasks/self')
    assert resp.status_code == 200
    tasks_list = resp.json['tasks_list']

    for task in tasks_list:
        task_type = task['task_type']
        task_id = task['task_id']
        if task_type == 'MultipleChoiceTask':
            request = {
                "answers": [
                    {"answer": task['answers'][0]['answer']},
                    {"answer": task['answers'][1]['answer']}
                ]
            }
            resp = client.post(f'contest/responses/participant'
                               f'/contest/{contest_id}/task/{task_id}/user/self/multiple', json=request)
            assert resp.status_code == 200

    resp = client.post(f'contest/responses/participant/contest/{contest_id}/user/self/finish')
    assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_response_to_contest_e(client, state):
    user = state.participants[4]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.post(f'contest/responses/participant'
                       f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 409

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


steps_participate = [step_response_to_contest_a, step_response_to_contest_b, step_response_to_contest_c,
                     step_response_to_contest_d, step_creator_time_change, step_response_to_contest_c_change,
                     step_response_to_contest_d_change, step_response_to_contest_e]
