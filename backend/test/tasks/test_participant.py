from . import *


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

    resp = client.post(f'/contest/{test_simple_contest[0].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 409

    resp = client.post(f'/contest/{test_simple_contest[1].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 409

    resp = client.post(f'/contest/{test_simple_contest[3].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 403

    resp = client.post(f'/contest/{test_simple_contest[4].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 409


def test_enroll_in_contest_different_stages(client, test_simple_contest_in_stage_1,
                                            test_olympiad_locations, test_user_for_student_contest):
    resp = client.post(f'/contest/{test_simple_contest_in_stage_1[1].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    print(resp.data)
    assert resp.status_code == 200


def test_enroll_in_contest_different_stages2(client, test_simple_contest_in_stage_2,
                                             test_olympiad_locations, test_user_for_student_contest):
    resp = client.post(f'/contest/{test_simple_contest_in_stage_2[1].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    print(resp.data)
    assert resp.status_code == 200


def test_enroll_in_contest_different_stages3(client, test_simple_contest_in_stage_3,
                                             test_olympiad_locations, test_user_for_student_contest):
    resp = client.post(f'/contest/{test_simple_contest_in_stage_3[1].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    print(resp.data)
    assert resp.status_code == 200


def test_enroll_in_contest_ended(client, test_variant, test_simple_contest, test_user_for_student_contest,
                                 test_olympiad_locations):
    test_simple_contest[0].end_of_enroll_date = datetime.utcnow()
    resp = client.post(f'/contest/{test_simple_contest[0].contest_id}/enroll',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 409


def test_get_variant_self(client, test_simple_contest_with_users,
                          test_variant):
    resp = client.get(f'/contest/{test_simple_contest_with_users[0].contest_id}/variant/self')
    assert resp.status_code == 200
    assert test_simple_contest_with_users[0].users.all()[0].variant_id == resp.json['variant_id']

    resp = client.get(f'/contest/{test_simple_contest_with_users[1].contest_id}/variant/self')
    assert resp.status_code == 404


def test_get_variant_self_no_variant(client, test_simple_contest_with_users_no_variant,
                                     test_variant):
    resp = client.get(f'/contest/{test_simple_contest_with_users_no_variant[1].contest_id}/variant/self')
    assert resp.status_code == 404


def test_get_variant_self_not_in_progress(client, test_simple_contest_with_users_not_in_progress,
                                          test_variant):
    resp = client.get(f'/contest/{test_simple_contest_with_users_not_in_progress[0].contest_id}/variant/self')
    assert resp.status_code == 403


def test_change_user_location_in_contest(client, test_simple_contest_with_users, test_olympiad_locations,
                                         test_user_for_student_contest):
    resp = client.post(f'/contest/{test_simple_contest_with_users[0].contest_id}/change_location',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 200


def test_change_user_location_in_contest_ended(client, test_simple_contest_with_users_ended, test_olympiad_locations,
                                               test_user_for_student_contest):
    resp = client.post(f'/contest/{test_simple_contest_with_users_ended[0].contest_id}/change_location',
                       json={
                           'location_id': test_olympiad_locations[0].location_id
                       })
    assert resp.status_code == 409


def test_get_all_tasks_self(client, test_simple_contest_with_users,
                            test_variant, create_multiple_task):
    resp = client.get(f'/contest/{test_simple_contest_with_users[0].contest_id}/tasks/self')
    assert resp.status_code == 200
    assert len(test_variant[0].tasks) == len(list(resp.json['tasks_list']))


def test_get_all_tasks_self_not_in_progress(client, test_simple_contest_with_users_not_in_progress,
                                            test_variant):
    resp = client.get(f'/contest/{test_simple_contest_with_users_not_in_progress[0].contest_id}/tasks/self')
    assert resp.status_code == 403


def test_get_all_tasks_self_completed(client, test_simple_contest_with_users_not_in_progress,
                                      test_variant):
    resp = client.get(f'/contest/{test_simple_contest_with_users_not_in_progress[0].contest_id}/tasks/self')
    assert resp.status_code == 403


def test_get_task_image_self(client, test_simple_contest_with_users, test_variant, create_plain_task):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/tasks/{test_variant[0].tasks[0].task_id}/image/self')
    assert resp.status_code == 409

    test_variant[0].tasks[0].image_of_task = b'Test'

    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/tasks/{test_variant[0].tasks[0].task_id}/image/self')
    assert resp.status_code == 200

    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/tasks/{test_variant[1].tasks[0].task_id}/image/self')
    assert resp.status_code == 409


def test_get_task_image_self_not_in_progress(client, test_simple_contest_with_users_not_in_progress,
                                             test_user_for_student_contest,
                                             test_variant, create_plain_task):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users_not_in_progress[0].contest_id}'
        f'/tasks/{test_variant[0].tasks[0].task_id}/image/self')
    assert resp.status_code == 403


def test_get_user_certificate_self_none_user(client, test_simple_contest_with_users_ended, test_variant,
                                             test_user_for_student_contest_none):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users_ended[0].contest_id}/certificate/self')
    assert resp.status_code == 409


def test_get_user_certificate_self_error(client, test_simple_contest_with_users_ended, test_variant):
    test_simple_contest_with_users_ended[0].result_publication_date = datetime.utcnow() + timedelta(hours=150)
    resp = client.get(
        f'/contest/{test_simple_contest_with_users_ended[0].contest_id}/certificate/self')
    assert resp.status_code == 403


def test_get_user_certificate_self(client, test_simple_contest_with_users, test_user_for_student_contest, test_variant):
    test_simple_contest_with_users[0].result_publication_date = datetime.utcnow() - timedelta(hours=150)
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/certificate/self')
    assert resp.status_code == 200


# get_contest_in_stage_self

def test_get_all_contests_in_stage_self(client, test_contests_composite,
                                        test_stages, test_composite_contest_with_users):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/{test_stages[0].stage_id}/contest/all')
    assert resp.status_code == 200
    assert 1 == len(list(resp.json['contest_list']))

    resp = client.get(f'/olympiad/{test_contests_composite[1].contest_id}'
                      f'/stage/{test_stages[0].stage_id}/contest/all')
    assert resp.status_code == 409


def test_get_contest_in_stage_self(client, test_composite_contest_with_users, test_simple_contest_in_stage_1,
                                   test_contests_composite, test_stages):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/{test_stages[0].stage_id}/contest/{test_simple_contest_in_stage_1[0].contest_id}')
    assert resp.status_code == 200
    assert test_simple_contest_in_stage_1[0].contest_id == resp.json['contest_id']

    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/{test_stages[1].stage_id}/contest/{test_simple_contest_in_stage_1[0].contest_id}')
    assert resp.status_code == 409

    resp = client.get(f'/olympiad/{test_contests_composite[1].contest_id}'
                      f'/stage/{test_stages[0].stage_id}/contest/{test_simple_contest_in_stage_1[0].contest_id}')
    assert resp.status_code == 409


def test_get_contest_in_stage_self_error(client, test_composite_contest_with_users, test_simple_contest_in_stage_1,
                                         test_contests_composite, test_stages):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/{test_stages[0].stage_id}/contest/{test_simple_contest_in_stage_1[1].contest_id}')
    assert resp.status_code == 409


# Olympiad


def test_olympiads_all(client, test_simple_contest, test_contests_composite):
    resp = client.get('/olympiad/all')
    assert resp.status_code == 200
    assert len(test_simple_contest + test_contests_composite) == resp.json['count']


def test_get_contest_self(client, test_base_contests, test_simple_contest, test_simple_contest_with_users):
    resp = client.get(
        f'/olympiad/{test_simple_contest[0].contest_id}')
    assert resp.status_code == 200
    assert test_simple_contest[0].contest_id == resp.json['contest_id']


def test_get_contest_sel_composite(client, test_base_contests, test_contests_composite, test_simple_contest_with_users):
    resp = client.get(
        f'/olympiad/{test_contests_composite[0].contest_id}')
    assert resp.status_code == 409


def test_get_contest_self_not_reg(client, test_base_contests, test_simple_contest):
    resp = client.get(
        f'/olympiad/{test_simple_contest[0].contest_id}')
    assert resp.status_code == 409
