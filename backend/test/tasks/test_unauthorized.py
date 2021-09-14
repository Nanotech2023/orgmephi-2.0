from . import *

DEFAULT_INDEX = 0
ERROR_ID = 1500


@pytest.fixture
def client(client_visitor):
    client_visitor.set_prefix('contest/tasks/unauthorized')
    yield client_visitor


# olympiad type


def test_olympiad_type_all(client, test_olympiad_types):
    resp = client.get('/olympiad_type/all')
    assert resp.status_code == 200
    assert len(test_olympiad_types) == len(list(resp.json['olympiad_types']))


def test_olympiad_type_get(client, test_olympiad_types):
    resp = client.get(f'/olympiad_type/{test_olympiad_types[0].olympiad_type_id}')
    assert resp.status_code == 200
    assert test_olympiad_types[0].olympiad_type_id == resp.json['olympiad_type_id']


# location


def test_location_all(client, test_olympiad_locations):
    resp = client.get('/location/all')
    assert resp.status_code == 200
    assert len(test_olympiad_locations) == len(list(resp.json['locations']))


def test_id_location_get(client, test_olympiad_locations):
    resp = client.get(f'/location/{test_olympiad_locations[0].location_id}')
    assert resp.status_code == 200
    assert test_olympiad_locations[0].location_id == resp.json['location_id']


# base olympiad


def test_base_olympiads_all(client, test_base_contests):
    resp = client.get('/base_olympiad/all')
    assert resp.status_code == 200
    assert len(test_base_contests) == len(list(resp.json['olympiad_list']))


def test_base_olympiad_get(client, test_base_contests):
    resp = client.get(f'/base_olympiad/{test_base_contests[0].base_contest_id}')
    assert resp.status_code == 200
    assert test_base_contests[0].base_contest_id == resp.json['base_contest_id']


# olympiads


def test_olympiads_all(client, test_simple_contest, test_contests_composite):
    resp = client.get('/olympiad/all')
    assert resp.status_code == 200
    assert len(test_simple_contest + test_contests_composite) == resp.json['count']


def test_olympiad_get(client, test_base_contests, test_simple_contest):
    resp = client.get(
        f'/base_olympiad/{test_base_contests[0].base_contest_id}/olympiad/{test_simple_contest[0].contest_id}')
    assert resp.status_code == 200
    assert test_simple_contest[0].contest_id == resp.json['contest_id']


# Stage


def test_stages_all(client, test_contests_composite, test_stages):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/all')
    assert resp.status_code == 200
    assert len(test_stages) == len(list(resp.json['stages_list']))


def test_stage_get(client, test_contests_composite, test_stages):
    resp = client.get(f'/olympiad/{test_contests_composite[0].contest_id}'
                      f'/stage/{test_stages[0].stage_id}')
    assert resp.status_code == 200
    assert test_stages[0].stage_id == resp.json['stage_id']
    resp = client.get(f'/olympiad/{test_contests_composite[1].contest_id}'
                      f'/stage/{test_stages[0].stage_id}')
    assert resp.status_code == 409


# Target classes


def test_target_classes_all(client, test_target_class):
    resp = client.get(f'/target_class/all')
    assert resp.status_code == 200
    assert len(test_target_class) == len(list(resp.json['target_classes']))


def test_get_target_class(client, test_target_class):
    resp = client.get(f'/target_class/{test_target_class[0].target_class_id}')
    assert resp.status_code == 200
    assert test_target_class[0].target_class_id == resp.json['target_class_id']
