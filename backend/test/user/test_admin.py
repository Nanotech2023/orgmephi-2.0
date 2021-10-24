from . import *


@pytest.fixture
def client(client_admin):
    client_admin.set_prefix('/user/admin')
    yield client_admin


def test_register_internal(client):
    from user.models import User
    resp = client.post('/internal_register', json={'username': 'internal_test', 'password': 'test-password'})
    assert resp.status_code == 200

    user = User.query.filter_by(id=resp.json['id']).one_or_none()
    assert user.id == resp.json['id']
    assert user.username == resp.json['username'] == 'internal_test'
    assert user.role.value == resp.json['role']
    assert user.type.value == resp.json['type'] == 'Internal'


def test_register_internal_exists(client):
    client.post('/internal_register', json={'username': 'internal_test', 'password': 'test-password'})
    resp = client.post('/internal_register', json={'username': 'internal_test', 'password': 'test-password'})
    assert resp.status_code == 409


def test_preregister(client):
    from user.models import User
    resp = client.post('/preregister')
    assert resp.status_code == 200

    user = User.query.filter_by(id=resp.json['registration_number']).one_or_none()
    assert user.id == resp.json['registration_number']
    assert user.username is not None
    assert user.role.value == 'Unconfirmed'
    assert user.type.value == 'PreRegister'
    test_app.password_policy.validate_password(resp.json['password'], user.password_hash)


def test_change_password(client, test_user):
    pre_password_changed = test_user.password_changed

    resp = client.post(f'/password/{test_user.id}', json={'new_password': 'qwertyA*1'})
    assert resp.status_code == 200

    test_app.db.session.refresh(test_user)
    assert test_user.password_changed > pre_password_changed
    test_app.password_policy.validate_password('qwertyA*1', test_user.password_hash)


def test_set_role(client, test_user):
    test_role = 'Unconfirmed'
    if test_user.role.value == 'Unconfirmed':
        test_role = 'Participant'

    resp = client.put(f'/role/{test_user.id}', json={'role': test_role})
    assert resp.status_code == 200

    test_app.db.session.refresh(test_user)
    assert test_user.role.value == test_role


def test_set_type(client, test_user):
    test_type = 'PreRegister'
    if test_user.role.value == 'PreRegister':
        test_type = 'Internal'

    resp = client.put(f'/type/{test_user.id}', json={'type': test_type})
    assert resp.status_code == 200

    test_app.db.session.refresh(test_user)
    assert test_user.type.value == test_type


def test_user_info_patch(client, test_user, test_country_native, test_region, test_city):
    resp = client.patch(f'/personal/{test_user.id}', json=test_user_info)
    assert resp.status_code == 200


def test_university_info_patch(client, test_user, test_country_native, test_region, test_city):
    resp = client.patch(f'/university/{test_user.id}', json=test_university_info)
    assert resp.status_code == 200


def test_school_info_patch(client, test_user, test_country_native, test_region, test_city):
    resp = client.patch(f'/school/{test_user.id}', json=test_school_info)
    assert resp.status_code == 200


def test_add_group(client):
    from user.models import Group
    resp = client.post('/add_group', json={'name': 'test'})
    assert resp.status_code == 200

    grp = Group.query.filter_by(name='test').one_or_none()

    assert grp.id == resp.json['id']
    assert grp.name == resp.json['name'] == 'test'


def test_add_group_exists(client, test_group):
    resp = client.post('/add_group', json={'name': test_group.name})
    assert resp.status_code == 409


def test_remove_group(client, test_group):
    from user.models import Group
    resp = client.post(f'/remove_group/{test_group.id}')
    assert resp.status_code == 200

    assert not test_app.db.session.query(Group.query.filter_by(name='test').exists()).scalar()


def test_user_add_group(client, test_user, test_group):
    resp = client.post(f'/add_member/{test_user.id}', json={'group_id': test_group.id})
    assert resp.status_code == 200
    test_app.db.session.refresh(test_user)
    assert len(test_user.groups) == 1
    assert test_user.groups[0].id == test_group.id
    assert test_user.groups[0].name == test_group.name


# noinspection DuplicatedCode
def test_user_add_group_exists(client, test_user, test_group):
    client.post(f'/add_member/{test_user.id}', json={'group_id': test_group.id})
    resp = client.post(f'/add_member/{test_user.id}', json={'group_id': test_group.id})
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_user_remove_group(client, test_user, test_group):
    client.post(f'/add_member/{test_user.id}', json={'group_id': test_group.id})
    resp = client.post(f'/remove_member/{test_user.id}', json={'group_id': test_group.id})
    assert resp.status_code == 200
    test_app.db.session.refresh(test_user)
    assert len(test_user.groups) == 0


def test_user_remove_group_not_exists(client, test_user, test_group):
    resp = client.post(f'/remove_member/{test_user.id}', json={'group_id': test_group.id})
    assert resp.status_code == 404


def test_photo(client, test_user_school):
    resp = client.get(f'/personal/{test_user_school.id}/photo')
    assert resp.status_code == 404

    resp = client.put(f'/personal/{test_user_school.id}/photo', data=test_image)
    assert resp.status_code == 204

    resp = client.get(f'/personal/{test_user_school.id}/photo')
    assert resp.status_code == 200
