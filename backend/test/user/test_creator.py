from . import *


@pytest.fixture
def client(client_creator):
    client_creator.set_prefix('/user/creator')
    yield client_creator


def test_get_auth_info(client, test_user):
    resp = client.get(f'/user/{test_user.id}')
    assert resp.status_code == 200
    assert resp.json['id'] == test_user.id
    assert resp.json['role'] == test_user.role.value
    assert resp.json['type'] == test_user.type.value
    assert resp.json['username'] == test_user.username


# noinspection DuplicatedCode
def test_get_all_auth_info(client, test_user):
    resp = client.get(f'/user/all')
    assert resp.status_code == 200
    assert len(resp.json['users']) > 0
    user_data = next(val for val in resp.json['users'] if val['id'] == test_user.id)

    assert user_data['id'] == test_user.id
    assert user_data['role'] == test_user.role.value
    assert user_data['type'] == test_user.type.value
    assert user_data['username'] == test_user.username


# noinspection DuplicatedCode
def test_get_all_full_info(client, test_user):
    resp = client.get(f'/user_full/all')
    assert resp.status_code == 200
    assert len(resp.json['users']) > 0
    user_data = next(val for val in resp.json['users'] if val['id'] == test_user.id)

    assert user_data['id'] == test_user.id
    assert user_data['role'] == test_user.role.value
    assert user_data['type'] == test_user.type.value
    assert user_data['username'] == test_user.username
    assert 'user_info' in user_data
    assert 'student_info' in user_data
    assert 'school_info' in user_data
    assert 'groups' in user_data
    

def test_user_info_get(client, test_user):
    resp = client.get(f'/personal/{test_user.id}')
    assert resp.status_code == 200
    assert resp.json is not None


def test_university_info_get(client, test_user_university):
    resp = client.get(f'/university/{test_user_university.id}')
    assert resp.status_code == 200
    assert resp.json is not None


def test_school_info_get(client, test_user_school):
    resp = client.get(f'/school/{test_user_school.id}')
    assert resp.status_code == 200
    assert resp.json is not None


def test_get_group(client, test_group):
    resp = client.get(f'/group/{test_group.id}')
    assert resp.status_code == 200
    assert resp.json['id'] == test_group.id
    assert resp.json['name'] == test_group.name


def test_get_group_all(client, test_group):
    resp = client.get(f'/group/all')
    assert resp.status_code == 200
    assert len(resp.json['groups']) > 0
    grp_data = next(val for val in resp.json['groups'] if val['id'] == test_group.id)

    assert grp_data['id'] == test_group.id
    assert grp_data['name'] == test_group.name


# noinspection DuplicatedCode
def test_get_user_groups(client, test_user, test_group):

    test_user.groups = [test_group]
    test_app.db.session.commit()

    resp = client.get(f'/membership/{test_user.id}')
    assert resp.status_code == 200
    assert len(resp.json['groups']) == 1
    assert resp.json['groups'][0]['id'] == test_group.id
    assert resp.json['groups'][0]['name'] == test_group.name


# noinspection DuplicatedCode
def test_get_user_by_group(client, test_user, test_group):

    test_user.groups = [test_group]
    test_app.db.session.commit()

    resp = client.get(f'/user/by-group/{test_group.id}')
    assert resp.status_code == 200
    assert len(resp.json['users']) == 1
    assert resp.json['users'][0]['id'] == test_user.id
