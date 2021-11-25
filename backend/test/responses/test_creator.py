from . import *

DEFAULT_INDEX = 0
ERROR_ID = 1500


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('contest/responses/creator')
    yield client_creator


@pytest.fixture
def client_tasks(client_creator):
    client_creator.set_prefix('contest/tasks/creator')
    yield client_creator


@pytest.fixture
def client_admin_response(client_admin):
    client_admin.set_prefix('contest/responses/creator')
    yield client_admin


def test_user_response_creator(client_admin_response, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_three_tasks, DEFAULT_INDEX)

    resp = client_admin_response.post(f'/contest/{contest_id}/user/{ERROR_ID}/create')
    assert resp.status_code == 409

    resp = client_admin_response.post(f'/contest/{ERROR_ID}/user/{user_id}/create')
    assert resp.status_code == 409

    resp = client_admin_response.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 200

    resp = client_admin_response.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    response = get_user_in_contest_work(user_id, contest_id)
    assert response.work_status.value == 'InProgress'


def test_creator_create_response(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_three_tasks, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 403


# noinspection DuplicatedCode
def test_plain_task_text_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum, PlainTask, TaskAnswerTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)
    from common.util import db_get_one_or_none
    task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', task_id)
    task.answer_type = TaskAnswerTypeEnum.Text
    wrong_task_id = 1 if task_id + 1 > 8 else task_id + 1
    task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', wrong_task_id)
    task.answer_type = TaskAnswerTypeEnum.Text
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{wrong_task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 'answer' == answer.answer_text

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    range_task_id = get_range_task_id(create_user_response, DEFAULT_INDEX)
    resp = client.post(f'/contest/{contest_id}/task/{range_task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'PlainAnswerText'
    assert resp.json['answer_text'] == 'answer'


# noinspection DuplicatedCode
def test_get_variant_by_number(client_tasks, create_user_response):
    index = 1
    contest_id = get_contest_id(create_user_response, index)
    user_id = get_user_id(create_user_response, index)
    variant = get_variant_by_num(contest_id, user_id)
    resp = client_tasks.get(f'/contest/{contest_id}/variant/{variant.variant_number}', data=test_image)
    assert resp.status_code == 200
    assert resp.json['variant_id'] == variant.variant_id

    resp = client_tasks.get(f'/contest/{contest_id}/variant/{variant.variant_number + 1}', data=test_image)
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_get_variants_all(client_tasks, create_user_response):
    index = 1
    contest_id = get_contest_id(create_user_response, index)
    from contest.tasks.models.olympiad import SimpleContest
    from common.util import db_get_one_or_none
    contest: SimpleContest = db_get_one_or_none(SimpleContest, 'contest_id', contest_id)
    user_id = get_user_id(create_user_response, index)
    resp = client_tasks.get(f'/contest/{contest_id}/variant/all')
    assert resp.status_code == 200
    assert len(resp.json['variants_list']) == len(contest.variants.all())


# noinspection DuplicatedCode
def test_plain_task_file_creator(client, create_user_response):
    index = 1
    contest_id = get_contest_id(create_user_response, index)
    user_id = get_user_id(create_user_response, index)
    from contest.tasks.models.tasks import TaskTypeEnum, PlainTask, TaskAnswerTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)
    from common.util import db_get_one_or_none
    task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', task_id)
    task.answer_type = TaskAnswerTypeEnum.File
    wrong_task_id = 1 if task_id + 1 > 8 else task_id + 1
    task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', wrong_task_id)
    task.answer_type = TaskAnswerTypeEnum.File
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{wrong_task_id}/user/{user_id}/jpeg', data=test_image)
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/jpeg', data=test_image)
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    assert user_answer.filetype == 'image/jpeg'


# noinspection DuplicatedCode
def test_plain_task_file_failed(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum, PlainTask, TaskAnswerTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)
    from common.util import db_get_one_or_none
    task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', task_id)
    task.answer_type = TaskAnswerTypeEnum.Text
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/png', data=test_image)
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_plain_task_get_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, 1)
    user_id = get_user_id(create_user_response, 1)
    from contest.tasks.models.tasks import TaskTypeEnum, PlainTask, TaskAnswerTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)
    from common.util import db_get_one_or_none
    task: PlainTask = db_get_one_or_none(PlainTask, 'task_id', task_id)
    task.answer_type = TaskAnswerTypeEnum.File
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain/file', data=test_image)
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['filetype'] == 'image/jpeg'

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain/file')
    assert resp.status_code == 200
    assert resp.content_type == 'image/jpeg'


def test_range_task_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.RangeTask)
    wrong_task_id = 9 if task_id + 1 > 16 else task_id + 1

    resp = client.post(f'/contest/{contest_id}/task/{wrong_task_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 0.6 == answer.answer

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_user_response, DEFAULT_INDEX)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'RangeAnswer'
    assert resp.json['answer'] == 0.6


def test_multiple_task_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.MultipleChoiceTask)
    wrong_task_id = 17 if task_id + 1 > 24 else task_id + 1

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "4"}]})
    assert resp.status_code == 409

    resp = client.post(f'/contest/{contest_id}/task/{wrong_task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert '1' in answer.answers
    assert '3' in answer.answers

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    plain_task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'MultipleChoiceAnswer'
    assert '1' in resp.json['answers']
    assert '3' in resp.json['answers']


def test_get_status_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/status')
    assert resp.status_code == 200
    assert resp.json['status'] == 'InProgress'


def test_set_status_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/status',
                       json={'status': 'NotChecked'})
    assert resp.status_code == 200

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NotChecked'

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/status',
                       json={'status': '333'})
    assert resp.status_code == 400


def test_mark_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)
    error_task_id = 100

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['mark'] == 0

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark',
                       json={'mark': 15})
    assert resp.status_code == 409

    resp = client.post(f'/contest/{contest_id}/task/{error_task_id}/user/{user_id}/mark',
                       json={'mark': 11})
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark',
                       json={'mark': 11})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert answer.mark == 11

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['mark'] == 11

    from contest.tasks.util import get_simple_contest_if_possible
    simple_contest = get_simple_contest_if_possible(contest_id)
    simple_contest.deadline_for_appeal = datetime.utcnow() - timedelta(minutes=15)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark',
                       json={'mark': 12})
    assert resp.status_code == 409


def test_admin_mark_creator(client_admin_response, create_user_with_answers):
    contest_id = get_contest_id(create_user_with_answers, DEFAULT_INDEX)
    user_id = get_user_id(create_user_with_answers, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)

    resp = client_admin_response.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark',
                                      json={'mark': 11})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert answer.mark == 11

    from contest.tasks.util import get_simple_contest_if_possible
    simple_contest = get_simple_contest_if_possible(contest_id)
    simple_contest.deadline_for_appeal = datetime.utcnow() - timedelta(minutes=15)
    test_app.db.session.commit()

    resp = client_admin_response.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark',
                                      json={'mark': 12})
    assert resp.status_code == 200


def test_time_left_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)

    resp = client.get(f'/contest/{1000}/user/{user_id}/time')
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/time')
    assert resp.status_code == 200
    assert resp.json['time'] < 1800


def test_time_extend_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/time/extra',
                       json={'time': 1800})
    assert resp.status_code == 200

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.time_extension == timedelta(seconds=1800)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/time')
    assert resp.status_code == 200
    assert resp.json['time'] > 1800

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/time/extra')
    assert resp.status_code == 200
    assert resp.json['time'] == 1800


def test_finish_contest_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/finish')
    assert resp.status_code == 200

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NotChecked'

    from contest.tasks.models.user import UserInContest
    user_in_contest: UserInContest = UserInContest.query.filter_by(contest_id=user_work.contest_id,
                                                                   user_id=user_work.user_id).one_or_none()
    assert user_in_contest.completed_the_contest == 1


# noinspection DuplicatedCode
def test_all_answers_creator(client, create_user_with_answers):
    contest_id = get_contest_id(create_user_with_answers, DEFAULT_INDEX)
    user_id = get_user_id(create_user_with_answers, DEFAULT_INDEX)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/response')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    assert len(resp.json['user_answers']) == 3


def test_get_contest_list_creator(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum
    plain_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/list')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert len(resp.json['user_row']) == 1
    assert resp.json['user_row'][0]['mark'] == 0
    assert resp.json['user_row'][0]['user_id'] == user_id


# noinspection DuplicatedCode
def test_auto_check_creator(client, create_user_with_answers):
    contest_id = get_contest_id(create_user_with_answers, DEFAULT_INDEX)
    user_id = get_user_id(create_user_with_answers, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum
    plain_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.PlainTask)
    range_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.RangeTask)
    multiple_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.MultipleChoiceTask)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/finish')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/check')
    assert resp.status_code == 409

    contest = create_user_with_answers['contests'][DEFAULT_INDEX]
    from contest.tasks.models.olympiad import ContestHoldingTypeEnum
    contest.holding_type = ContestHoldingTypeEnum.OfflineContest
    resp = client.post(f'/contest/{contest_id}/check')
    assert resp.status_code == 409
    contest.holding_type = ContestHoldingTypeEnum.OnLineContest

    contest.end_date = datetime.utcnow() - timedelta(minutes=5)
    resp = client.post(f'/contest/{contest_id}/check')
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get, get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NotChecked'
    plain_answer = user_answer_get(user_id, contest_id, plain_id)
    assert plain_answer.mark == 0
    range_answer = user_answer_get(user_id, contest_id, range_id)
    assert range_answer.mark == 14
    multiple_answer = user_answer_get(user_id, contest_id, multiple_id)
    assert multiple_answer.mark == 0

    from contest.tasks.util import get_user_in_contest_by_id_if_possible
    user_in_contest = get_user_in_contest_by_id_if_possible(contest_id, user_id)
    user_in_contest.show_results_to_user = False
    test_app.db.session.commit()

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    user_answers = resp.json['user_answers']
    assert len(user_answers) == 3

    for answer in user_answers:
        if answer['answer_type'] == 'PlainAnswerText':
            assert answer['mark'] == 0
            assert answer['task_points'] == 14
            assert answer['task_id'] == plain_id
            assert answer['right_answer']['answer'] == 'answer'
        elif answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 14
            assert answer['task_points'] == 14
            assert answer['task_id'] == range_id
            assert answer['right_answer']['start_value'] == 0.5
            assert answer['right_answer']['end_value'] == 0.7
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 0
            assert answer['task_points'] == 14
            assert answer['task_id'] == multiple_id
            assert answer['right_answer']['answers'] == ['1', '3']

    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 409

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/{user_id}/mark',
                       json={'mark': 12})
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/status',
                       json={'status': 'Accepted'})
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200

    from contest.tasks.models.user import UserInContest, UserStatusEnum
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Diploma_2

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/mark',
                       json={'mark': 0})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Participant

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/mark',
                       json={'mark': 10})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Diploma_3

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/mark',
                       json={'mark': 14})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 4})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Diploma_1

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/{user_id}/mark',
                       json={'mark': 14})
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 6})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Winner_3

    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 10})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Winner_2

    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 14})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Winner_1

    resp = client.get(f'/contest/user/{user_id}/results')
    assert resp.status_code == 200

    results = resp.json['results']
    contest = results[0]['contest_info']
    assert len(results) == 8
    assert contest['subject'] == 'Math'

    academic_year = datetime.utcnow().year - 1 if datetime.utcnow().month < 9 else datetime.utcnow().year
    assert contest['academic_year'] == academic_year
    assert results[0]['status'] == 'NoResults'
    assert results[0]['mark'] == 42
    assert results[0]['user_status'] == 'Winner 1'


# noinspection DuplicatedCode
def test_auto_check_status(client, create_user_response):
    contest_id = get_contest_id(create_user_response, DEFAULT_INDEX)
    user_id = get_user_id(create_user_response, DEFAULT_INDEX)
    from contest.tasks.models.tasks import TaskTypeEnum
    range_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.RangeTask)
    multiple_id = get_task_id_by_variant_and_type(contest_id, user_id, TaskTypeEnum.MultipleChoiceTask)

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "2"}]})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/user/{user_id}/finish')
    assert resp.status_code == 200

    contest = create_user_response['contests'][DEFAULT_INDEX]
    from contest.tasks.models.olympiad import ContestHoldingTypeEnum
    contest.holding_type = ContestHoldingTypeEnum.OfflineContest
    contest.holding_type = ContestHoldingTypeEnum.OnLineContest
    contest.end_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()
    resp = client.post(f'/contest/{contest_id}/check')
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get, get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NoResults'
    assert user_work.work_status.value == 'Accepted'
    range_answer = user_answer_get(user_id, contest_id, range_id)
    assert range_answer.mark == 14
    multiple_answer = user_answer_get(user_id, contest_id, multiple_id)
    assert multiple_answer.mark == 0

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    user_answers = resp.json['user_answers']
    assert len(user_answers) == 2

    for answer in user_answers:
        if answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 14
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 0


def test_user_results_without_response(client, create_three_tasks):
    user_id = get_user_id(create_three_tasks, DEFAULT_INDEX)

    resp = client.get(f'/contest/user/{user_id}/results')
    assert resp.status_code == 200
    results = resp.json['results']
    assert results[0]['status'] == 'InProgress'
    assert results[0]['mark'] == 0
    assert results[0]['user_status'] == 'Participant'


# noinspection DuplicatedCode
def test_group_restrictions(client, create_user_with_answers):
    contest_id = get_contest_id(create_user_with_answers, 0)
    test_user_id = get_user_id(create_user_with_answers, 0)
    client.set_prefix('user/profile')

    resp = client.get('/user')
    assert resp.status_code == 200
    user_id = resp.json['id']

    from user.models import Group, User
    from common.util import db_get_one_or_none
    test_group = db_get_one_or_none(Group, 'name', 'Test Group')
    user = db_get_one_or_none(User, 'id', user_id)
    test_group.users.append(user)
    test_app.db.session.commit()

    client.set_prefix('contest/tasks/creator')

    resp = client.get(f'/contest/{contest_id}/restrictions')
    assert resp.status_code == 200
    restrictions = resp.json['restrictions']
    assert restrictions[0]['group_name'] == 'Everyone'
    assert restrictions[0]['restriction'] == 'EditUserStatus'

    restrictions = [
        {
            'group_name': 'Test Group',
            'restriction': 'ViewMarkAndUserStatus'
        },
        {
            'group_name': 'Everyone',
            'restriction': 'ViewMarkAndUserStatus'
        }
    ]

    resp = client.put(f'/contest/{contest_id}/restrictions',
                      json={'restrictions': restrictions})
    assert resp.status_code == 200

    client.set_prefix('contest/responses/creator')
    resp = client.get(f'/contest/{contest_id}/user/{test_user_id}/status')
    assert resp.status_code == 200
    resp = client.get(f'/contest/{contest_id}/user/{test_user_id}/response')
    assert resp.status_code == 403

    client.set_prefix('contest/tasks/creator')
    restrictions = [
        {
            'group_name': 'Test Group',
            'restriction': 'ViewResponse'
        }
    ]

    resp = client.put(f'/contest/{contest_id}/restrictions',
                      json={'restrictions': restrictions})
    assert resp.status_code == 200

    client.set_prefix('contest/responses/creator')
    resp = client.get(f'/contest/{contest_id}/user/{test_user_id}/response')
    assert resp.status_code == 200

    from contest.tasks.models.tasks import TaskTypeEnum
    task_id = get_task_id_by_variant_and_type(contest_id, test_user_id, TaskTypeEnum.RangeTask)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{test_user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 403
    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{test_user_id}/mark',
                       json={'mark': 11})
    assert resp.status_code == 403

    client.set_prefix('contest/tasks/creator')
    restrictions = [
        {
            'group_name': 'Test Group',
            'restriction': 'EditUserStatus'
        }
    ]

    resp = client.put(f'/contest/{contest_id}/restrictions',
                      json={'restrictions': restrictions})
    assert resp.status_code == 200

    client.set_prefix('contest/responses/creator')
    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{test_user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/user/{test_user_id}/status',
                       json={'status': 'NotChecked'})
    assert resp.status_code == 200

    client.set_prefix('contest/tasks/creator')
    restrictions = [
        {
            'group_name': 'Test Group',
            'restriction': 'EditMark'
        }
    ]

    resp = client.put(f'/contest/{contest_id}/restrictions',
                      json={'restrictions': restrictions})
    assert resp.status_code == 200

    client.set_prefix('contest/responses/creator')
    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{test_user_id}/mark',
                       json={'mark': 11})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/user/{test_user_id}/status',
                       json={'status': 'NotChecked'})
    assert resp.status_code == 403


# noinspection DuplicatedCode
def test_admin_group_restrictions(client_admin_response, create_user_with_answers):
    contest_id = get_contest_id(create_user_with_answers, 0)
    test_user_id = get_user_id(create_user_with_answers, 0)
    client_admin_response.set_prefix('user/profile')

    resp = client_admin_response.get('/user')
    assert resp.status_code == 200
    user_id = resp.json['id']

    from user.models import Group, User
    from common.util import db_get_one_or_none
    test_group = db_get_one_or_none(Group, 'name', 'Test Group')
    user = db_get_one_or_none(User, 'id', user_id)
    test_group.users.append(user)
    test_app.db.session.commit()

    client_admin_response.set_prefix('contest/tasks/creator')

    resp = client_admin_response.get(f'/contest/{contest_id}/restrictions')
    assert resp.status_code == 200
    restrictions = resp.json['restrictions']
    assert restrictions[0]['group_name'] == 'Everyone'
    assert restrictions[0]['restriction'] == 'EditUserStatus'

    restrictions = [
        {
            'group_name': 'Test Group',
            'restriction': 'ViewMarkAndUserStatus'
        },
        {
            'group_name': 'Everyone',
            'restriction': 'ViewMarkAndUserStatus'
        }
    ]

    resp = client_admin_response.put(f'/contest/{contest_id}/restrictions',
                                     json={'restrictions': restrictions})
    assert resp.status_code == 200

    client_admin_response.set_prefix('contest/responses/creator')
    resp = client_admin_response.get(f'/contest/{contest_id}/user/{test_user_id}/status')
    assert resp.status_code == 200
    resp = client_admin_response.get(f'/contest/{contest_id}/user/{test_user_id}/response')
    assert resp.status_code == 200


def test_contest_properties(client, create_user_with_answers):
    contest_id = get_contest_id(create_user_with_answers, DEFAULT_INDEX)
    base_contest_id = create_user_with_answers['base_contests'][DEFAULT_INDEX].base_contest_id
    client.set_prefix('contest/tasks/unauthorized')

    resp = client.get(f'/base_olympiad/{base_contest_id}/olympiad/{contest_id}')
    assert resp.status_code == 200
    response = resp.json
    assert response['user_count'] == 1
    assert response['academic_year'] == datetime.utcnow().year

    contest = create_user_with_answers['contests'][0]
    contest.start_date = datetime(2021, 6, 6, 10, 0, 0)
    test_app.db.session.commit()
    resp = client.get(f'/base_olympiad/{base_contest_id}/olympiad/{contest_id}')
    assert resp.status_code == 200
    response = resp.json
    assert response['academic_year'] == datetime.utcnow().year - 1
    print(response.keys())
    assert  2 == 3