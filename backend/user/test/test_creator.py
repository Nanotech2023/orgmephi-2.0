import pytest

from common.testing import get_test_app, OrgMephiTestingClient, reset_db

from user.creator import module


test_app = get_test_app(module)


@pytest.fixture
def client():
    reset_db(test_app)
    with test_app.app.test_client() as client:
        yield OrgMephiTestingClient(client)


def test_get_auth_info(client):
    from user.models import User
    user = User.query.first()
    client.fake_login(role='Creator')

    resp = client.get(f'/user/{user.id}')
    assert resp.status_code == 200
    assert resp.json['id'] == user.id
    assert resp.json['role'] == user.role.value
    assert resp.json['type'] == user.type.value
    assert resp.json['username'] == user.username


# noinspection DuplicatedCode
def test_get_all_auth_info(client):
    from user.models import User
    user = User.query.first()
    client.fake_login(role='Creator')

    resp = client.get(f'/user/all')
    assert resp.status_code == 200
    assert len(resp.json['users']) > 0
    user_data = next(val for val in resp.json['users'] if val['id'] == user.id)

    assert user_data['id'] == user.id
    assert user_data['role'] == user.role.value
    assert user_data['type'] == user.type.value
    assert user_data['username'] == user.username


# noinspection DuplicatedCode
def test_get_all_full_info(client):
    from user.models import User
    user = User.query.first()
    client.fake_login(role='Creator')

    resp = client.get(f'/user_full/all')
    assert resp.status_code == 200
    assert len(resp.json['users']) > 0
    user_data = next(val for val in resp.json['users'] if val['id'] == user.id)

    assert user_data['id'] == user.id
    assert user_data['role'] == user.role.value
    assert user_data['type'] == user.type.value
    assert user_data['username'] == user.username
    assert 'user_info' in user_data
    assert 'student_info' in user_data
    assert 'school_info' in user_data
    assert 'groups' in user_data
    

def test_user_info_get(client):
    from user.models import User
    user = User.query.first()

    client.fake_login(role='Creator')

    resp = client.get(f'/personal/{user.id}')
    assert resp.status_code == 200
    assert resp.json is not None


def test_university_info_get(client):
    from user.models import User
    user = User.query.first()

    client.fake_login(role='Creator')

    resp = client.get(f'/university/{user.id}')
    assert resp.status_code == 200
    assert resp.json is not None


def test_school_info_get(client):
    from user.models import User
    user = User.query.first()

    client.fake_login(role='Creator')

    resp = client.get(f'/school/{user.id}')
    assert resp.status_code == 200
    assert resp.json is not None


def test_get_group(client):
    from user.models import Group
    grp = Group(name='test')
    test_app.db.session.add(grp)
    test_app.db.session.commit()

    client.fake_login(role='Creator')

    resp = client.get(f'/group/{grp.id}')
    assert resp.status_code == 200
    assert resp.json['id'] == grp.id
    assert resp.json['name'] == grp.name


def test_get_group_all(client):
    from user.models import Group
    grp = Group(name='test')
    test_app.db.session.add(grp)
    test_app.db.session.commit()

    client.fake_login(role='Creator')

    resp = client.get(f'/group/all')
    assert resp.status_code == 200
    assert len(resp.json['groups']) > 0
    grp_data = next(val for val in resp.json['groups'] if val['id'] == grp.id)

    assert grp_data['id'] == grp.id
    assert grp_data['name'] == grp.name


# noinspection DuplicatedCode
def test_get_user_groups(client):
    from user.models import Group, User
    user = User.query.first()
    grp = Group(name='test')
    user.groups = [grp]
    test_app.db.session.commit()

    client.fake_login(role='Creator')

    resp = client.get(f'/membership/{user.id}')
    assert resp.status_code == 200
    assert len(resp.json['groups']) == 1
    assert resp.json['groups'][0]['id'] == grp.id
    assert resp.json['groups'][0]['name'] == grp.name


# noinspection DuplicatedCode
def test_get_user_by_group(client):
    from user.models import Group, User
    user = User.query.first()
    grp = Group(name='test')
    user.groups = [grp]
    test_app.db.session.commit()

    client.fake_login(role='Creator')

    resp = client.get(f'/user/by-group/{grp.id}')
    assert resp.status_code == 200
    assert len(resp.json['users']) == 1
    assert resp.json['users'][0]['id'] == user.id
