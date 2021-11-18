from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('contest/tasks/editor')
    yield client_creator


# Base olympiad


def test_base_olympiad_remove(client, test_base_contests):
    from contest.tasks.models import BaseContest
    test_base_contests: BaseContest = test_base_contests[1]
    resp = client.post(f'/base_olympiad/{test_base_contests.base_contest_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        BaseContest.query.filter_by(base_contest_id=f'{test_base_contests.base_contest_id}').exists()
    ).scalar()


def test_base_olympiad_patch(client, test_base_contests, test_olympiad_types):
    from contest.tasks.models import BaseContest, OlympiadSubjectEnum
    resp = client.patch(f'/base_olympiad/{test_base_contests[0].base_contest_id}',
                        json={
                            'name': 'Test 0',
                            'description': 'Test 0',
                            'rules': 'Test 8',
                            'winner_1_condition': '0.8',
                            'winner_2_condition': '0.8',
                            'winner_3_condition': '0.8',
                            'diploma_1_condition': '0.8',
                            'diploma_2_condition': '0.8',
                            'diploma_3_condition': '0.8',
                            'olympiad_type_id': f'{test_olympiad_types[0].olympiad_type_id}',
                            'subject': 'Physics',
                            'level': '2',
                        })
    assert resp.status_code == 200

    base_olympiad: BaseContest = BaseContest.query.filter_by(
        base_contest_id=resp.json['base_contest_id']).one_or_none()
    assert base_olympiad.base_contest_id == resp.json['base_contest_id']
    assert base_olympiad.winner_1_condition == 0.8
    assert base_olympiad.winner_2_condition == 0.8
    assert base_olympiad.winner_3_condition == 0.8
    assert base_olympiad.diploma_1_condition == 0.8
    assert base_olympiad.diploma_2_condition == 0.8
    assert base_olympiad.diploma_3_condition == 0.8
    assert base_olympiad.rules == "Test 8"
    assert base_olympiad.subject == OlympiadSubjectEnum.Physics


# Olympiad

# noinspection DuplicatedCode
def test_olympiad_remove(client, test_base_contests, test_contests):
    from contest.tasks.models import Contest
    test_contests: Contest = test_contests[1]
    resp = client.post(
        f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/{test_contests.contest_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        Contest.query.filter_by(contest_id=f'{test_contests.contest_id}').exists()
    ).scalar()


# noinspection DuplicatedCode
def test_olympiad_patch(client, test_base_contests, test_simple_contest, test_contests_composite):
    from contest.tasks.models import SimpleContest, ContestHoldingTypeEnum, CompositeContest
    new_start_date = datetime.utcnow()
    new_end_date = datetime.utcnow() + timedelta(hours=4)
    new_end_of_enroll_date = datetime.utcnow() + timedelta(hours=1)
    new_deadline_for_appeal = datetime.utcnow() + timedelta(hours=4)
    new_result_publication_date = datetime.utcnow() + timedelta(hours=6)
    resp = client.patch(
        f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/{test_simple_contest[0].contest_id}',
        json={
            'start_date': f'{new_start_date}',
            'end_date': f'{new_end_date}',
            'regulations': 'Test 0',
            'end_of_enroll_date': f'{new_end_of_enroll_date}',
            'deadline_for_appeal': f'{new_deadline_for_appeal}',
            'result_publication_date': f'{new_result_publication_date}',
            'visibility': 'true',
            'holding_type': f'{ContestHoldingTypeEnum.OfflineContest.value}',
        })
    assert resp.status_code == 200

    simple_contest: SimpleContest = SimpleContest.query.filter_by(
        contest_id=resp.json['contest_id']).one_or_none()
    assert simple_contest.contest_id == resp.json['contest_id']

    assert simple_contest.start_date == new_start_date
    assert simple_contest.end_date == new_end_date
    assert simple_contest.end_of_enroll_date == new_end_of_enroll_date
    assert simple_contest.deadline_for_appeal == new_deadline_for_appeal
    assert simple_contest.result_publication_date == new_result_publication_date

    resp = client.patch(
        f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/{test_contests_composite[0].contest_id}',
        json={
            'visibility': 'true',
            'holding_type': 'OfflineContest',
        })
    assert resp.status_code == 200

    composite_contest: CompositeContest = CompositeContest.query.filter_by(
        contest_id=resp.json['contest_id']).one_or_none()
    assert composite_contest.contest_id == resp.json['contest_id']


# Stage

# noinspection DuplicatedCode
def test_stage_remove(client, test_contests_composite, test_stages):
    from contest.tasks.models import Stage
    test_stages: Stage = test_stages[1]
    resp = client.post(f'/olympiad/{test_contests_composite[0].contest_id}/stage/{test_stages.stage_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        Stage.query.filter_by(stage_id=f'{test_stages.stage_id}').exists()
    ).scalar()


def test_stage_patch(client, test_contests_composite, test_stages):
    from contest.tasks.models import StageConditionEnum, \
        Stage
    resp = client.patch(f'/olympiad/{test_contests_composite[0].contest_id}/stage/{test_stages[0].stage_id}',
                        json={
                            'stage_name': 'Test name2',
                            'stage_num': '42',
                            'this_stage_condition': 'Test 2',
                            'condition': f'{StageConditionEnum.And.value}',
                        })
    assert resp.status_code == 200

    stage: Stage = Stage.query.filter_by(
        stage_id=resp.json['stage_id']).one_or_none()
    assert stage.stage_id == resp.json['stage_id']
    assert stage.stage_num == 42
    assert stage.stage_name == 'Test name2'
    assert stage.this_stage_condition == 'Test 2'


# Inner contest


# noinspection DuplicatedCode
def test_contest_remove(client, test_contests_composite, test_stages, test_simple_contest_in_stage_1):
    from contest.tasks.models import SimpleContest
    test_contest: SimpleContest = test_simple_contest_in_stage_1[1]
    resp = client.post(
        f'/olympiad/{test_contests_composite[0].contest_id}/stage/{test_stages[0].stage_id}'
        f'/contest/{test_contest.contest_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        SimpleContest.query.filter_by(contest_id=f'{test_contest.contest_id}').exists()
    ).scalar()

    resp = client.post(
        f'/olympiad/{test_contests_composite[1].contest_id}/stage/{test_stages[0].stage_id}'
        f'/contest/{test_contest.contest_id}/remove')
    assert resp.status_code == 409

    resp = client.post(
        f'/olympiad/{test_contests_composite[0].contest_id}/stage/{test_stages[0].stage_id}'
        f'/contest/{test_simple_contest_in_stage_1[2].contest_id}/remove')
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_contest_add_previous(client, test_contests_composite, test_stages, test_simple_contest_in_stage_1):
    from contest.tasks.models import UserStatusEnum
    resp = client.patch(
        f'/olympiad/{test_contests_composite[0].contest_id}/stage/{test_stages[0].stage_id}'
        f'/contest/{test_simple_contest_in_stage_1[1].contest_id}/add_previous',
        json={
            'previous_contest_id': f'{test_simple_contest_in_stage_1[0].contest_id}',
            'previous_participation_condition': f'{UserStatusEnum.Participant.value}',
        })
    assert resp.status_code == 200


# Variant

# Task


def test_task_image_upload(client, test_simple_contest, create_plain_task):
    resp = client.post(f'/task_pool/{create_plain_task[0].task_pool_id}'
                       f'/task/{create_plain_task[0].task_id}/upload_image',
                       data=test_image)
    assert resp.status_code == 200


def test_task_pool_patch(client, test_create_tasks_pool):
    from contest.tasks.models import TaskPool
    task_pool: TaskPool = test_create_tasks_pool[0]
    resp = client.patch(f'/base_olympiad/{test_create_tasks_pool[0].base_contest.base_contest_id}'
                        f'/task_pool/{task_pool.task_pool_id}',
                        json={
                            'name': "renamed"
                        })
    assert resp.status_code == 200
    task_pool: TaskPool = TaskPool.query.filter_by(
        task_pool_id=task_pool.task_pool_id).one_or_none()
    assert task_pool.name == "renamed"


def test_task_pool_remove(client, test_create_tasks_pool):
    from contest.tasks.models import TaskPool
    task_pool: TaskPool = test_create_tasks_pool[0]
    resp = client.post(f'/base_olympiad/{test_create_tasks_pool[0].base_contest.base_contest_id}'
                       f'/task_pool/{task_pool.task_pool_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        TaskPool.query.filter_by(task_pool_id=f'{task_pool.task_pool_id}').exists()
    ).scalar()


def test_contest_task_patch(client, test_create_contest_tasks):
    from contest.tasks.models import ContestTask
    resp = client.patch(f'/contest/{test_create_contest_tasks[0].contest.contest_id}'
                        f'/contest_task/{test_create_contest_tasks[0].contest_task_id}',
                        json={
                            'num': 20
                        })
    print(resp.data)
    assert resp.status_code == 200
    contest_task: ContestTask = ContestTask.query.filter_by(
        contest_task_id=test_create_contest_tasks[0].contest_task_id).one_or_none()
    assert contest_task.num == 20


def test_contest_task_remove(client, test_create_contest_tasks):
    from contest.tasks.models import ContestTask
    contest_task: ContestTask = test_create_contest_tasks[0]
    resp = client.post(f'/contest/{test_create_contest_tasks[0].contest.contest_id}'
                       f'/contest_task/{test_create_contest_tasks[0].contest_task_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        ContestTask.query.filter_by(contest_task_id=f'{contest_task.contest_task_id}').exists()
    ).scalar()


def test_task_remove(client, test_simple_contest, create_plain_task):
    from contest.tasks.models import Task
    task: Task = create_plain_task[1]
    resp = client.post(f'/task_pool/{create_plain_task[0].task_pool_id}'
                       f'/task/{task.task_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        Task.query.filter_by(task_id=f'{task.task_id}').exists()
    ).scalar()


def test_task_patch_plain(client, test_simple_contest, create_plain_task):
    from contest.tasks.models import PlainTask
    resp = client.patch(
        f'/task_pool/{create_plain_task[0].task_pool_id}'
        f'/task/{create_plain_task[0].task_id}/plain',
        json={
            'recommended_answer': 'TestTest',
        })
    assert resp.status_code == 200

    task: PlainTask = PlainTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']
    assert task.recommended_answer == "TestTest"


def test_task_patch_range(client, test_simple_contest, create_range_task):
    from contest.tasks.models import RangeTask
    resp = client.patch(
        f'/task_pool/{create_range_task[0].task_pool_id}'
        f'/task/{create_range_task[0].task_id}/range',
        json={
            'start_value': '0.2',
            'end_value': '0.9'
        })
    assert resp.status_code == 200

    task: RangeTask = RangeTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']
    assert task.start_value == 0.2
    assert task.end_value == 0.9


def test_task_patch_multiple(client, test_simple_contest, create_multiple_task):
    from contest.tasks.models import MultipleChoiceTask
    resp = client.patch(
        f'/task_pool/{create_multiple_task[0].task_pool_id}'
        f'/task/{create_multiple_task[0].task_id}/multiple',
        json={
            'answers': [
                {
                    'answer': 'test',
                    'is_right_answer': 'false'
                },
                {
                    'answer': 'test2',
                    'is_right_answer': 'false'
                }
            ]
        })
    assert resp.status_code == 200

    task: MultipleChoiceTask = MultipleChoiceTask.query.filter_by(
        task_id=resp.json['task_id']).one_or_none()
    assert task.task_id == resp.json['task_id']
    assert len(task.answers) == 2


# Location


# noinspection DuplicatedCode
def test_add_locations_to_contest(client, test_simple_contest, test_olympiad_locations):
    resp = client.post(
        f'/contest/{test_simple_contest[0].contest_id}/add_location',
        json={
            'locations': [f'{test_olympiad_locations[0].location_id}',
                          f'{test_olympiad_locations[1].location_id}']
        })
    assert resp.status_code == 200
    assert len(test_simple_contest[0].locations) == 2


def test_remove_locations_from_contest(client, test_simple_contest_with_location, test_olympiad_locations):
    resp = client.post(
        f'/contest/{test_simple_contest_with_location[0].contest_id}/remove_location',
        json={
            'locations': [f'{test_olympiad_locations[0].location_id}']
        })
    assert resp.status_code == 200

    resp = client.post(
        f'/contest/{test_simple_contest_with_location[0].contest_id}/remove_location',
        json={
            'locations': [f'{test_olympiad_locations[0].location_id}']
        })
    assert resp.status_code == 404


# Target classes


def test_add_target_classes_to_contest(client, test_base_contests, test_target_class):
    resp = client.post(
        f'/base_olympiad/{test_base_contests[0].base_contest_id}/add_target_classes',
        json={
            'target_classes_ids': [f'{test_target_class[0].target_class_id}',
                                   f'{test_target_class[1].target_class_id}']
        })
    assert resp.status_code == 200
    assert len(test_base_contests[0].target_classes) == 2


def test_remove_target_classes_from_contest(client, test_base_contests_with_target, test_target_class):
    resp = client.post(
        f'/base_olympiad/{test_base_contests_with_target[0].base_contest_id}/remove_target_classes',
        json={
            'target_classes_ids': [f'{test_target_class[0].target_class_id}']
        })
    assert resp.status_code == 200
    resp = client.post(
        f'/base_olympiad/{test_base_contests_with_target[0].base_contest_id}/remove_target_classes',
        json={
            'target_classes_ids': [f'{test_target_class[0].target_class_id}']
        })
    assert resp.status_code == 404


def cmp_certs(cert_type_obj, cert_type_json):
    assert cert_type_json['name'] == cert_type_obj.name
    assert cert_type_json['description'] == cert_type_obj.description
    json_dict = {v['certificate_id']: v['certificate_category'] for v in cert_type_json['certificates']}
    obj_dict = {v.certificate_id: v.certificate_category.value for v in cert_type_obj.certificates}
    assert json_dict == obj_dict


def test_get_certificate_types(client, test_certificate_type):
    resp = client.get('/certificate_type')
    assert resp.status_code == 200
    assert len(resp.json['certificate_types']) == 1
    resp_cert_type = resp.json['certificate_types'][0]
    cmp_certs(test_certificate_type, resp_cert_type)


def test_get_certificate_type_by_id(client, test_certificate_type):
    resp = client.get(f'/certificate_type/{test_certificate_type.certificate_type_id}')
    assert resp.status_code == 200
    cmp_certs(test_certificate_type, resp.json)


def test_get_certificate_by_id(client, test_certificate_type):
    cert = test_certificate_type.certificates[0]
    resp = client.get(f'/certificate/{cert.certificate_id}')
    assert resp.status_code == 200
    assert resp.json['certificate_id'] == cert.certificate_id
    assert resp.json['certificate_type_id'] == cert.certificate_type_id
    assert resp.json['certificate_category'] == cert.certificate_category.value
    assert resp.json['text_x'] == cert.text_x
    assert resp.json['text_y'] == cert.text_y
    assert resp.json['text_width'] == cert.text_width
    assert resp.json['text_size'] == cert.text_size
    assert resp.json['text_style'] == cert.text_style
    assert resp.json['text_spacing'] == cert.text_spacing
    assert resp.json['text_color'] == cert.text_color


def test_get_certificate_image(client, test_certificate_type):
    cert = test_certificate_type.certificates[0]
    resp = client.get(f'/certificate/{cert.certificate_id}/image')
    assert resp.status_code == 200
    assert resp.data
