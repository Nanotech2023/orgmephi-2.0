from . import *


# noinspection DuplicatedCode
def step_view_first_work(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200
    user_id = state.participants[0]['id']
    contest_id = state.contest['contest_id']

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/user/{user_id}/response')
    assert resp.status_code == 200

    task_id = 0
    for elem in resp.json['user_answers']:
        if elem['answer_type'] == 'PlainAnswerText':
            task_id = elem['task_id']
            break

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == "PlainAnswerText"

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 200

    resp = client.post(f'contest/responses/creator/contest/{contest_id}/task/{task_id}/user/{user_id}/mark',
                       json={'mark': resp.json['mark'] + 1})
    assert resp.status_code == 200

    from contest.tasks.models.olympiad import UserStatusEnum
    resp = client.patch(f'contest/tasks/control_users/contest/{contest_id}/edit_users',
                        json={
                            'users_id': [user_id],
                            'user_status': UserStatusEnum.Winner_1.value
                        })
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_view_second_work(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200
    user_id = state.participants[1]['id']
    contest_id = state.contest['contest_id']

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/user/{user_id}/response')
    assert resp.status_code == 200

    task_id = 0
    for elem in resp.json['user_answers']:
        if elem['answer_type'] == 'PlainAnswerText':
            task_id = elem['task_id']
            break

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == "PlainAnswerText"

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 200

    client.logout('/user/auth/logout')


steps_view_work = [step_view_first_work, step_view_second_work]
