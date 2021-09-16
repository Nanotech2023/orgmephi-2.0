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
                           'end_of_enroll_date': f'{datetime.utcnow() + timedelta(hours=1)}',
                           'result_publication_date': f'{datetime.utcnow() + timedelta(hours=6)}',
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
                           'result_publication_date': f'{datetime.utcnow() + timedelta(hours=6)}',
                           'previous_contest_id': f'{simple_contest.contest_id}',
                           'previous_participation_condition': f'{UserStatusEnum.Winner_1.value}',
                           'stage_id': '2',
                           'visibility': 'false',
                           'holding_type': f'{ContestHoldingTypeEnum.OfflineContest.value}',
                       })
    assert resp.status_code == 200

    resp = client.post(f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/create_simple',
                       json={
                           'start_date': f'{datetime.utcnow()}',
                           'end_date': f'{datetime.utcnow() + timedelta(hours=4)}',
                           'end_of_enroll_date': f'{datetime.utcnow() + timedelta(hours=1)}',
                           'result_publication_date': f'{datetime.utcnow() + timedelta(hours=6)}',
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


def test_variant_create(client, test_simple_contest):
    from contest.tasks.models import Variant
    resp = client.post(f'/contest/{test_simple_contest[0].contest_id}/variant/create',
                       json={
                           'variant_description': 'Test',
                       })
    assert resp.status_code == 200

    variant: Variant = Variant.query.filter_by(
        variant_id=resp.json['variant_id']).one_or_none()

    assert variant.variant_id == resp.json['variant_id']

    resp = client.post(f'/contest/{test_simple_contest[0].contest_id}/variant/create',
                       json={
                           'variant_description': 'Test',
                       })
    assert resp.status_code == 200


def test_variant_get(client, test_simple_contest, test_variant):
    resp = client.get(f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_number}')
    assert resp.status_code == 200
    assert 1 == len(list(resp.response))

    resp = client.get(f'/contest/{test_simple_contest[1].contest_id}/variant/{test_variant[0].variant_number}')
    assert resp.status_code == 409


def test_variant_all(client, test_simple_contest, test_variant):
    resp = client.get(f'/contest/{test_simple_contest[0].contest_id}/variant/all')
    assert resp.status_code == 200
    assert len(test_simple_contest[0].variants.all()) == len(list(resp.json['variants_list']))


def test_task_create_plain(client, test_simple_contest, test_variant):
    from contest.tasks.models import PlainTask
    resp = client.post(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_id}/task/create_plain',
        json={
            'num_of_task': '0',
            'recommended_answer': 'Test',
            'show_answer_after_contest': 'false',
            'task_points': '10',
        })
    assert resp.status_code == 200

    task: PlainTask = PlainTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']


def test_task_create_range(client, test_simple_contest, test_variant):
    from contest.tasks.models import RangeTask
    resp = client.post(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_id}/task/create_range',
        json={
            'num_of_task': '0',
            'start_value': '0.1',
            'end_value': '0.8',
            'show_answer_after_contest': 'false',
            'task_points': '10',
        })
    assert resp.status_code == 200

    task: RangeTask = RangeTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']


def test_task_create_multiple(client, test_simple_contest, test_variant):
    from contest.tasks.models import MultipleChoiceTask
    resp = client.post(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_id}/task/create_multiple',
        json={
            'num_of_task': '0',
            'answers': [
                {
                    'answer': 'test',
                    'is_right_answer': 'false'
                }
            ],
            'show_answer_after_contest': 'false',
            'task_points': '10',
        })
    assert resp.status_code == 200

    task: MultipleChoiceTask = MultipleChoiceTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']


def test_task_get(client, test_simple_contest, test_variant, create_plain_task):
    resp = client.get(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_id}'
        f'/task/{create_plain_task[0].task_id}')

    assert resp.status_code == 200
    assert 1 == len(list(resp.response))

    resp = client.get(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[1].variant_id}'
        f'/task/{create_plain_task[0].task_id}')

    assert resp.status_code == 409


def test_task_image(client, test_simple_contest, test_variant, create_plain_task):
    resp = client.get(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_id}'
        f'/tasks/{create_plain_task[0].task_id}/image')

    assert resp.status_code == 409

    create_plain_task[0].image_of_task = b'Test'
    resp = client.get(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_id}'
        f'/tasks/{create_plain_task[0].task_id}/image')

    assert resp.status_code == 200


def test_task_all(client, test_simple_contest, test_variant):
    resp = client.get(
        f'/contest/{test_simple_contest[0].contest_id}/variant/{test_variant[0].variant_id}'
        f'/task/all')
    assert resp.status_code == 200
    assert len(test_variant[0].tasks) == len(list(resp.json['tasks_list']))