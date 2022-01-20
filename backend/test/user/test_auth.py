from . import *

import datetime
from flask_jwt_extended import decode_token


@pytest.fixture
def client(client_visitor):
    client_visitor.set_prefix('/user/auth')
    yield client_visitor


def find_cookie(headers, name):
    for val in headers:
        if val[0] == 'Set-Cookie' and val[1].split(sep='=')[0] == name:
            return val[1].split(sep='=')[1].split(sep=';')[0]


def check_jwt(resp, sub, name, role):
    access_cookie = find_cookie(resp.headers, 'access_token_cookie')
    access_jwt = decode_token(access_cookie)
    assert access_jwt['sub'] == sub
    assert access_jwt['name'] == name
    assert access_jwt['role'] == role

    refresh_cookie = find_cookie(resp.headers, 'refresh_token_cookie')
    refresh_jwt = decode_token(refresh_cookie)
    assert access_jwt['sub'] == refresh_jwt['sub']


def shift_password_change(user):
    user.password_changed = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
    test_app.db.session.commit()


def test_login_success(client, test_user_school, test_user_admin):
    resp = client.login('/user/auth/login', test_user_school.username, 'test-password')
    assert resp.status_code == 200
    assert 'csrf_access_token' in resp.json
    assert 'csrf_refresh_token' in resp.json
    assert resp.json['confirmed']

    check_jwt(resp, test_user_school.id, test_user_school.username, 'Participant')

    resp = client.login('/user/auth/login', test_user_admin.username, 'test-password')
    assert resp.status_code == 200
    assert 'csrf_access_token' in resp.json
    assert 'csrf_refresh_token' in resp.json
    assert resp.json['confirmed']

    check_jwt(resp, test_user_admin.id, test_user_admin.username, 'Admin')

    resp = client.login('/user/auth/login', test_user_school.username.upper(), 'test-password')
    assert resp.status_code == 200
    assert 'csrf_access_token' in resp.json
    assert 'csrf_refresh_token' in resp.json
    assert resp.json['confirmed']

    check_jwt(resp, test_user_school.id, test_user_school.username, 'Participant')


def test_login_success_legacy(client, test_user_school, test_user_admin):
    test_user_school.password_hash = '$org-legacy$salt$fb47635b5776eb5d9da730578b4800c9'
    test_app.db.session.commit()
    resp = client.login('/user/auth/login', test_user_school.username, 'test-password')
    assert resp.status_code == 200
    assert 'csrf_access_token' in resp.json
    assert 'csrf_refresh_token' in resp.json
    assert resp.json['confirmed']

    check_jwt(resp, test_user_school.id, test_user_school.username, 'Participant')


def test_login_wrong_username(client):
    resp = client.login('/user/auth/login', 'wrong-username', 'test-password')
    assert resp.status_code == 401


def test_login_wrong_password(client, test_user_school):
    resp = client.login('/user/auth/login', test_user_school.username, 'not-test-password')
    assert resp.status_code == 401


def test_login_wrong_password_legacy(client, test_user_school):
    test_user_school.password_hash = '$org-legacy$salt$fb47635b5776eb5d9da730578b4800c9'
    test_app.db.session.commit()
    resp = client.login('/user/auth/login', test_user_school.username, 'not-test-password')
    assert resp.status_code == 401


def test_logout(client_school):
    resp = client_school.logout('/user/auth/logout')
    assert resp.status_code == 200


def test_refresh(client_school, test_user_school):
    resp = client_school.refresh('/user/auth/refresh')
    assert resp.status_code == 200
    assert resp.json['confirmed']

    check_jwt(resp, test_user_school.id, 'school', 'Participant')


# noinspection DuplicatedCode
def test_impersonate(client_admin, test_user_admin, test_user_school):

    resp = client_admin.refresh(f'/user/auth/impersonate/{test_user_school.id}')
    assert resp.status_code == 200
    check_jwt(resp, test_user_school.id, 'school', 'Participant')
    assert resp.json['confirmed']

    impersonate_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']
    orig_id = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['orig_sub']
    assert impersonate_id == test_user_school.id
    assert orig_id == test_user_admin.id


def test_impersonate_no_perms(client_school, test_user_admin):
    resp = client_school.refresh(f'/user/auth/impersonate/{test_user_admin.id}')
    assert resp.status_code == 403


# noinspection DuplicatedCode
def test_unimpersonate(client_admin, test_user_admin, test_user_school):
    client_admin.refresh(f'/user/auth/impersonate/{test_user_school.id}')
    resp = client_admin.refresh(f'/user/auth/unimpersonate')
    assert resp.status_code == 200
    assert resp.json['confirmed']
    returned_id = decode_token(find_cookie(resp.headers, 'access_token_cookie'))['sub']
    assert returned_id == test_user_admin.id


def test_refresh_old_password(client_school, test_user_school):
    test_user_school.password_changed = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    test_app.db.session.commit()
    resp = client_school.refresh('/user/auth/refresh')
    assert resp.status_code == 401


def test_remember_me(client, test_user_school):
    resp = client.login('/user/auth/login', test_user_school.username, 'test-password', remember_me=False)
    iat = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['iat']
    exp = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['exp']
    assert not decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['remember']
    delta = exp - iat
    resp = client.login('/user/auth/login', test_user_school.username, 'test-password', remember_me=True)
    iat_remember = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['iat']
    exp_remember = decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['exp']
    delta_remember = exp_remember - iat_remember
    assert decode_token(find_cookie(resp.headers, 'refresh_token_cookie'))['remember']
    assert delta_remember > delta
