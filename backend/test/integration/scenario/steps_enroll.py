from datetime import datetime, timedelta

from . import *


# TODO ADD USER INIT AND CYCLE FOR 5 USERS


def step_user_normal_enroll(client, state):
    for user in state.participants[:-1]:
        resp = client.login('/user/auth/login', username=user['username'], password=user['password'])
        assert resp.status_code == 200

        request = {'location_id': f'{state.olympiad_location["location_id"]}'}
        resp = client.post(f'contest/tasks'
                           f'/contest/{state.contest["contest_id"]}/enroll', json=request)
        assert resp.status_code == 200
        state.olympiad_type = dict()

        resp = client.logout('/user/auth/logout')
        assert resp.status_code == 200


def step_change_contest_enroll(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200

    request = {
        'end_of_enroll_date': f'{datetime.utcnow() - timedelta(hours=1)}'
    }
    resp = client.patch(f'contest/tasks/creator'
                        f'/base_olympiad/{state.base_olympiad["base_contest_id"]}'
                        f'/olympiad/{state.contest["contest_id"]}', json=request)
    assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


def step_user_late_enroll(client, state):
    wrong_user = state.participants[-1]

    resp = client.login('/user/auth/login', username=wrong_user['username'], password=wrong_user['password'])
    assert resp.status_code == 200

    request = {'location_id': f'{state.olympiad_location["location_id"]}'}
    resp = client.post(f'contest/tasks'
                       f'/contest/{state.contest["contest_id"]}/enroll', json=request)
    assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


steps_enroll = [step_user_normal_enroll,
                step_change_contest_enroll,
                step_user_late_enroll]
