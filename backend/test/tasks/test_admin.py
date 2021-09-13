from contest.tasks.models import OlympiadType, OlympiadLocation
from . import *


@pytest.fixture
def client(client_admin):
    client_admin.set_prefix('contest/tasks/admin')
    yield client_admin


@pytest.fixture
def test_olympiad_type_remove(client, test_olympiad_types):
    test_type: OlympiadType = test_olympiad_types[0]
    resp = client.post(f'/olympiad_type/{test_type.olympiad_type_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        OlympiadType.query.filter_by(olympiad_type_id=f'{test_type.olympiad_type_id}').exists()
    ).scalar()


@pytest.fixture
def test_olympiad_type_create(client):
    resp = client.post('/olympiad_type/create',
                       json={
                           'olympiad_type': 'Test 0',
                       })
    assert resp.status_code == 200

    olympiad_type: OlympiadType = OlympiadType.query.filter_by(
        olympiad_type_id=resp.json['olympiad_type_id']).one_or_none()
    assert olympiad_type.id == resp.json['olympiad_type_id']


@pytest.fixture
def test_location_remove(client, test_olympiad_locations):
    test_location: OlympiadLocation = test_olympiad_locations[0]
    resp = client.post(f'/location/{test_location.location_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        OlympiadLocation.query.filter_by(location_id=f'{test_location.location_id}').exists()
    ).scalar()


@pytest.fixture
def test_online_location_create(client):
    resp = client.post('/location/create_online',
                       json={
                           'url': 'Test 0',
                       })
    assert resp.status_code == 200

    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.id == resp.json['location_id']


@pytest.fixture
def test_location_create_russia(client):
    resp = client.post('/location/create_russia',
                       json={
                           'city_name': 'Тула',
                           'region_name': 'Тульская обл.',
                           'address': 'Test 0',
                       })
    assert resp.status_code == 200

    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.id == resp.json['location_id']


@pytest.fixture
def test_location_create_other(client):
    resp = client.post('/location/create_other',
                       json={
                           'country_name': 'Россия',
                           'location': 'Test 0',
                       })
    assert resp.status_code == 200

    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.id == resp.json['location_id']
