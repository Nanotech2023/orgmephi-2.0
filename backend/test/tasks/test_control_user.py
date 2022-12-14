from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('contest/tasks/control_users')
    yield client_creator


def test_add_user_to_contest(client, test_simple_contest_with_location, test_olympiad_locations,
                             test_user_for_student_contest):
    resp = client.post(
        f'/contest/{test_simple_contest_with_location[0].contest_id}/add_user',
        json={
            'users_id': [f'{test_user_for_student_contest.id}'],
            'location_id': f'{test_olympiad_locations[0].location_id}',
            'show_results_to_user': 'true',
            'check_condition': 'true'
        })
    assert resp.status_code == 200

    resp = client.post(
        f'/contest/{test_simple_contest_with_location[0].contest_id}/add_user',
        json={
            'users_id': [f'{test_user_for_student_contest.id}'],
            'location_id': f'{test_olympiad_locations[0].location_id}',
            'show_results_to_user': 'true',
            'check_condition': 'true'
        })
    assert resp.status_code == 409

    resp = client.post(
        f'/contest/{test_simple_contest_with_location[1].contest_id}/add_user',
        json={
            'users_id': [f'{test_user_for_student_contest.id}'],
            'location_id': f'{test_olympiad_locations[0].location_id}',
            'show_results_to_user': 'true',
            'check_condition': 'true'
        })
    assert resp.status_code == 409

    resp = client.post(
        f'/contest/{test_simple_contest_with_location[3].contest_id}/add_user',
        json={
            'users_id': [f'{test_user_for_student_contest.id}'],
            'location_id': f'{test_olympiad_locations[0].location_id}',
            'show_results_to_user': 'true',
            'check_condition': 'true'
        })
    assert resp.status_code == 200


def test_add_user_to_contest_school(client, test_simple_contest_with_location, test_olympiad_locations,
                                    test_user_school):
    resp = client.post(
        f'/contest/{test_simple_contest_with_location[0].contest_id}/add_user',
        json={
            'users_id': [f'{test_user_school.id}'],
            'location_id': f'{test_olympiad_locations[0].location_id}',
            'show_results_to_user': 'true',
            'check_condition': 'true'
        })
    assert resp.status_code == 409


def test_change_user_location(client, test_simple_contest_with_users, test_olympiad_locations,
                              test_user_for_student_contest):
    resp = client.post(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/change_location',
        json={
            'users_id': [f'{test_user_for_student_contest.id}'],
            'location_id': f'{test_olympiad_locations[0].location_id}',
        })
    assert resp.status_code == 200
    resp = client.post(
        f'/contest/{test_simple_contest_with_users[2].contest_id}/change_location',
        json={
            'users_id': [f'{test_user_for_student_contest.id}'],
            'location_id': f'{test_olympiad_locations[0].location_id}',
        })
    assert resp.status_code == 409


def test_change_user_from_contest(client, test_simple_contest_with_users,
                                  test_olympiad_locations, test_user_university):
    resp = client.patch(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/edit_users',
        json={
            'users_id': [f'{test_user_university.id}'],
            'show_results_to_user': True,
        })
    assert resp.status_code == 200

    resp = client.patch(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/edit_users',
        json={
            'users_id': [f'{test_user_university.id}'],
            'show_results_to_user': True,
            'location_id': '0',
        })
    assert resp.status_code == 404


def test_remove_user_from_contest(client, test_simple_contest_with_users,
                                  test_olympiad_locations, test_user_university):
    resp = client.post(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/remove_user',
        json={
            'users_id': [f'{test_user_university.id}'],
        })
    assert resp.status_code == 200
    resp = client.post(
        f'/contest/{test_simple_contest_with_users[1].contest_id}/remove_user',
        json={
            'users_id': [f'{test_user_university.id}'],
        })
    assert resp.status_code == 409


def test_get_all_users_in_contest(client, test_simple_contest_with_users):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/user/all')
    assert resp.status_code == 200

    assert len(test_simple_contest_with_users[0].users.all()) == len(list(resp.json['user_list']))


def test_get_user_certificate_in_contest(client, test_simple_contest_with_users, test_user_for_student_contest):
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[0].contest_id}/user/{test_user_for_student_contest.id}/certificate')
    assert resp.status_code == 200
    resp = client.get(
        f'/contest/{test_simple_contest_with_users[1].contest_id}/user/{test_user_for_student_contest.id}/certificate')
    assert resp.status_code == 409
