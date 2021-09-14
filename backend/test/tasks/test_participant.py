from . import *

DEFAULT_INDEX = 0
ERROR_ID = 1500


@pytest.fixture
def client(client_university):
    client_university.set_prefix('contest/tasks/participant')
    yield client_university


# Variant


def test_enroll_in_contest(client, test_variant, test_simple_contest, test_user_for_student_contest,
                           test_olympiad_locations):
    resp = client.post(f'/contest/{test_simple_contest[0].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 200


def test_get_variant_self(client, test_simple_contest_with_users,
                          test_variant):
    resp = client.get(f'/contest/{test_simple_contest_with_users[0].contest_id}/variant/self')
    assert resp.status_code == 200
    assert test_simple_contest_with_users[0].users.all()[0].variant_id == resp.json['variant_id']


def test_change_user_location_in_contest(client, test_simple_contest_with_users, test_olympiad_locations,
                                         test_user_for_student_contest):
    resp = client.post(f'/contest/{test_simple_contest_with_users[0].contest_id}/change_location',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    print(resp.data)
    assert resp.status_code == 200


def test_get_all_tasks_self(client, test_simple_contest_with_users,
                            test_variant):
    resp = client.get(f'/contest/{test_simple_contest_with_users[0].contest_id}/tasks/self')
    assert resp.status_code == 200
    assert len(test_variant[0].tasks) == len(list(resp.json['tasks_list']))


def test_get_task_image_self(client, test_simple_contest_with_users, test_variant, create_plain_task):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/tasks/{test_variant[0].tasks[0].task_id}/image/self')
    assert resp.status_code == 409


def test_get_user_certificate_self_error(client, test_simple_contest_with_users, test_variant):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/certificate/self')
    print(resp.data)
    assert resp.status_code == 400
    # TODO version with correct date


def test_get_user_certificate_self(client, test_simple_contest_with_users, test_variant):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/certificate/self')
    print(resp.data)
    assert resp.status_code == 400
    # TODO version with correct date


# get_contest_in_stage_self

def test_get_all_contests_in_stage_self(client, test_contests_composite, test_stages, test_composite_contest_with_users):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/{test_stages[0].stage_id}/contest/all')
    print(resp.data)
    assert resp.status_code == 200
    assert 1 == len(list(resp.json['contest_list']))


def test_get_contest_in_stage_self(client, test_composite_contest_with_users, test_simple_contest_in_stage,
                                   test_contests_composite, test_stages):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/{test_stages[0].stage_id}/contest/{test_simple_contest_in_stage[0].contest_id}')
    print(resp.data)
    assert resp.status_code == 200
    assert test_simple_contest_in_stage[0].contest_id == resp.json['contest_id']


# Olympiad


def test_olympiads_all(client, test_simple_contest, test_contests_composite):
    resp = client.get('/olympiad/all')
    assert resp.status_code == 200
    assert len(test_simple_contest + test_contests_composite) == resp.json['count']


def test_get_contest_self(client, test_base_contests, test_simple_contest, test_simple_contest_with_users):
    resp = client.get(
        f'/olympiad/{test_simple_contest[0].contest_id}')
    print(resp.data)
    assert resp.status_code == 200
    assert test_simple_contest[0].contest_id == resp.json['contest_id']
