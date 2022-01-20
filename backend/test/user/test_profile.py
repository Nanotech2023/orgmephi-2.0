from . import *
import datetime


@pytest.fixture
def client(client_school):
    client_school.set_prefix('/user/profile')
    yield client_school


@pytest.fixture
def client_uni(client_university):
    client_university.set_prefix('/user/profile')
    yield client_university


@pytest.fixture
def client_adm(client_admin):
    client_admin.set_prefix('/user/profile')
    yield client_admin


def test_auth_info_get(client, test_user_school):
    resp = client.get('/user')
    assert resp.status_code == 200
    assert resp.json['id'] == test_user_school.id
    assert resp.json['role'] == test_user_school.role.value
    assert resp.json['type'] == test_user_school.type.value
    assert resp.json['username'] == test_user_school.username


def test_user_info_patch(client, test_country_native, test_region, test_city):
    resp = client.patch('/personal', json=test_user_info)
    assert resp.status_code == 200


def test_user_info_limitations_patch(client, test_country_native, test_region, test_city):
    resp = client.patch('/personal/limitations', json=test_user_info['limitations'])
    assert resp.status_code == 200


def test_user_info_dwellings_patch(client, test_country_native, test_region, test_city):
    resp = client.patch('/personal/dwelling', json=test_user_info['dwelling'])
    assert resp.status_code == 200


def test_user_info_phone_number_patch(client, test_country_native, test_region, test_city):
    resp = client.patch('/personal/phone_number', json={
        "phone": "8 (800) 555 35 35"
    })
    assert resp.status_code == 200


def test_user_info_personal_patch(client, test_country_native, test_region, test_city):
    from user.models import GenderEnum
    resp = client.patch('/personal/personal', json={
        "first_name": "first_name",
        "middle_name": "middle_name",
        "second_name": "second_name",
        "gender": GenderEnum.male.value,
        "place_of_birth": "test place",
    })
    assert resp.status_code == 200


def test_user_info_get(client, test_country_native, test_region, test_city):
    client.patch('/personal', json=test_user_info)

    resp = client.get('/personal')
    assert resp.status_code == 200
    assert resp.json is not None


def test_university_info_patch(client, test_country_native, test_region, test_city):
    resp = client.patch('/university', json=test_university_info)
    assert resp.status_code == 200


def test_university_info_get(client, test_country_native, test_region, test_city):
    client.patch('/university', json=test_university_info)

    resp = client.get('/university')
    assert resp.status_code == 200
    assert resp.json is not None


def test_school_info_patch(client, test_country_native, test_region, test_city):
    resp = client.patch('/school', json=test_school_info)
    assert resp.status_code == 200


def test_school_info_get(client, test_country_native, test_region, test_city):
    client.patch('/school', json=test_school_info)

    resp = client.get('/school')
    assert resp.status_code == 200
    assert resp.json is not None


def test_get_groups(client, test_user_school, test_group):

    test_user_school.groups = [test_group]
    test_app.db.session.commit()

    resp = client.get('/groups')
    assert resp.status_code == 200
    assert len(resp.json['groups']) == 1
    assert resp.json['groups'][0]['id'] == test_group.id
    assert resp.json['groups'][0]['name'] == test_group.name


def test_change_password(client, test_user_school):
    pre_password_changed = test_user_school.password_changed
    resp = client.post('/password', json={'old_password': 'test-password', 'new_password': 'qwertyA*1'})
    assert resp.status_code == 200
    test_app.db.session.refresh(test_user_school)
    assert test_user_school.password_changed > pre_password_changed
    test_app.password_policy.validate_password('qwertyA*1', test_user_school.password_hash)


def test_change_password_wrong(client, test_user_school):
    resp = client.post('/password', json={'old_password': 'wrong-password', 'new_password': 'qwertyA*1'})
    assert resp.status_code == 401


def test_change_password_weak(client, test_user_school):
    resp = client.post('/password', json={'old_password': 'test-password', 'new_password': 'qwerty'})
    assert resp.status_code == 400


# noinspection DuplicatedCode
def test_check_filled_school(client, test_user_school, test_country_native, test_region, test_city):
    from user.models import UserInfo

    test_user_school.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                                          date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client.patch('/personal', json=test_user_info)

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client.patch('/school', json=test_school_info)

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) == 0


# noinspection DuplicatedCode
def test_check_filled_university(client_uni, test_user_university, test_country_native, test_region, test_city):
    from user.models import UserInfo

    test_user_university.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                                              date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()

    resp = client_uni.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client_uni.patch('/personal', json=test_user_info)

    resp = client_uni.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client_uni.patch('/university', json=test_university_info)

    resp = client_uni.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) == 0


# noinspection DuplicatedCode
def test_check_filled_internal(client_adm, test_user_admin, test_country_native, test_region, test_city):
    from user.models import UserInfo

    test_user_admin.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                                         date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client_adm.fake_login(username=test_user_admin.username, role=test_user_admin.role.value, user_id=test_user_admin.id)

    resp = client_adm.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client_adm.patch('/personal', json=test_user_info)

    resp = client_adm.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) == 0


# noinspection DuplicatedCode
def test_generate_card(client, test_user_school, test_country_native, test_region, test_city):
    from user.models import UserInfo

    test_user_school.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                                          date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=test_user_school.username, role=test_user_school.role.value, user_id=test_user_school.id)
    client.patch('/personal', json=test_user_info)
    client.patch('/school', json=test_school_info)

    resp = client.get('/card')
    assert resp.status_code == 200
    assert resp.mimetype == 'application/pdf'


# noinspection DuplicatedCode
def test_generate_card_unfilled(client, test_user_school):
    from user.models import UserInfo

    test_user_school.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                                          date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=test_user_school.username, role=test_user_school.role.value, user_id=test_user_school.id)

    resp = client.get('/card')
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_generate_card_wrong_type(client_adm, test_user_admin):
    from user.models import UserInfo

    test_user_admin.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                                         date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client_adm.fake_login(username=test_user_admin.username, role=test_user_admin.role.value, user_id=test_user_admin.id)
    client_adm.patch('/personal', json=test_user_info)

    resp = client_adm.get('/card')
    assert resp.status_code == 409


def test_photo(client):
    resp = client.get('/photo')
    assert resp.status_code == 404

    resp = client.put('/photo', data=test_image)
    assert resp.status_code == 204

    resp = client.get('/photo')
    assert resp.status_code == 200
