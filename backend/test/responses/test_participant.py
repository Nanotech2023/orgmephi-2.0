from . import *


@pytest.fixture
def client(client_university):
    client_university.set_prefix('contest/responses/participant')
    yield client_university


# noinspection DuplicatedCode
def test_user_response_participant(client, create_plain_task):
    contest_id = get_contest_id(create_plain_task)
    user_id = get_user_id(create_plain_task)

    resp = client.post(f'/contest/{1010}/user/self/create')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    response = get_user_in_contest_work(user_id, contest_id)
    assert response.work_status.value == 'InProgress'


# noinspection DuplicatedCode
def test_plain_task_text_participant(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks)
    user_id = get_user_id(create_two_tasks)
    task_id = get_plain_task_id(create_two_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 'answer' == answer.answer_text

    resp = client.post(f'/contest/{contest_id}/task/{14}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    range_task_id = get_range_task_id(create_two_tasks)
    resp = client.post(f'/contest/{contest_id}/task/{range_task_id}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'PlainAnswerText'
    assert resp.json['answer_text'] == 'answer'

    resp = client.get(f'/contest/{12}/task/{task_id}/user/self')
    assert resp.status_code == 404
    resp = client.get(f'/contest/{contest_id}/task/{1100}/user/self')
    assert resp.status_code == 404


# noinspection DuplicatedCode
def test_plain_task_file_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    task_id = get_plain_task_id(create_one_task)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/png', data=b'Test')
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    assert user_answer.answer_file == b'Test'
    assert user_answer.filetype.value == 'png'

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/pdf', data=b'File2')
    assert resp.status_code == 200
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    assert user_answer.answer_file == b'File2'
    assert user_answer.filetype.value == 'pdf'


# noinspection DuplicatedCode
def test_plain_task_get_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    task_id = get_plain_task_id(create_one_task)

    from contest.responses.util import user_answer_post_file
    user_answer_post_file(b'Test', 'png', user_id, contest_id, task_id)

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self')
    assert resp.status_code == 200
    assert resp.json['filetype'] == 'png'

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/plain/file')
    assert resp.status_code == 200
    assert resp.data == b'Test'


# noinspection DuplicatedCode
def test_range_task_participant(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks)
    user_id = get_user_id(create_two_tasks)
    task_id = get_range_task_id(create_two_tasks)

    resp = client.post(f'/contest/{100}/task/{task_id}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 0.6 == answer.answer

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/range',
                       json={'answer': 0.5})
    assert resp.status_code == 200
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 0.5 == answer.answer

    resp = client.post(f'/contest/{contest_id}/task/{14}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_two_tasks)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'RangeAnswer'
    assert resp.json['answer'] == 0.5


# noinspection DuplicatedCode
def test_multiple_task_creator(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks)
    user_id = get_user_id(create_three_tasks)
    task_id = get_multiple_task_id(create_three_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert '1' in answer.answers
    assert '3' in answer.answers

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/multiple',
                       json={"answers": [{"answer": "2"}, {"answer": "3"}]})
    assert resp.status_code == 200

    answer = user_answer_get(user_id, contest_id, task_id)
    assert '1' not in answer.answers
    assert '2' in answer.answers

    resp = client.post(f'/contest/{contest_id}/task/{14}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_three_tasks)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'MultipleChoiceAnswer'
    assert '3' in resp.json['answers']
    assert '2' in resp.json['answers']


def test_get_status_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)

    resp = client.get(f'/contest/{contest_id}/user/self/status')
    assert resp.status_code == 200
    assert resp.json['status'] == 'InProgress'


# noinspection DuplicatedCode
def test_mark_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    task_id = get_plain_task_id(create_one_task)

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/mark')
    assert resp.status_code == 409

    contest = create_one_task[0]
    contest.result_publication_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/mark')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/mark')
    assert resp.status_code == 200
    assert resp.json['mark'] == 0

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    answer.mark = 12
    test_app.db.session.commit()

    resp = client.get(f'/contest/{contest_id}/task/{14}/user/self/mark')
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/mark')
    assert resp.status_code == 200
    assert resp.json['mark'] == 12


def test_time_left_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)

    resp = client.get(f'/contest/{contest_id}/user/self/time')
    assert resp.status_code == 200
    assert resp.json['time'] < 1800
    assert resp.json['time'] > 0

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    user_work.start_time = datetime.utcnow() - timedelta(minutes=45)

    resp = client.get(f'/contest/{contest_id}/user/self/time')
    assert resp.status_code == 200
    assert resp.json['time'] == 0


# noinspection DuplicatedCode
def test_finish_contest_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task)
    user_id = get_user_id(create_one_task)
    plain_id = get_plain_task_id(create_one_task)

    resp = client.post(f'/contest/{contest_id}/user/self/finish')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/plain',
                       json={'answer_text': "answer"})
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NotChecked'

    from contest.tasks.models.user import UserInContest
    user_in_contest: UserInContest = UserInContest.query.filter_by(contest_id=user_work.contest_id,
                                                                   user_id=user_work.user_id).one_or_none()
    assert user_in_contest.completed_the_contest == 1

    resp = client.get(f'/contest/{contest_id}/user/self/time')
    assert resp.status_code == 200
    assert resp.json['time'] == 0


# noinspection DuplicatedCode
def test_all_answers_participant(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks)
    user_id = get_user_id(create_three_tasks)
    plain_id = get_plain_task_id(create_three_tasks)
    range_id = get_range_task_id(create_three_tasks)
    multiple_id = get_multiple_task_id(create_three_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/user/self/response')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    assert len(resp.json['user_answers']) == 3


# noinspection DuplicatedCode
def test_auto_check_creator(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks)
    user_id = get_user_id(create_three_tasks)
    plain_id = get_plain_task_id(create_three_tasks)
    range_id = get_range_task_id(create_three_tasks)
    multiple_id = get_multiple_task_id(create_three_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/self/range',
                       json={'answer': 0.8})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/task/{multiple_id}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 200
    resp = client.post(f'/contest/{contest_id}/user/self/finish')
    assert resp.status_code == 200

    from contest.responses.util import get_user_in_contest_work, check_user_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    check_user_work(user_work)

    from contest.responses.util import user_answer_get
    plain_answer = user_answer_get(user_id, contest_id, plain_id)
    assert plain_answer.mark == 0
    range_answer = user_answer_get(user_id, contest_id, range_id)
    assert range_answer.mark == 0
    multiple_answer = user_answer_get(user_id, contest_id, multiple_id)
    assert multiple_answer.mark == 7

    resp = client.get(f'/contest/{contest_id}/user/self/mark')
    assert resp.status_code == 409
    contest = create_three_tasks[0]
    contest.result_publication_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.get(f'/contest/{contest_id}/user/self/mark')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    user_answers = resp.json['user_answers']
    assert len(user_answers) == 3

    for answer in user_answers:
        if answer['answer_type'] == 'PlainAnswerText':
            assert answer['mark'] == 0
        elif answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 0
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 7


# noinspection DuplicatedCode
def test_time_error_participant(client, create_plain_task):
    contest_id = get_contest_id(create_plain_task)
    contest = create_plain_task[0]
    contest.end_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 409


def test_answer_errors_participant(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks)
    plain_id = get_plain_task_id(create_three_tasks)
    range_id = get_range_task_id(create_three_tasks)

    resp = client.get(f'/contest/{contest_id}/task/{plain_id}/user/self')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/png', data=b'Test')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{range_id}/user/self/plain/file')
    assert resp.status_code == 404


def test_time_left_error_participant(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks)
    user_id = get_user_id(create_two_tasks)
    plain_id = get_plain_task_id(create_two_tasks)
    range_id = get_range_task_id(create_two_tasks)

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/self/range',
                       json={'answer': 0.8})
    assert resp.status_code == 200

    contest = create_two_tasks[0]
    contest.contest_duration = timedelta(seconds=0)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/plain',
                       json={'answer_text': "answer"})
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NotChecked'

