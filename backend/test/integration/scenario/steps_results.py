from . import *
from datetime import datetime, timedelta


def step_user_results_too_early(client, state):
    user = state.participants[0]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get(f'contest/responses/participant/contest/{contest_id}/user/self/mark')
    assert resp.status_code == 409

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


def step_creator_result_publication_date_change(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200

    request = {
        'result_publication_date': f'{datetime.utcnow() - timedelta(minutes=15)}'
    }
    resp = client.patch(f'contest/tasks/editor/base_olympiad/{state.base_olympiad["base_contest_id"]}'
                        f'/olympiad/{state.contest["contest_id"]}', json=request)
    assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


# noinspection DuplicatedCode
def step_user_results_a(client, state):
    user = state.participants[0]
    contest_id = state.contest['contest_id']
    resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
    assert resp.status_code == 200

    resp = client.get(f'contest/responses/participant/contest/{contest_id}/user/self/mark')
    assert resp.status_code == 409

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


def step_show_results_to_creator(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200

    contest_id = state.contest['contest_id']
    user_id_a = state.participants[0]['id']
    user_id_c = state.participants[2]['id']

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/user/{user_id_a}/mark')
    assert resp.status_code == 200

    user_answers = resp.json['user_answers']
    for answer in user_answers:
        if answer['answer_type'] == 'PlainAnswerText':
            assert answer['mark'] == 2 + user_id_a
        elif answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 8
            assert answer['right_answer']["start_value"] == 0.1
            assert answer['right_answer']["end_value"] == 0.8
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 15
            assert len(answer['right_answer']['answers']) == 2

    resp = client.get(f'contest/responses/creator/contest/{contest_id}/user/{user_id_c}/mark')
    assert resp.status_code == 200

    user_answers = resp.json['user_answers']
    for answer in user_answers:
        if answer['answer_type'] == 'PlainAnswerText':
            assert answer['mark'] == 2 + user_id_c
        elif answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 0
            assert answer['right_answer']["start_value"] == 0.1
            assert answer['right_answer']["end_value"] == 0.8
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 0
            assert len(answer['right_answer']['answers']) == 2

    resp = client.get(f'contest/tasks/control_users/contest/{contest_id}/user/all')
    assert resp.status_code == 200

    for user in resp.json['user_list']:
        if user['user_id'] == user_id_a or user['user_id'] == state.participants[1]['id']:
            assert user['user_status'] == 'Winner 3'
        elif user['user_id'] == user_id_c:
            assert user['user_status'] == 'Participant'
        elif user['user_id'] == state.participants[3]['id']:
            assert user['user_status'] == 'Diploma 3'

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


steps_results = [step_user_results_too_early, step_creator_result_publication_date_change,
                 step_user_results_a, step_show_results_to_creator]
