from datetime import datetime, timedelta

from . import *


# TODO ADD USER INIT AND CYCLE FOR 5 USERS


def step_user_normal_enroll(client, state):
    request = {'location_id': f'state.olympiad_location["location_id"]'}
    resp = client.post(f'contest/tasks'
                       f'/contest/{state.contest["contest_id"]}/enroll', json=request)
    assert resp.status_code == 200
    state.olympiad_type = dict()


def step_creator_login(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200


def step_change_contest_enroll(client, state):
    request = {
        'end_of_enroll_date': f'{datetime.utcnow() - timedelta(hours=1)}'
    }
    resp = client.patch(f'contest/tasks/creator'
                        f'/base_olympiad/{state.base_olympiad["base_contest_id"]}'
                        f'/olympiad/{state.contest["contest_id"]}', json=request)
    assert resp.status_code == 200


# TODO ADD LAST USER INIT


def step_user_late_enroll(client, state):
    request = {'location_id': f'state.olympiad_location["location_id"]'}
    resp = client.post(f'contest/tasks'
                       f'/contest/{state.contest["contest_id"]}/enroll', json=request)
    assert resp.status_code == 200


steps_enroll = [step_user_normal_enroll,
                step_creator_login, step_change_contest_enroll,
                step_user_late_enroll]
