from . import *


@pytest.fixture
def client(client_admin):
    client_admin.set_prefix('contest/tasks/admin')
    yield client_admin


def test_olympiad_type_remove(client, test_olympiad_types):
    from contest.tasks.models import OlympiadType
    test_type: OlympiadType = test_olympiad_types[0]
    resp = client.post(f'/olympiad_type/{test_type.olympiad_type_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        OlympiadType.query.filter_by(olympiad_type_id=f'{test_type.olympiad_type_id}').exists()
    ).scalar()


def test_olympiad_type_create(client):
    from contest.tasks.models import OlympiadType
    resp = client.post('/olympiad_type/create',
                       json={
                           'olympiad_type': 'Test 0',
                       })
    assert resp.status_code == 200

    olympiad_type: OlympiadType = OlympiadType.query.filter_by(
        olympiad_type_id=resp.json['olympiad_type_id']).one_or_none()
    assert olympiad_type.olympiad_type_id == resp.json['olympiad_type_id']


def test_location_remove(client, test_olympiad_locations):
    from contest.tasks.models import OlympiadLocation
    test_location: OlympiadLocation = test_olympiad_locations[0]
    resp = client.post(f'/location/{test_location.location_id}/remove')
    assert resp.status_code == 200

    assert not test_app.db.session.query(
        OlympiadLocation.query.filter_by(location_id=f'{test_location.location_id}').exists()
    ).scalar()


def test_online_location_create(client):
    from contest.tasks.models import OlympiadLocation
    resp = client.post('/location/create_online',
                       json={
                           'url': 'https://www.example.com',
                       })
    assert resp.status_code == 200
    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.location_id == resp.json['location_id']


def test_location_create_russia(client, test_city):
    from contest.tasks.models import OlympiadLocation
    resp = client.post('/location/create_russia',
                       json={
                           'city_name': f'{test_city.name}',
                           'region_name': f'{test_city.region_name}',
                           'address': 'Test 0',
                       })
    assert resp.status_code == 200
    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.location_id == resp.json['location_id']


def test_location_create_other(client, test_country_native):
    from contest.tasks.models import OlympiadLocation
    resp = client.post('/location/create_other',
                       json={
                           'country_name': f'{test_country_native.name}',
                           'location': 'Test 0',
                       })
    assert resp.status_code == 200
    test_location: OlympiadLocation = OlympiadLocation.query.filter_by(
        location_id=resp.json['location_id']).one_or_none()
    assert test_location.location_id == resp.json['location_id']


def test_get_user_certificate(client, test_simple_contest_with_users, test_user_for_student_contest, test_variant):
    test_simple_contest_with_users[0].result_publication_date = datetime.utcnow() - timedelta(hours=150)
    resp = client.get(
        f'/certificate?'
        f'user_id={test_user_for_student_contest.id}&contest_id={test_simple_contest_with_users[0].contest_id}')
    assert resp.status_code == 200
    assert resp.content_type == 'application/pdf'


def test_get_test_certificate(client, test_certificate_type):
    resp = client.get(f'/certificate/{test_certificate_type.certificates[0].certificate_id}/test')
    assert resp.status_code == 200
    assert resp.content_type == 'application/pdf'


def test_get_test_certificate_long(client, test_certificate_type):
    resp = client.get(f'/certificate/{test_certificate_type.certificates[0].certificate_id}/test'
                      f'?first_name=very_very_very_very_long_name'
                      f'&second_name=very_very_very_very_long_name'
                      f'&middle_name=very_very_very_very_long_name')
    assert resp.status_code == 200
    assert resp.content_type == 'application/pdf'


def test_font_getter(client):
    resp = client.get(f'/fonts')
    assert resp.status_code == 200
    assert 'fonts' in resp.json
    assert resp.json['fonts']


__now = datetime.utcnow()
__academic_year = __now.year if __now.month >= 9 else __now.year - 1
__cert_type_json = {
        'name': 'test cert type',
        'description': 'test cert description'
    }
__cert_json = {
        'certificate_category': 'Winner 1',
        'text_x': 0,
        'text_y': 20,
        'text_width': 100,
        'certificate_year': __academic_year
    }


def test_add_certificate_type(client):
    from contest.tasks.models.certificate import CertificateType

    cert_type_json = __cert_type_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)

    assert resp.status_code == 200
    cert_type_id = resp.json['certificate_type_id']

    cert_type = CertificateType.query.filter_by(certificate_type_id=cert_type_id).one_or_none()
    assert cert_type is not None
    assert resp.json['name'] == cert_type_json['name'] == cert_type.name
    assert resp.json['description'] == cert_type_json['description'] == cert_type.description


def test_patch_certificate_type(client):
    from contest.tasks.models.certificate import CertificateType

    cert_type_json = __cert_type_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    cert_type_json['name'] = 'another test cert type'
    cert_type_json['description'] = 'another test cert description'

    resp = client.patch(f'/certificate_type/{cert_type_id}', json=cert_type_json)
    assert resp.status_code == 204

    cert_type = CertificateType.query.filter_by(certificate_type_id=cert_type_id).one_or_none()
    assert cert_type is not None
    assert cert_type_json['name'] == cert_type.name
    assert cert_type_json['description'] == cert_type.description


def test_delete_certificate_type(client):
    from contest.tasks.models.certificate import CertificateType

    cert_type_json = __cert_type_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    resp = client.delete(f'/certificate_type/{cert_type_id}')
    assert resp.status_code == 204

    cert_type = CertificateType.query.filter_by(certificate_type_id=cert_type_id).one_or_none()
    assert cert_type is None


def test_add_certificate(client):
    from contest.tasks.models.certificate import Certificate

    cert_type_json = __cert_type_json.copy()
    cert_json = __cert_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    assert resp.status_code == 200
    cert_id = resp.json['certificate_id']

    cert = Certificate.query.filter_by(certificate_id=cert_id).one_or_none()
    assert cert is not None
    assert cert_json['certificate_category'] == resp.json['certificate_category'] == cert.certificate_category.value
    assert cert_json['text_x'] == resp.json['text_x'] == cert.text_x
    assert cert_json['text_y'] == resp.json['text_y'] == cert.text_y
    assert cert_json['text_width'] == resp.json['text_width'] == cert.text_width


def test_add_certificate_twice(client):
    cert_type_json = __cert_type_json.copy()
    cert_json = __cert_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    assert resp.status_code == 200

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    assert resp.status_code == 409

    cert_json['certificate_category'] = 'Winner 2'

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    assert resp.status_code == 200


def test_add_certificate_wrong_font(client):
    cert_type_json = __cert_type_json.copy()
    cert_json = __cert_json.copy()
    cert_json['text_style'] = 'ThisFontTotallyDoesNotExist'

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    assert resp.status_code == 409


def test_patch_certificate(client):
    from contest.tasks.models.certificate import Certificate

    cert_type_json = __cert_type_json.copy()
    cert_json = __cert_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    cert_id = resp.json['certificate_id']

    cert_json['text_x'] = 10
    resp = client.patch(f'/certificate/{cert_id}', json=cert_json)
    assert resp.status_code == 204

    cert = Certificate.query.filter_by(certificate_id=cert_id).one_or_none()
    assert cert is not None
    assert cert_json['certificate_category'] == cert.certificate_category.value
    assert cert_json['text_x'] == cert.text_x
    assert cert_json['text_y'] == cert.text_y
    assert cert_json['text_width'] == cert.text_width

    from contest.tasks.models.certificate import Certificate
    assert Certificate.query.count() == 1


def test_add_certificate_used_category(client):

    cert_type_json = __cert_type_json.copy()
    cert_json = __cert_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    cert_json['certificate_category'] = 'Winner 2'
    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    cert_id = resp.json['certificate_id']

    cert_json['certificate_category'] = 'Winner 1'
    resp = client.patch(f'/certificate/{cert_id}', json=cert_json)
    assert resp.status_code == 409

    cert_json['certificate_category'] = 'Winner 3'
    resp = client.patch(f'/certificate/{cert_id}', json=cert_json)
    assert resp.status_code == 204

    from contest.tasks.models.certificate import Certificate
    assert Certificate.query.count() == 2


def test_delete_certificate(client):
    from contest.tasks.models.certificate import Certificate

    cert_type_json = __cert_type_json.copy()
    cert_json = __cert_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    cert_id = resp.json['certificate_id']

    resp = client.delete(f'/certificate/{cert_id}', json=cert_json)
    assert resp.status_code == 204

    cert = Certificate.query.filter_by(certificate_id=cert_id).one_or_none()
    assert cert is None


def test_certificate_post_image(client):
    from contest.tasks.models.certificate import Certificate

    cert_type_json = __cert_type_json.copy()
    cert_json = __cert_json.copy()

    resp = client.post(f'/certificate_type', json=cert_type_json)
    cert_type_id = resp.json['certificate_type_id']

    resp = client.post(f'/certificate_type/{cert_type_id}/certificate', json=cert_json)
    cert_id = resp.json['certificate_id']

    resp = client.post(f'/certificate/{cert_id}/image', data=test_image)
    assert resp.status_code == 204

    cert = Certificate.query.filter_by(certificate_id=cert_id).one_or_none()
    assert cert.certificate_image is not None
