from datetime import datetime, timedelta

from . import *

GENERATE_VARIANTS_NUMBER = 5


def step_creator_login(client, state):
    resp = client.login('/user/auth/login', username=state.creator['username'], password=state.creator['password'])
    assert resp.status_code == 200


def step_create_base_olympiad(client, state):
    from contest.tasks.models import OlympiadSubjectEnum
    request = {'name': 'Base olympiad 1',
               'description': 'Description of Base olympiad 1',
               'rules': 'Rules of Base olympiad 1',
               'winner_1_condition': '0.9',
               'winner_2_condition': '0.8',
               'winner_3_condition': '0.7',
               'diploma_1_condition': '0.6',
               'diploma_2_condition': '0.5',
               'diploma_3_condition': '0.4',
               'olympiad_type_id': f'{state.olympiad_type["olympiad_type_id"]}',
               'subject': f'{OlympiadSubjectEnum.Math.value}'}
    resp = client.post('contest/tasks/creator/base_olympiad/create', json=request)
    assert resp.status_code == 200
    state.base_olympiad = dict()
    state.base_olympiad['base_contest_id'] = resp.json['base_contest_id']


def step_create_olympiad_composite(client, state):
    from contest.tasks.models import ContestHoldingTypeEnum
    request = {
        'visibility': 'true',
        'holding_type': f'{ContestHoldingTypeEnum.OnLineContest.value}', }
    resp = client.post(f'contest/tasks/creator/base_olympiad/{state.base_olympiad["base_contest_id"]}'
                       f'/olympiad/create_composite', json=request)
    assert resp.status_code == 200
    state.composite_olympiad = dict()
    state.composite_olympiad['contest_id'] = resp.json['contest_id']


def step_create_stage(client, state):
    from contest.tasks.models import StageConditionEnum
    request = {
        'stage_name': 'Test stage',
        'stage_num': '1',
        'this_stage_condition': 'Description of this stage condition',
        'condition': f'{StageConditionEnum.No.value}', }
    resp = client.post(f'contest/tasks/creator'
                       f'/olympiad/{state.composite_olympiad["contest_id"]}/stage/create', json=request)
    assert resp.status_code == 200
    state.stage = dict()
    state.stage['stage_id'] = resp.json['stage_id']


def step_create_simple_contest(client, state):
    from contest.tasks.models import ContestHoldingTypeEnum
    request = {
        'visibility': 'true',
        'holding_type': f'{ContestHoldingTypeEnum.OnLineContest.value}',
        'start_date': f'{datetime.utcnow()}',
        'end_date': f'{datetime.utcnow() + timedelta(hours=4)}',
        'end_of_enroll_date': f'{datetime.utcnow() + timedelta(hours=1)}',
        'result_publication_date': f'{datetime.utcnow() + timedelta(hours=5)}',
        'stage_id': f'{state.stage["stage_id"]}'}
    resp = client.post(f'contest/tasks/creator'
                       f'/base_olympiad/{state.base_olympiad["base_contest_id"]}/olympiad/create_simple', json=request)
    assert resp.status_code == 200
    state.contest = dict()
    state.contest['contest_id'] = resp.json['contest_id']

    request = {
       ' locations': [f'{state.olympiad_location["location_id"]}'],
    }
    resp = client.post(f'contest/tasks/creator'
                       f'/contest/{state.contest["contest_id"]}/add_location', json=request)

    assert resp.status_code == 200


def step_create_variants(client, state):
    request = {
        'variant_description': 'Test variant description'}
    state.variants = []
    for _ in range(GENERATE_VARIANTS_NUMBER):
        resp = client.post(f'contest/tasks/creator'
                           f'/contest/{state.contest["contest_id"]}/variant/create', json=request)
        assert resp.status_code == 200
        state.variants.append({
            "variant_id": resp.json['variant_id'],
            "tasks": dict()
        })


def step_create_tasks(client, state):
    for i in range(GENERATE_VARIANTS_NUMBER):
        request = {
            'num_of_task': '1',
            'recommended_answer': 'Test recommendation',
            'show_answer_after_contest': 'false',
            'task_points': '10', }

        resp = client.post(f'contest/tasks/creator'
                           f'/contest/{state.contest["contest_id"]}/variant/{state.variants[i]["variant_id"]}'
                           f'/task/create_plain', json=request)
        assert resp.status_code == 200
        state.variants[i]['tasks']['plain'] = {
            "task_id": resp.json['task_id'],
            "show_answer_after_contest": 'false',
            "task_points": '10',
            "recommended_answer": 'Test recommendation',
        }

        request = {
            'num_of_task': '2',
            'start_value': '0.1',
            'end_value': '0.8',
            'show_answer_after_contest': 'true',
            'task_points': '8',
        }

        resp = client.post(f'contest/tasks/creator'
                           f'/contest/{state.contest["contest_id"]}/variant/{state.variants[i]["variant_id"]}'
                           f'/task/create_range', json=request)
        assert resp.status_code == 200
        state.variants[i]['tasks']['range'] = {
            "task_id": resp.json['task_id'],
            "show_answer_after_contest": 'true',
            "task_points": '8',
            "start_value": '0.1',
            "end_value": '0.8',
        }

        answers = [
            {
                'answer': 'test 1',
                'is_right_answer': 'false'
            },
            {
                'answer': 'test 2',
                'is_right_answer': 'true'
            },
            {
                'answer': 'test 3',
                'is_right_answer': 'false'
            },
            {
                'answer': 'test 4',
                'is_right_answer': 'true'
            }
        ]

        request = {
            'num_of_task': '2',
            'answers': answers,
            'show_answer_after_contest': 'true',
            'task_points': '15',
        }

        resp = client.post(f'contest/tasks/creator'
                           f'/contest/{state.contest["contest_id"]}/variant/{state.variants[i]["variant_id"]}'
                           f'/task/create_multiple', json=request)
        assert resp.status_code == 200
        state.variants[i]['tasks']['multiple'] = {
            "task_id": resp.json['task_id'],
            "show_answer_after_contest": 'true',
            "task_points": '15',
            "answers": answers
        }


steps_create_olympiad = [step_creator_login, step_create_base_olympiad, step_create_olympiad_composite,
                         step_create_stage, step_create_simple_contest, step_create_variants,
                         step_create_tasks]
