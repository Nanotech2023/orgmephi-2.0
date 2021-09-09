import datetime

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
    assert user_work.time_extension == datetime.timedelta(seconds=1800)

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
