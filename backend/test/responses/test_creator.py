from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('contest/responses/creator')
    yield client_creator


def test_user_response_creator(client, create_plain_task):
    contest_id = get_contest_id(create_plain_task)
    user_id = get_user_id(create_plain_task)

    resp = client.post(f'/contest/{contest_id}/user/{1000}/create')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{1010}/user/{user_id}/create')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    response = get_user_in_contest_work(user_id, contest_id)
    assert response.work_status.value == 'InProgress'


def test_plain_task_text_creator(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks)
    user_id = get_user_id(create_two_tasks)
    task_id = get_plain_task_id(create_two_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 'answer' == answer.answer_text

    resp = client.post(f'/contest/{contest_id}/task/{14}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    range_task_id = get_range_task_id(create_two_tasks)
    resp = client.post(f'/contest/{contest_id}/task/{range_task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'PlainAnswerText'
    assert resp.json['answer_text'] == 'answer'


def test_plain_task_file_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    task_id = get_plain_task_id(create_one_task)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/png', data=b'Test')
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    assert user_answer.answer_file == b'Test'
    assert user_answer.filetype.value == 'png'


def test_plain_task_get(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    task_id = get_plain_task_id(create_one_task)

    from contest.responses.util import user_answer_post_file
    user_answer_post_file(b'Test', 'png', user_id, contest_id, task_id)

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['filetype'] == 'png'

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain/file')
    assert resp.status_code == 200
    assert resp.data == b'Test'


def test_range_task_creator(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks)
    user_id = get_user_id(create_two_tasks)
    task_id = get_range_task_id(create_two_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 0.6 == answer.answer

    resp = client.post(f'/contest/{contest_id}/task/{14}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_two_tasks)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'RangeAnswer'
    assert resp.json['answer'] == 0.6


def test_multiple_task_creator(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks)
    user_id = get_user_id(create_three_tasks)
    task_id = get_multiple_task_id(create_three_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert '1' in answer.answers
    assert '3' in answer.answers

    resp = client.post(f'/contest/{contest_id}/task/{14}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_three_tasks)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'MultipleChoiceAnswer'
    assert '1' in resp.json['answers']
    assert '3' in resp.json['answers']


def test_get_status_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/status')
    assert resp.status_code == 200
    assert resp.json['status'] == 'InProgress'


def test_set_status_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/status',
                       json={'status': 'NotChecked'})
    assert resp.status_code == 200

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NotChecked'

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/status',
                       json={'status': '333'})
    assert resp.status_code == 400


def test_mark_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    task_id = get_plain_task_id(create_one_task)

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['mark'] == 0

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark',
                       json={'mark': 12})
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/task/{15}/user/{user_id}/mark',
                       json={'mark': 12})
    assert resp.status_code == 404

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert answer.mark == 12

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['mark'] == 12


def test_time_left_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/time')
    assert resp.status_code == 200
    assert resp.json['time'] < 1800


def test_time_extend_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/time',
                       json={'time': 1800})
    assert resp.status_code == 200

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.time_extension == timedelta(seconds=1800)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/time')
    assert resp.status_code == 200
    assert resp.json['time'] > 1800


def test_finish_contest(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)

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
def test_all_answers(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks)
    user_id = get_user_id(create_three_tasks)
    plain_id = get_plain_task_id(create_three_tasks)
    range_id = get_range_task_id(create_three_tasks)
    multiple_id = get_multiple_task_id(create_three_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/response')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    assert len(resp.json['user_answers']) == 3


def test_get_contest_list(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    plain_id = get_plain_task_id(create_one_task)

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
def test_auto_check(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks)
    user_id = get_user_id(create_three_tasks)
    plain_id = get_plain_task_id(create_three_tasks)
    range_id = get_range_task_id(create_three_tasks)
    multiple_id = get_multiple_task_id(create_three_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "2"}]})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/user/{user_id}/finish')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/check')
    assert resp.status_code == 409

    contest = create_three_tasks[0]
    from contest.tasks.models.olympiad import ContestHoldingTypeEnum
    contest.holding_type = ContestHoldingTypeEnum.OfflineContest
    resp = client.post(f'/contest/{contest_id}/check')
    assert resp.status_code == 409
    contest.holding_type = ContestHoldingTypeEnum.OnLineContest

    contest.end_date = datetime.utcnow() - timedelta(minutes=5)
    resp = client.post(f'/contest/{contest_id}/check')
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    plain_answer = user_answer_get(user_id, contest_id, plain_id)
    assert plain_answer.mark == 0
    range_answer = user_answer_get(user_id, contest_id, range_id)
    assert range_answer.mark == 5
    multiple_answer = user_answer_get(user_id, contest_id, multiple_id)
    assert multiple_answer.mark == 0

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    user_answers = resp.json['user_answers']
    assert len(user_answers) == 3

    for answer in user_answers:
        if answer['answer_type'] == 'PlainAnswerText':
            assert answer['mark'] == 0
        elif answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 5
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 0

