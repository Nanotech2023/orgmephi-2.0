from . import *

DEFAULT_INDEX = 0
ERROR_ID = 1500


@pytest.fixture
def client(client_university):
    client_university.set_prefix('contest/responses/participant')
    yield client_university


# noinspection DuplicatedCode
def test_user_response_participant(client, create_plain_task):
    contest_id = get_contest_id(create_plain_task, DEFAULT_INDEX)
    user_id = get_user_id(create_plain_task, DEFAULT_INDEX)

    contest = create_plain_task['contests'][DEFAULT_INDEX]
    contest.start_date = datetime.utcnow() + timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 409

    resp = client.post(f'/contest/{ERROR_ID}/user/self/create')
    assert resp.status_code == 404

    contest.start_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    response = get_user_in_contest_work(user_id, contest_id)
    assert response.work_status.value == 'InProgress'


def test_contest_zero_duration(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)
    task_id = get_plain_task_id(create_one_task, DEFAULT_INDEX)

    contest = create_one_task['contests'][DEFAULT_INDEX]
    contest.contest_duration = timedelta(seconds=0)
    contest.end_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    response = get_user_in_contest_work(user_id, contest_id)
    assert response.work_status.value == 'NotChecked'


# noinspection DuplicatedCode
def test_user_response_offline_contest_participant(client, create_plain_task):
    index = 1
    contest_id = get_contest_id(create_plain_task, index)

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_plain_task_text_participant(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_two_tasks, DEFAULT_INDEX)
    task_id = get_plain_task_id(create_two_tasks, DEFAULT_INDEX)
    task_id_from_different_contest = get_plain_task_id(create_two_tasks, 2)

    resp = client.post(f'/contest/{contest_id}/task/{task_id_from_different_contest}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    answer = user_answer_get(user_id, contest_id, task_id)
    assert 'answer' == answer.answer_text

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/self/plain',
                       json={'answer_text': 'answer'})
    assert resp.status_code == 404

    range_task_id = get_range_task_id(create_two_tasks, DEFAULT_INDEX)
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
    index = 1
    contest_id = get_contest_id(create_one_task, index)
    user_id = get_user_id(create_one_task, index)
    task_id = get_plain_task_id(create_one_task, index)
    task_id_from_different_contest = get_plain_task_id(create_one_task, 3)

    resp = client.post(f'/contest/{contest_id}/task/{task_id_from_different_contest}/user/self/png',
                       data=test_image)
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/plain/file', data=test_image)
    assert resp.status_code == 200

    from contest.responses.util import user_answer_get
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    assert user_answer.filetype == 'image/jpeg'

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/plain/file', data=test_image)
    assert resp.status_code == 200
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    assert user_answer.filetype == 'image/jpeg'


# noinspection DuplicatedCode
def test_plain_task_get_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task, 1)
    user_id = get_user_id(create_one_task, 1)
    task_id = get_plain_task_id(create_one_task, 1)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/plain/file', data=test_image)
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self')
    assert resp.status_code == 200
    assert resp.json['filetype'] == 'image/jpeg'

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/plain/file')
    assert resp.status_code == 200
    assert resp.content_type == 'image/jpeg'


# noinspection DuplicatedCode
def test_range_task_participant(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_two_tasks, DEFAULT_INDEX)
    task_id = get_range_task_id(create_two_tasks, DEFAULT_INDEX)

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

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_two_tasks, DEFAULT_INDEX)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'RangeAnswer'
    assert resp.json['answer'] == 0.5


# noinspection DuplicatedCode
def test_multiple_task_creator(client, create_three_tasks):
    contest_id = get_contest_id(create_three_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_three_tasks, DEFAULT_INDEX)
    task_id = get_multiple_task_id(create_three_tasks, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/task/{task_id}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "4"}]})
    assert resp.status_code == 409

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

    resp = client.post(f'/contest/{contest_id}/task/{ERROR_ID}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    plain_task_id = get_plain_task_id(create_three_tasks, DEFAULT_INDEX)
    resp = client.post(f'/contest/{contest_id}/task/{plain_task_id}/user/self/multiple',
                       json={"answers": [{"answer": "1"}, {"answer": "3"}]})
    assert resp.status_code == 404

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self')
    assert resp.status_code == 200
    assert resp.json['answer_type'] == 'MultipleChoiceAnswer'
    assert '3' in resp.json['answers']
    assert '2' in resp.json['answers']


def test_get_status_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)

    resp = client.get(f'/contest/{contest_id}/user/self/status')
    assert resp.status_code == 200
    assert resp.json['status'] == 'InProgress'


# noinspection DuplicatedCode
def test_mark_participant(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_two_tasks, DEFAULT_INDEX)
    task_id = get_plain_task_id(create_two_tasks, DEFAULT_INDEX)

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/mark')
    assert resp.status_code == 409

    contest = create_two_tasks['contests'][DEFAULT_INDEX]
    contest.result_publication_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.get(f'/contest/{contest_id}/task/{task_id}/user/self/mark')
    assert resp.status_code == 409

    from contest.tasks.util import get_user_in_contest_by_id_if_possible
    user_in_contest = get_user_in_contest_by_id_if_possible(contest_id, user_id)
    user_in_contest.show_results_to_user = True
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
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)

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

    contest = create_one_task['contests'][DEFAULT_INDEX]
    contest.contest_duration = timedelta(seconds=0)
    contest.start_date = datetime.utcnow() - timedelta(minutes=5)
    user_work.start_time = datetime.utcnow()
    contest.end_date = datetime.utcnow() + timedelta(minutes=5)
    resp = client.get(f'/contest/{contest_id}/user/self/time')
    assert resp.status_code == 200
    assert resp.json['time'] > 250
    assert resp.json['time'] < 310


# noinspection DuplicatedCode
def test_finish_contest_participant(client, create_one_task):
    contest_id = get_contest_id(create_one_task, DEFAULT_INDEX)
    user_id = get_user_id(create_one_task, DEFAULT_INDEX)
    plain_id = get_plain_task_id(create_one_task, DEFAULT_INDEX)

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
def test_all_answers_participant(client, create_user_with_answers):
    contest_id = get_contest_id(create_user_with_answers, DEFAULT_INDEX)
    user_id = get_user_id(create_user_with_answers, DEFAULT_INDEX)

    resp = client.get(f'/contest/{contest_id}/user/self/response')
    assert resp.status_code == 200
    assert resp.json['contest_id'] == contest_id
    assert resp.json['user_id'] == user_id
    assert len(resp.json['user_answers']) == 3


# noinspection DuplicatedCode
def test_auto_check_participant(client, create_user_with_answers):
    index = 1
    contest_id = get_contest_id(create_user_with_answers, index)
    user_id = get_user_id(create_user_with_answers, index)
    plain_id = get_plain_task_id(create_user_with_answers, index)
    range_id = get_range_task_id(create_user_with_answers, index)
    multiple_id = get_multiple_task_id(create_user_with_answers, index)

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

    from contest.tasks.util import get_user_in_contest_by_id_if_possible
    user_in_contest = get_user_in_contest_by_id_if_possible(contest_id, user_id)
    user_in_contest.show_results_to_user = True
    test_app.db.session.commit()

    resp = client.get(f'/contest/{contest_id}/user/self/mark')
    assert resp.status_code == 409

    contest = create_user_with_answers['contests'][index]
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
            assert answer['task_points'] == 11
            assert answer['task_id'] == plain_id
            assert answer['right_answer'] is None
        elif answer['answer_type'] == 'RangeAnswer':
            assert answer['mark'] == 0
            assert answer['task_points'] == 5
            assert answer['task_id'] == range_id
            assert answer['right_answer']['start_value'] == 0.5
            assert answer['right_answer']['end_value'] == 0.7
        elif answer['answer_type'] == 'MultipleChoiceAnswer':
            assert answer['mark'] == 7
            assert answer['task_points'] == 7
            assert answer['task_id'] == multiple_id
            assert answer['right_answer']['answers'] == ['1', '3']


# noinspection DuplicatedCode
def test_time_error_participant(client, create_plain_task):
    contest_id = get_contest_id(create_plain_task, DEFAULT_INDEX)
    contest = create_plain_task['contests'][DEFAULT_INDEX]
    contest.end_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/user/self/create')
    assert resp.status_code == 409


def test_answer_errors_participant(client, create_three_tasks):
    index = 1
    contest_id = get_contest_id(create_three_tasks, index)
    plain_id = get_plain_task_id(create_three_tasks, index)
    range_id = get_range_task_id(create_three_tasks, index)

    resp = client.get(f'/contest/{contest_id}/task/{plain_id}/user/self')
    assert resp.status_code == 404

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/png', data=test_image)
    assert resp.status_code == 200

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/self/range',
                       json={'answer': 0.6})
    assert resp.status_code == 200

    resp = client.get(f'/contest/{contest_id}/task/{range_id}/user/self/plain/file')
    assert resp.status_code == 404


def test_time_left_error_participant(client, create_two_tasks):
    contest_id = get_contest_id(create_two_tasks, DEFAULT_INDEX)
    user_id = get_user_id(create_two_tasks, DEFAULT_INDEX)
    plain_id = get_plain_task_id(create_two_tasks, DEFAULT_INDEX)
    range_id = get_range_task_id(create_two_tasks, DEFAULT_INDEX)

    resp = client.post(f'/contest/{contest_id}/task/{range_id}/user/self/range',
                       json={'answer': 0.8})
    assert resp.status_code == 200

    contest = create_two_tasks['contests'][DEFAULT_INDEX]
    contest.contest_duration = timedelta(seconds=0)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/plain',
                       json={'answer_text': "answer"})
    assert resp.status_code == 200

    contest.end_date = datetime.utcnow() - timedelta(minutes=5)
    test_app.db.session.commit()

    resp = client.post(f'/contest/{contest_id}/task/{plain_id}/user/self/plain',
                       json={'answer_text': "answer"})
    assert resp.status_code == 409

    from contest.responses.util import get_user_in_contest_work
    user_work = get_user_in_contest_work(user_id, contest_id)
    assert user_work.status.value == 'NotChecked'


def test_all_user_results_participant(client, create_user_with_answers):
    resp = client.get(f'/contest/user/self/results')
    assert resp.status_code == 200

    results = resp.json['results']
    contest = results[0]['contest_info']
    assert len(results) == 8
    assert contest['subject'] == 'Math'

    academic_year = datetime.utcnow().year - 1 if datetime.utcnow().month < 6 else datetime.utcnow().year
    assert contest['academic_year'] == academic_year
    assert results[0]['status'] == 'InProgress'
    assert results[0]['mark'] == 0
    assert results[0]['user_status'] == 'Participant'
