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


def test_change_password(client):
    from user.models import User
    user = User.query.first()

    pre_password_changed = user.password_changed

    resp = client.post(f'/password/{user.id}', json={'new_password': 'qwertyA*1'})
    assert resp.status_code == 200

    test_app.db.session.refresh(user)
    assert user.password_changed > pre_password_changed
    test_app.password_policy.validate_password('qwertyA*1', user.password_hash)


def test_set_role(client):
    from user.models import User
    test_role = 'Unconfirmed'
    user = User.query.first()
    if user.role.value == 'Unconfirmed':
        test_role = 'Participant'

    resp = client.put(f'/role/{user.id}', json={'role': test_role})
    assert resp.status_code == 200

    test_app.db.session.refresh(user)
    assert user.role.value == test_role


def test_set_type(client):
    from user.models import User
    test_type = 'PreRegister'
    user = User.query.first()
    if user.role.value == 'PreRegister':
        test_type = 'Internal'

    resp = client.put(f'/type/{user.id}', json={'type': test_type})
    assert resp.status_code == 200

    test_app.db.session.refresh(user)
    assert user.type.value == test_type


def test_user_info_patch(client):
    from user.models import User
    user = User.query.first()
    resp = client.patch(f'/personal/{user.id}', json=test_user_info)
    assert resp.status_code == 200


def test_university_info_patch(client):
    from user.models import User
    user = User.query.first()
    resp = client.patch(f'/university/{user.id}', json=test_university_info)
    assert resp.status_code == 200


def test_school_info_patch(client):
    from user.models import User
    user = User.query.first()
    resp = client.patch(f'/school/{user.id}', json=test_school_info)
    assert resp.status_code == 200


def test_add_group(client):
    from user.models import Group
    resp = client.post('/add_group', json={'name': 'test'})
    assert resp.status_code == 200

    grp = Group.query.filter_by(name='test').one_or_none()

    assert grp.id == resp.json['id']
    assert grp.name == resp.json['name'] == 'test'


def test_add_group_exists(client):
    client.post('/add_group', json={'name': 'test'})
    resp = client.post('/add_group', json={'name': 'test'})
    assert resp.status_code == 409


def test_remove_group(client):
    from user.models import Group
    resp = client.post('/add_group', json={'name': 'test'})
    resp = client.post(f'/remove_group/{resp.json["id"]}')

    assert resp.status_code == 200

    grp = Group.query.filter_by(name='test').one_or_none()

    assert grp is None


def test_user_add_group(client):
    from user.models import User
    user = User.query.first()
    resp = client.post('/add_group', json={'name': 'test'})
    grp_id = resp.json['id']
    resp = client.post(f'/add_member/{user.id}', json={'group_id': grp_id})
    assert resp.status_code == 200
    test_app.db.session.refresh(user)
    assert len(user.groups) == 1
    assert user.groups[0].id == grp_id
    assert user.groups[0].name == 'test'


# noinspection DuplicatedCode
def test_user_add_group_exists(client):
    from user.models import User
    user = User.query.first()
    resp = client.post('/add_group', json={'name': 'test'})
    grp_id = resp.json['id']
    client.post(f'/add_member/{user.id}', json={'group_id': grp_id})
    resp = client.post(f'/add_member/{user.id}', json={'group_id': grp_id})
    assert resp.status_code == 409


# noinspection DuplicatedCode
def test_user_remove_group(client):
    from user.models import User
    user = User.query.first()
    resp = client.post('/add_group', json={'name': 'test'})
    grp_id = resp.json['id']
    client.post(f'/add_member/{user.id}', json={'group_id': grp_id})
    resp = client.post(f'/remove_member/{user.id}', json={'group_id': grp_id})
    assert resp.status_code == 200
    test_app.db.session.refresh(user)
    assert len(user.groups) == 0


def test_user_remove_group_not_exists(client):
    from user.models import User
    user = User.query.first()
    resp = client.post('/add_group', json={'name': 'test'})
    resp = client.post(f'/remove_member/{user.id}', json={'group_id': resp.json['id']})
    assert resp.status_code == 404
