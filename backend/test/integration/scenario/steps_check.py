from . import *


def step_creator_auto_check(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200

    contest_id = state.contest['contest_id']

    resp = client.post(f'contest/responses/creator/contest/{contest_id}/check')
    assert resp.status_code == 200

    for user in state.participants[:-1]:
        user_id = user['id']
        resp = client.get(f"contest/responses/creator/contest/{contest_id}"
                          f"/user/{user_id}/response")
        assert resp.status_code == 200

        user_answers = resp.json['user_answers']
        for answer in user_answers:
            if answer['answer_type'] == 'PlainAnswerText':
                resp = client.post(f'contest/responses/creator/contest/{contest_id}/task/{answer["task_id"]}'
                                   f'/user/{user_id}/mark', json={'mark': 2 + user_id})
                assert resp.status_code == 200
                break

        resp = client.post(f'contest/responses/creator/contest/{contest_id}'
                           f'/user/{user_id}/status', json={'status': 'Accepted'})
        assert resp.status_code == 200

    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


steps_check = [step_creator_auto_check]
