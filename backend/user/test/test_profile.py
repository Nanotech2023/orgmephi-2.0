import datetime

import pytest

from common.testing import get_test_app, OrgMephiTestingClient, DefaultTestConfiguration, reset_db

from user.profile import module


test_app = get_test_app(module, DefaultTestConfiguration())


@pytest.fixture
def client():
    reset_db(test_app)
    with test_app.app.test_client() as client:
        yield OrgMephiTestingClient(client)


test_user_info = {
    "document": {
        "code": "123-456",
        "document_type": "RFPassport",
        "issue_date": "2021-09-02",
        "issuer": "string",
        "number": "123456",
        "series": "4520"
    },
    "dwelling": {
        "city": "test",
        "country": "native",
        "region": "test",
        "rural": True
    },
    "gender": "Male",
    "limitations": {
        "hearing": True,
        "movement": True,
        "sight": True
    },
    "phone": "8 (800) 555 35 35",
    "place_of_birth": "string"
}


test_university_info = {
    "citizenship": "native",
    "city": "test",
    "grade": 1,
    "region": "test",
    "university": {
        "country": "native",
        "university": "test"
    }
}


test_school_info = {
    "grade": 1,
    "location": {
        "city": "test",
        "country": "native",
        "region": "test",
        "rural": True
    },
    "name": "string",
    "number": 0,
    "school_type": "School"
}


def test_auth_info_get(client):
    from user.models import User
    user = User.query.first()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    resp = client.get('/user')
    assert resp.status_code == 200
    assert resp.json['id'] == user.id
    assert resp.json['role'] == user.role.value
    assert resp.json['type'] == user.type.value
    assert resp.json['username'] == user.username


def test_user_info_patch(client):
    client.fake_login()
    resp = client.patch('/personal', json=test_user_info)
    assert resp.status_code == 200


def test_user_info_get(client):
    client.fake_login()
    client.patch('/personal', json=test_user_info)

    resp = client.get('/personal')
    assert resp.status_code == 200
    assert resp.json is not None


def test_university_info_patch(client):
    client.fake_login()
    resp = client.patch('/university', json=test_university_info)
    assert resp.status_code == 200


def test_university_info_get(client):
    client.fake_login()
    client.patch('/university', json=test_university_info)

    resp = client.get('/university')
    assert resp.status_code == 200
    assert resp.json is not None


def test_school_info_patch(client):
    client.fake_login()
    resp = client.patch('/school', json=test_school_info)
    assert resp.status_code == 200


def test_school_info_get(client):
    client.fake_login()
    client.patch('/school', json=test_school_info)

    resp = client.get('/school')
    assert resp.status_code == 200
    assert resp.json is not None


def test_get_groups(client):
    from user.models import User, Group
    user = User.query.first()
    grp = Group(name='test')
    user.groups = [grp]
    test_app.db.session.commit()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    resp = client.get('/groups')
    assert resp.status_code == 200
    assert len(resp.json['groups']) == 1
    assert resp.json['groups'][0]['id'] == grp.id
    assert resp.json['groups'][0]['name'] == grp.name


def test_change_password(client):
    from user.models import User
    user = User.query.first()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    pre_password_changed = user.password_changed

    resp = client.post('/password', json={'old_password': 'test-password', 'new_password': 'qwertyA*1'})
    assert resp.status_code == 200

    user = User.query.filter_by(id=user.id).one_or_none()
    assert user.password_changed > pre_password_changed
    test_app.password_policy.validate_password('qwertyA*1', user.password_hash)


def test_change_password_wrong(client):
    from user.models import User
    user = User.query.first()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    resp = client.post('/password', json={'old_password': 'wrong-password', 'new_password': 'qwertyA*1'})
    assert resp.status_code == 401


def test_change_password_weak(client):
    from user.models import User
    user = User.query.first()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    resp = client.post('/password', json={'old_password': 'test-password', 'new_password': 'qwerty'})
    assert resp.status_code == 400


# noinspection DuplicatedCode
def test_check_filled_school(client):
    from user.models import User, UserInfo, UserTypeEnum
    user = User.query.filter_by(type=UserTypeEnum.school).first()
    user.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                              date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

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
def test_check_filled_university(client):
    from user.models import User, UserInfo, UserTypeEnum
    user = User.query.filter_by(type=UserTypeEnum.university).first()
    user.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                              date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client.patch('/personal', json=test_user_info)

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client.patch('/university', json=test_university_info)

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) == 0


# noinspection DuplicatedCode
def test_check_filled_internal(client):
    from user.models import User, UserInfo, UserTypeEnum
    user = User.query.filter_by(type=UserTypeEnum.internal).first()
    user.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                              date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) > 0

    client.patch('/personal', json=test_user_info)

    resp = client.get('/unfilled')
    assert resp.status_code == 200
    assert len(resp.json['unfilled']) == 0


# noinspection DuplicatedCode
def test_generate_card(client):
    from user.models import User, UserInfo, UserTypeEnum
    user = User.query.filter_by(type=UserTypeEnum.school).first()
    user.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                              date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)
    client.patch('/personal', json=test_user_info)
    client.patch('/school', json=test_school_info)

    resp = client.get('/card')
    assert resp.status_code == 200
    assert resp.mimetype == 'application/pdf'


# noinspection DuplicatedCode
def test_generate_card_unfilled(client):
    from user.models import User, UserInfo, UserTypeEnum
    user = User.query.filter_by(type=UserTypeEnum.school).first()
    user.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                              date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)

    resp = client.get('/card')
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_generate_card_wrong_type(client):
    from user.models import User, UserInfo, UserTypeEnum
    user = User.query.filter_by(type=UserTypeEnum.internal).first()
    user.user_info = UserInfo(first_name='string', middle_name='string', second_name='string',
                              date_of_birth=datetime.date.today(), email='example@example.org')
    test_app.db.session.commit()
    client.fake_login(username=user.username, role=user.role.value, user_id=user.id)
    client.patch('/personal', json=test_user_info)

    resp = client.get('/card')
    assert resp.status_code == 409
