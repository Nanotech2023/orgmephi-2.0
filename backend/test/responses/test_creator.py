from . import *

DEFAULT_INDEX = 0
ERROR_ID = 1500


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('contest/responses/creator')
    yield client_creator


def test_user_response_creator(client, create_plain_task):
    contest_id = get_contest_id(create_plain_task, DEFAULT_INDEX)
    user_id = get_user_id(create_plain_task, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/user/{ERROR_ID}/create')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{ERROR_ID}/user/{user_id}/create')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/create')
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    response = get_user_in_contest_work(user_id, contest_id)
    assert response.work_status.value == 'InProgress'


def test_plain_task_text_creator(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_two_tasks, DEFAULT_INDEX)
    task_id = get_plain_task_id(create_two_tasks, DEFAULT_INDEX)
    task_id_from_different_contest = get_plain_task_id(create_two_tasks, 2)

    resp = client.post(f'/contest/{contest_id}/task/{task_id_from_different_contest}/user/{user_id}/plain',
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

    range_task_id = get_range_task_id(create_two_tasks, DEFAULT_INDEX)
    resp = client.post(f'/contest/{contest_id}/task/{range_task_id}/user/{user_id}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'PlainAnswerText'
    assert resp.json['answer_text'] == 'answer'


def test_plain_task_file_creator(client, create_one_task):
    index = 1
    contest_id = get_contest_id(create_one_task, index)
    user_id = get_user_id(create_one_task, index)
    task_id = get_plain_task_id(create_one_task, index)
    task_id_from_different_contest = get_plain_task_id(create_one_task, 2)

    resp = client.post(f'/contest/{contest_id}/task/{task_id_from_different_contest}/user/{user_id}/png',
                       data=test_image)
    assert resp.status_code == 409

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/jpeg', data=test_image)
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    assert user_answer.filetype == 'image/jpeg'


# noinspection DuplicatedCode
def test_plain_task_file_failed(client, create_one_task):
    contest_id_text = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id_text = get_user_id(create_one_task, DEFAULT_INDEX)
    task_id_text = get_plain_task_id(create_one_task, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id_text}/task/{task_id_text}/user/{user_id_text}/png', data=test_image)
    assert resp.status_code == 409

    index = 1
    contest_id_file = get_contest_id(create_one_task, index)
    user_id_file = get_user_id(create_one_task, index)
    task_id_file = get_plain_task_id(create_one_task, index)

    resp = client.post(f'/contest/{contest_id_file}/task/{task_id_file}/user/{user_id_file}/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 409


def test_plain_task_get_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task, 1)
    user_id = get_user_id(create_one_task, 1)
    task_id = get_plain_task_id(create_one_task, 1)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain/file', data=test_image)
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['filetype'] == 'image/jpeg'

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/plain/file')
    assert resp.status_code == 200
    assert resp.content_type == 'image/jpeg'


def test_range_task_creator(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_two_tasks, DEFAULT_INDEX)
    task_id = get_range_task_id(create_two_tasks, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 0.6 == answer.answer

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_two_tasks, DEFAULT_INDEX)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'RangeAnswer'
    assert resp.json['answer'] == 0.6


def test_multiple_task_creator(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_three_tasks, DEFAULT_INDEX)
    task_id = get_multiple_task_id(create_three_tasks, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "4"}]})
    assert resp.status_code == 409

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

    plain_task_id = get_plain_task_id(create_three_tasks, DEFAULT_INDEX)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'MultipleChoiceAnswer'
    assert '1' in resp.json['answers']
    assert '3' in resp.json['answers']


def test_get_status_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/status')
    assert resp.status_code == 200
    assert resp.json['status'] == 'InProgress'


def test_set_status_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)

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
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)
    task_id = get_plain_task_id(create_one_task, DEFAULT_INDEX)
    error_task_id = get_plain_task_id(create_one_task, 1)

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

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/{user_id}/mark',
                       json={'mark': 12})
    assert resp.status_code == 404

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert answer.mark == 11

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/{user_id}/mark')
    assert resp.status_code == 200
    assert resp.json['mark'] == 11


def test_time_left_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/time')
    assert resp.status_code == 200
    assert resp.json['time'] < 1800


def test_time_extend_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/user/{user_id}/time',
                       json={'time': 1800})
    assert resp.status_code == 200

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.time_extension == timedelta(seconds=1800)

    resp = client.get(f'/contest/{contest_id}/user/{user_id}/time')
    assert resp.status_code == 200
    assert resp.json['time'] > 1800


def test_finish_contest_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)

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


def test_get_contest_list_creator(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)
    plain_id = get_plain_task_id(create_one_task, DEFAULT_INDEX)

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
    plain_id = get_plain_task_id(create_user_with_answers, DEFAULT_INDEX)
    range_id = get_range_task_id(create_user_with_answers, DEFAULT_INDEX)
    multiple_id = get_multiple_task_id(create_user_with_answers, DEFAULT_INDEX)

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
    assert range_answer.mark == 5
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
            assert answer['task_points'] == 11
            assert answer['task_id'] == plain_id
            assert answer['right_answer'] is None
        elif answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 5
            assert answer['task_points'] == 5
            assert answer['task_id'] == range_id
            assert answer['right_answer']['start_value'] == 0.5
            assert answer['right_answer']['end_value'] == 0.7
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 0
            assert answer['task_points'] == 7
            assert answer['task_id'] == multiple_id
            assert answer['right_answer']['answers'] == ['1', '3']

    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 409

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/{user_id}/mark',
                       json={'mark': 11})
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
                       json={'mark': 1})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Diploma_3

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/mark',
                       json={'mark': 5})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 1})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Diploma_1

    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 3})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Winner_3

    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 5})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/winning')
    assert resp.status_code == 200
    user_in_contest = UserInContest.query.filter_by(contest_id=contest_id, user_id=user_id).one_or_none()
    assert user_in_contest.user_status == UserStatusEnum.Winner_2

    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/mark',
                       json={'mark': 7})
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

    start_year = datetime.utcnow().year - 1 if datetime.utcnow().month < 6 else datetime.utcnow().year
    end_year = datetime.utcnow().year if datetime.utcnow().month < 6 else datetime.utcnow().year + 1
    assert contest['start_year'] == start_year
    assert contest['end_year'] == end_year
    assert results[0]['status'] == 'NoResults'
    assert results[0]['mark'] == 23
    assert results[0]['user_status'] == 'Winner 1'


# noinspection DuplicatedCode
def test_auto_check_status(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_three_tasks, DEFAULT_INDEX)
    range_id = get_range_task_id(create_three_tasks, DEFAULT_INDEX)
    multiple_id = get_multiple_task_id(create_three_tasks, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/{user_id}/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/{user_id}/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "2"}]})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/user/{user_id}/finish')
    assert resp.status_code == 200

    contest = create_three_tasks['contests'][DEFAULT_INDEX]
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
    assert range_answer.mark == 5
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
            assert answer['mark'] == 5
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 0
