import io

from contest.tasks.models import ContestTask
from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('contest/tasks/creator')
    yield client_creator


def test_base_olympiad_create(client, test_olympiad_types):
    from contest.tasks.models import BaseContest
    resp = client.post('/base_olympiad/create',
                       json={
                           'name': 'Test 0',
                           'description': 'Test 0',
                           'rules': 'Test 0',
                           'winner_1_condition': '0.5',
                           'winner_2_condition': '0.5',
                           'winner_3_condition': '0.5',
                           'diploma_1_condition': '0.5',
                           'diploma_2_condition': '0.5',
                           'diploma_3_condition': '0.5',
                           'olympiad_type_id': f'{test_olympiad_types[0].olympiad_type_id}',
                           'subject': 'Math',
                           'level': '1',
                       })
    assert resp.status_code == 200

    base_olympiad: BaseContest = BaseContest.query.filter_by(
        base_contest_id=resp.json['base_contest_id']).one_or_none()
    assert base_olympiad.base_contest_id == resp.json['base_contest_id']


def test_olympiad_create_simple(client, test_base_contests, test_stages):
    from contest.tasks.models import SimpleContest, ContestHoldingTypeEnum, UserStatusEnum
    resp = client.post(f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/create_simple',
                       json={
                           'start_date': f'{datetime.utcnow()}',
                           'end_date': f'{datetime.utcnow() + timedelta(hours=4)}',
                           'regulations': 'Test 0',
                           'end_of_enroll_date': f'{datetime.utcnow() + timedelta(hours=1)}',
                           'deadline_for_appeal': f'{datetime.utcnow() + timedelta(hours=2)}',
                           'result_publication_date': f'{datetime.utcnow() + timedelta(hours=6)}',
                           'show_answer_after_contest': True,
                           'visibility': 'false',
                           'holding_type': f'{ContestHoldingTypeEnum.OfflineContest.value}',
                       })
    assert resp.status_code == 200

    simple_contest: SimpleContest = SimpleContest.query.filter_by(
        contest_id=resp.json['contest_id']).one_or_none()
    assert simple_contest.contest_id == resp.json['contest_id']

    resp = client.post(f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/create_simple',
                       json={
                           'start_date': f'{datetime.utcnow()}',
                           'end_date': f'{datetime.utcnow() + timedelta(hours=4)}',
                           'end_of_enroll_date': f'{datetime.utcnow() + timedelta(hours=1)}',
                           'deadline_for_appeal': f'{datetime.utcnow() + timedelta(hours=2)}',
                           'regulations': 'Test 0',
                           'result_publication_date': f'{datetime.utcnow() + timedelta(hours=6)}',
                           'previous_contest_id': f'{simple_contest.contest_id}',
                           'previous_participation_condition': f'{UserStatusEnum.Winner_1.value}',
                           'show_answer_after_contest': True,
                           'stage_id': '2',
                           'visibility': 'false',
                           'holding_type': f'{ContestHoldingTypeEnum.OfflineContest.value}',
                       })
    assert resp.status_code == 200

    resp = client.post(f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/create_simple',
                       json={
                           'start_date': f'{datetime.utcnow()}',
                           'end_date': f'{datetime.utcnow() + timedelta(hours=4)}',
                           'regulations': 'Test 0',
                           'end_of_enroll_date': f'{datetime.utcnow() + timedelta(hours=1)}',
                           'deadline_for_appeal': f'{datetime.utcnow() + timedelta(hours=2)}',
                           'result_publication_date': f'{datetime.utcnow() + timedelta(hours=6)}',
                           'show_answer_after_contest': True,
                           'previous_contest_id': f'{simple_contest.contest_id}',
                           'stage_id': '2',
                           'visibility': 'false',
                           'holding_type': f'{ContestHoldingTypeEnum.OfflineContest.value}',
                       })
    assert resp.status_code == 409


def test_olympiad_create_composite(client, test_base_contests):
    from contest.tasks.models import CompositeContest
    resp = client.post(f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/create_composite',
                       json={
                           'visibility': 'false',
                           'holding_type': 'OfflineContest',
                       })
    assert resp.status_code == 200

    composite_contest: CompositeContest = CompositeContest.query.filter_by(
        contest_id=resp.json['contest_id']).one_or_none()
    assert composite_contest.contest_id == resp.json['contest_id']


def test_stage_create(client, test_contests_composite):
    from contest.tasks.models import StageConditionEnum, \
        Stage
    resp = client.post(f'/olympiad/{test_contests_composite[0].contest_id}/stage/create',
                       json={
                           'stage_name': 'Test name',
                           'stage_num': '0',
                           'this_stage_condition': 'Test 0',
                           'condition': f'{StageConditionEnum.And.value}',
                       })
    assert resp.status_code == 200

    stage: Stage = Stage.query.filter_by(
        stage_id=resp.json['stage_id']).one_or_none()
    assert stage.stage_id == resp.json['stage_id']


def test_stage_create_in_simple(client, test_simple_contest):
    from contest.tasks.models import StageConditionEnum, \
        Stage
    resp = client.post(f'/olympiad/{test_simple_contest[0].contest_id}/stage/create',
                       json={
                           'stage_name': 'Test name',
                           'stage_num': '0',
                           'this_stage_condition': 'Test 0',
                           'condition': f'{StageConditionEnum.And.value}',
                       })
    assert resp.status_code == 409


def test_contests_all(client, test_contests_composite, test_stages, test_simple_contest_in_stage_1):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}/stage/{test_stages[0].stage_id}/contest/all')
    assert resp.status_code == 200
    assert len(test_simple_contest_in_stage_1) - 1 == len(list(resp.json['olympiad_list']))


def test_task_create_plain(client, test_simple_contest, test_create_tasks_pool):
    from contest.tasks.models import PlainTask
    resp = client.post(f'/task_pool/{test_create_tasks_pool[0].task_pool_id}/task/create_plain',
                       json={
                           'name': 'Test name',
                           'recommended_answer': 'Test',
                       })
    assert resp.status_code == 200

    task: PlainTask = PlainTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']


def test_task_create_range(client, test_simple_contest, test_create_tasks_pool):
    from contest.tasks.models import RangeTask
    resp = client.post(
        f'/task_pool/{test_create_tasks_pool[1].task_pool_id}/task/create_range',
        json={
            'name': 'Test name',
            'start_value': '0.1',
            'end_value': '0.8',
        })
    assert resp.status_code == 200

    task: RangeTask = RangeTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']


def test_task_create_multiple(client, test_simple_contest, test_create_tasks_pool):
    from contest.tasks.models import MultipleChoiceTask
    resp = client.post(
        f'/task_pool/{test_create_tasks_pool[2].task_pool_id}/task/create_multiple',
        json={
            'name': 'Test name',
            'answers': [
                {
                    'answer': 'test',
                    'is_right_answer': 'false'
                }
            ]
        })
    assert resp.status_code == 200

    task: MultipleChoiceTask = MultipleChoiceTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']


def test_tasks_pool_get(client, test_create_tasks_pool):
    resp = client.get(f'/base_olympiad/{test_create_tasks_pool[0].base_contest.base_contest_id}'
                      f'/task_pool/all')

    assert resp.status_code == 200
    assert len(test_create_tasks_pool) == len(resp.json['task_pools_list'])


def test_tasks_pool_get_all(client, test_create_tasks_pool):
    resp = client.get(f'/base_olympiad/{test_create_tasks_pool[0].base_contest.base_contest_id}'
                      f'/task_pool/{test_create_tasks_pool[0].task_pool_id}')

    assert resp.status_code == 200
    assert test_create_tasks_pool[0].task_pool_id == resp.json['task_pool_id']


def test_contest_task_create(client, test_simple_contest, test_create_tasks_pool):
    resp = client.post(f'/contest/{test_simple_contest[0].contest_id}/contest_task/create',
                       json={
                           'num': 1,
                           'task_points': 15,
                           'task_pool_ids': [test_create_tasks_pool[0].task_pool_id]
                       })
    assert resp.status_code == 200
    contest_task: ContestTask = ContestTask.query.filter_by(
        contest_task_id=resp.json['contest_task_id']).one_or_none()
    assert contest_task.contest_task_id == resp.json['contest_task_id']


    resp = client.post(f'/contest/{test_simple_contest[0].contest_id}/contest_task/create',
                       json={
                           'num': 2,
                           'task_points': 15,
                           'task_pool_ids': [test_create_tasks_pool[0].task_pool_id]
                       })
    assert resp.status_code == 409


def test_contest_task_get_all(client, test_create_contest_tasks):
    resp = client.get(f'/contest/{test_create_contest_tasks[0].contest.contest_id}'
                      f'/contest_task/all')

    assert resp.status_code == 200
    assert len(test_create_contest_tasks) == len(resp.json['contest_task_list'])


def test_contest_task_pool_get(client, test_create_contest_tasks):
    resp = client.get(f'/contest/{test_create_contest_tasks[0].contest.contest_id}'
                      f'/contest_task/{test_create_contest_tasks[0].contest_task_id}')

    assert resp.status_code == 200
    assert test_create_contest_tasks[0].contest_task_id == resp.json['contest_task_id']


def test_task_get(client, test_simple_contest, test_create_tasks_pool, create_plain_task):
    resp = client.get(f'/task_pool/{test_create_tasks_pool[0].task_pool_id}/task/{create_plain_task[0].task_id}')

    assert resp.status_code == 200
    assert 1 == len(list(resp.response))

    resp = client.get(f'/task_pool/{test_create_tasks_pool[1].task_pool_id}/task/{create_plain_task[0].task_id}')

    assert resp.status_code == 409


def test_task_image(client, test_simple_contest, create_plain_task):
    resp = client.get(f'/task_pool/{create_plain_task[0].task_pool_id}/task/{create_plain_task[0].task_id}/image')

    assert resp.status_code == 404

    from common.media_types import TaskImage
    test_app.io_to_media('TASK', create_plain_task[0], 'image_of_task', io.BytesIO(test_image), TaskImage)
    test_app.db.session.commit()

    resp = client.get(f'/task_pool/{create_plain_task[0].task_pool_id}/task/{create_plain_task[0].task_id}/image')
    assert resp.status_code == 200


def test_task_all(client, test_simple_contest, test_create_tasks_pool):
    resp = client.get(f'/task_pool/{test_create_tasks_pool[0].task_pool_id}/task/all')
    assert resp.status_code == 200
    assert len(test_create_tasks_pool[0].tasks.all()) == len(list(resp.json['tasks_list']))
