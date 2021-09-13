from contest.tasks.models import OlympiadType, OlympiadLocation
from . import *


@pytest.fixture
def client(client_admin):
    client_admin.set_prefix('contest/tasks/admin')
    yield client_admin


def test_olympiad_type_remove(client, test_olympiad_types):
    test_type: OlympiadType = test_olympiad_types[0]
    resp = client.post(f'/olympiad_type/{test_type.olympiad_type_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        OlympiadType.query.filter_by(olympiad_type_id=f'{test_type.olympiad_type_id}').exists()
    ).scalar()


def test_olympiad_type_create(client):
    resp = client.post('/olympiad_type/create',
                       json={
                           'olympiad_type': 'Test 0',
                       })
    assert resp.status_code == 200

    olympiad_type: OlympiadType = OlympiadType.query.filter_by(
        olympiad_type_id=resp.json['olympiad_type_id']).one_or_none()
    assert olympiad_type.olympiad_type_id == resp.json['olympiad_type_id']


def test_location_remove(client, test_olympiad_locations):
    test_location: OlympiadLocation = test_olympiad_locations[0]
    resp = client.post(f'/location/{test_location.location_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        OlympiadLocation.query.filter_by(location_id=f'{test_location.location_id}').exists()
    ).scalar()


def test_online_location_create(client):
    resp = client.post('/location/create_online',
                       json={
                           'url': 'https://www.example.com',
                       })
    print(resp.data)
    assert resp.status_code == 200
    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.location_id == resp.json['location_id']


def test_location_create_russia(client, test_city):
    resp = client.post('/location/create_russia',
                       json={
                           'city_name': f'{test_city.name}',
                           'region_name': f'{test_city.region_name}',
                           'address': 'Test 0',
                       })
    print(resp.data)
    assert resp.status_code == 200
    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.location_id == resp.json['location_id']


def test_location_create_other(client, test_country_native):
    resp = client.post('/location/create_other',
                       json={
                           'country_name': f'{test_country_native.name}',
                           'location': 'Test 0',
                       })
    print(resp.data)
    assert resp.status_code == 200
    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.location_id == resp.json['location_id']
