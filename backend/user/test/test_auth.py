import datetime

import pytest
from flask_jwt_extended import decode_token

from common.testing import get_test_app, OrgMephiTestingClient

from user.auth import module

test_app = get_test_app(module)


def find_cookie(headers, name):
    for val in headers:
        if val[0] == 'Set-Cookie' and val[1].split(sep='=')[0] == name:
            return val[1].split(sep='=')[1].split(sep=';')[0]


def check_jwt(resp, name, role):
    access_cookie = find_cookie(resp.headers, 'access_token_cookie')
    access_jwt = decode_token(access_cookie)
    assert access_jwt['name'] == name
    assert access_jwt['role'] == role

    refresh_cookie = find_cookie(resp.headers, 'refresh_token_cookie')
    refresh_jwt = decode_token(refresh_cookie)
    assert access_jwt['sub'] == refresh_jwt['sub']


def shift_password_change(username):
    from user.models import User
    user = User.query.filter_by(username=username).one_or_none()
    user.password_changed = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    test_app.db.session.commit()


@pytest.fixture
def client():
    with test_app.app.test_client() as client:
        yield OrgMephiTestingClient(client)


def test_login_success(client):
    resp = client.login('/login', 'school', 'test-password')
    assert resp.status_code == 200
    assert 'csrf_access_token' in resp.json
    assert 'csrf_refresh_token' in resp.json

    check_jwt(resp, 'school', 'Participant')

    resp = client.login('/login', 'admin', 'test-password')
    assert resp.status_code == 200
    assert 'csrf_access_token' in resp.json
    assert 'csrf_refresh_token' in resp.json

    check_jwt(resp, 'admin', 'Admin')


def test_login_wrong_username(client):
    resp = client.login('/login', 'not-school', 'test-password')
    assert resp.status_code == 401


def test_login_wrong_password(client):
    resp = client.login('/login', 'school', 'not-test-password')
    assert resp.status_code == 401


def test_logout(client):
    client.login('/login', 'school', 'test-password')
    resp = client.logout('/logout')
    assert resp.status_code == 200


def test_refresh(client):
    shift_password_change('school')
    client.login('/login', 'school', 'test-password')
    resp = client.refresh('/refresh')
    assert resp.status_code == 200

    check_jwt(resp, 'school', 'Participant')


# noinspection DuplicatedCode
def test_impersonate(client):
    shift_password_change('admin')
    shift_password_change('school')

    resp = client.login('/login', 'school', 'test-password')
    school_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']

    resp = client.login('/login', 'admin', 'test-password')
    admin_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']

    assert school_id != admin_id

    resp = client.refresh(f'/impersonate/{school_id}')
    assert resp.status_code == 200
    check_jwt(resp, 'school', 'Participant')

    impersonate_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']
    orig_id = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['orig_sub']
    assert impersonate_id == school_id
    assert orig_id == admin_id


def test_impersonate_no_perms(client):
    shift_password_change('admin')
    shift_password_change('school')

    resp = client.login('/login', 'admin', 'test-password')
    admin_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']

    resp = client.login('/login', 'school', 'test-password')
    school_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']

    assert school_id != admin_id

    resp = client.refresh(f'/impersonate/{admin_id}')
    assert resp.status_code == 403


# noinspection DuplicatedCode
def test_unimpersonate(client):
    shift_password_change('admin')
    shift_password_change('school')

    resp = client.login('/login', 'school', 'test-password')
    school_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']

    resp = client.login('/login', 'admin', 'test-password')
    admin_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']

    assert school_id != admin_id

    client.refresh(f'/impersonate/{school_id}')

    resp = client.refresh(f'/unimpersonate')
    returned_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']

    assert returned_id == admin_id


def test_refresh_old_password(client):
    shift_password_change('school')

    from user.models import User
    client.login('/login', 'school', 'test-password')
    user = User.query.filter_by(username='school').one_or_none()
    user.password_changed = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    test_app.db.session.commit()
    resp = client.refresh('/refresh')
    assert resp.status_code == 401


def test_remember_me(client):
    resp = client.login('/login', 'school', 'test-password', remember_me=False)
    iat = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['iat']
    exp = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['exp']
    assert not decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['remember']
    delta = exp - iat
    resp = client.login('/login', 'school', 'test-password', remember_me=True)
    iat_remember = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['iat']
    exp_remember = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['exp']
    delta_remember = exp_remember - iat_remember
    assert decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['remember']
    assert delta_remember > delta
