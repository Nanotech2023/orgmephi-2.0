from datetime import datetime, timedelta

from . import *

GENERATE_TASKS_NUMBER = 3
GENERATE_TASK_POOLS = 3


def step_creator_login(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200


def step_create_base_olympiad(client, state):
    from contest.tasks.models import OlympiadSubjectEnum, OlympiadLevelEnum
    request = {'name': 'Base olympiad 1',
               'description': 'Description of Base olympiad 1',
               'rules': 'Rules of Base olympiad 1',
               'winner_1_condition': 0.9,
               'winner_2_condition': 0.8,
               'winner_3_condition': 0.7,
               'diploma_1_condition': 0.6,
               'diploma_2_condition': 0.5,
               'diploma_3_condition': 0.4,
               'level': OlympiadLevelEnum.Level1.value,
               'olympiad_type_id': f'{state.olympiad_type["olympiad_type_id"]}',
               'subject': OlympiadSubjectEnum.Math.value}
    resp = client.post('contest/tasks/creator/base_olympiad/create', json=request)
    assert resp.status_code == 200
    state.base_olympiad = dict()
    state.base_olympiad['base_contest_id'] = resp.json['base_contest_id']

    request = {
        'target_classes_ids': state.target_classes
    }
    resp = client.post(f'contest/tasks/editor'
                       f'/base_olympiad/{state.base_olympiad["base_contest_id"]}/add_target_classes', json=request)
    assert resp.status_code == 200


def step_create_olympiad_composite(client, state):
    from contest.tasks.models import ContestHoldingTypeEnum
    request = {
        'visibility': True,
        'holding_type': ContestHoldingTypeEnum.OnLineContest.value, }
    resp = client.post(f'contest/tasks/creator/base_olympiad/{state.base_olympiad["base_contest_id"]}'
                       f'/olympiad/create_composite', json=request)
    assert resp.status_code == 200
    state.composite_olympiad = dict()
    state.composite_olympiad['contest_id'] = resp.json['contest_id']


def step_create_stage(client, state):
    from contest.tasks.models import StageConditionEnum
    request = {
        'stage_name': 'Test stage',
        'stage_num': 1,
        'this_stage_condition': 'Description of this stage condition',
        'condition': StageConditionEnum.No.value, }
    resp = client.post(f'contest/tasks/creator'
                       f'/olympiad/{state.composite_olympiad["contest_id"]}/stage/create', json=request)
    assert resp.status_code == 200
    state.stage = dict()
    state.stage['stage_id'] = resp.json['stage_id']


def step_create_simple_contest(client, state):
    from contest.tasks.models import ContestHoldingTypeEnum
    request = {
        'visibility': True,
        'holding_type': ContestHoldingTypeEnum.OnLineContest.value,
        'start_date': f'{datetime.utcnow()}',
        'end_date': f'{datetime.utcnow() + timedelta(hours=4)}',
        'regulations': 'Test 0',
        'end_of_enroll_date': f'{datetime.utcnow() + timedelta(hours=1)}',
        'deadline_for_appeal': f'{datetime.utcnow() + timedelta(hours=3)}',
        'result_publication_date': f'{datetime.utcnow() + timedelta(hours=5)}',
        'show_answer_after_contest': True,
        'stage_id': f'{state.stage["stage_id"]}'}
    resp = client.post(f'contest/tasks/creator'
                       f'/base_olympiad/{state.base_olympiad["base_contest_id"]}/olympiad/create_simple', json=request)
    assert resp.status_code == 200
    state.contest = dict()
    state.contest['contest_id'] = resp.json['contest_id']

    request = {
        'locations': [state.olympiad_location["location_id"]],
    }
    resp = client.post(f'contest/tasks/editor'
                       f'/contest/{state.contest["contest_id"]}/add_location', json=request)
    assert resp.status_code == 200


def step_create_tasks_pool(client, state):
    request = {
        'name': 'Test tasks pool 1',
        'year': 2021,
        'orig_task_points': 20
    }
    state.tasks_pools = []
    for _ in range(GENERATE_TASK_POOLS):
        resp = client.post(f'contest/tasks/creator'
                           f'/base_olympiad/{state.base_olympiad["base_contest_id"]}/task_pool/create',
                           json=request)
        assert resp.status_code == 200
        state.tasks_pools.append(
            {
                'task_pool_id': resp.json['task_pool_id'],
                'tasks': list()
            }
        )


def step_create_contest_tasks(client, state):
    state.contest_tasks = []
    for i in range(GENERATE_TASKS_NUMBER):
        request = {
            'num': i + 1,
            'task_points': 15,
            'task_pools': [state.tasks_pools[i]['task_pool_id']]
        }
        if i == 1:
            request['task_points'] = 8
        resp = client.post(f'contest/tasks/creator'
                           f'/contest/{state.contest["contest_id"]}/contest_task/create',
                           json=request)
        assert resp.status_code == 200
        state.contest_tasks.append(resp.json['contest_task_id'])


def step_create_tasks(client, state):
    for i in range(GENERATE_TASK_POOLS):
        request = {
            'name': f'Test tasks pool 1 - {i}',
            'recommended_answer': f'Test recommendation {str(i)}'
        }

        resp = client.post(f'contest/tasks/creator'
                           f'/task_pool/{state.tasks_pools[0]["task_pool_id"]}/task/create_plain', json=request)
        assert resp.status_code == 200
        state.tasks_pools[i]['tasks'].append({
            "task_id": resp.json['task_id'],
            "name": f'Test tasks pool 1 - {i}',
            "recommended_answer": f'Test recommendation {i}',
        })

        request = {
            'name': f'Test tasks pool 2 - {i}',
            'start_value': 0.1,
            'end_value': 0.8,
        }

        resp = client.post(f'contest/tasks/creator'
                           f'/task_pool/{state.tasks_pools[1]["task_pool_id"]}/task/create_range', json=request)
        assert resp.status_code == 200
        state.tasks_pools[i]['tasks'].append({
            "task_id": resp.json['task_id'],
            "name": f'Test tasks pool 2 - {i}',
            "start_value": 0.1,
            "end_value": 0.8,
        })

        answers = [
            {
                'answer': f'test 1.{str(i)}',
                'is_right_answer': False
            },
            {
                'answer': f'test 2.{str(i)}',
                'is_right_answer': True
            },
            {
                'answer': f'test 3.{str(i)}',
                'is_right_answer': False
            },
            {
                'answer': f'test 4.{str(i)}',
                'is_right_answer': True
            }
        ]

        request = {
            'name': f'Test tasks pool 3 - {i}',
            'answers': answers
        }

        resp = client.post(f'contest/tasks/creator'
                           f'/task_pool/{state.tasks_pools[2]["task_pool_id"]}/task/create_multiple', json=request)
        assert resp.status_code == 200
        state.tasks_pools[i]['tasks'].append({
            "task_id": resp.json['task_id'],
            "name": f'Test tasks pool 3 - {i}',
            "answers": answers
        })


def step_creator_logout(client, state):
    resp = client.logout('/user/auth/logout')
    assert resp.status_code == 200


steps_create_olympiad = [step_creator_login, step_create_base_olympiad, step_create_olympiad_composite,
                         step_create_stage, step_create_simple_contest,
                         step_create_tasks_pool, step_create_contest_tasks, step_create_tasks,
                         step_creator_logout]
