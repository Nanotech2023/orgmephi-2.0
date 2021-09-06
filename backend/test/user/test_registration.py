from . import *
import datetime


@pytest.fixture
def client(client_visitor):
    client_visitor.set_prefix('/user/registration')
    yield client_visitor


def test_get_universities(client, test_university):
    resp = client.get('/info/universities')
    assert resp.status_code == 200
    assert len(resp.json['university_list']) > 0
    assert 'country' in resp.json['university_list'][0]
    assert 'name' in resp.json['university_list'][0]


def test_get_countries(client, test_country_native):
    resp = client.get('/info/countries')
    assert resp.status_code == 200
    assert len(resp.json['country_list']) > 0
    assert 'name' in resp.json['country_list'][0]


def test_get_regions(client, test_region):
    resp = client.get('/info/regions')
    assert resp.status_code == 200
    assert len(resp.json['region_list']) > 0
    assert 'name' in resp.json['region_list'][0]


def test_get_cities(client, test_city):
    resp = client.get('/info/regions')
    region_name = resp.json['region_list'][0]['name']
    resp = client.get(f'/info/cities/{region_name}')
    assert resp.status_code == 200
    assert len(resp.json['city_list']) > 0
    assert 'name' in resp.json['city_list'][0]
    assert resp.json['city_list'][0]['region'] == region_name


def test_registration_school(client):
    from user.models import User
    pre_date = datetime.datetime.utcnow()
    request = {
        "auth_info": {
            "email": "school@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "School"
    }
    resp = client.post('/school', json=request)
    post_date = datetime.datetime.utcnow()
    assert resp.status_code == 200
    assert 'id' in resp.json
    assert resp.json['role'] == 'Participant'
    assert resp.json['type'] == 'School'
    assert resp.json['username'] == 'school@example.com'

    user = User.query.filter_by(id=resp.json['id']).one_or_none()
    assert user is not None
    assert user.id == resp.json['id']
    assert user.username == 'school@example.com'
    assert user.role.value == 'Participant'
    assert user.type.value == 'School'
    assert pre_date < user.registration_date < post_date
    assert user.user_info.email == 'school@example.com'
    assert user.user_info.first_name == 'string'
    assert user.user_info.middle_name == 'string'
    assert user.user_info.second_name == 'string'
    assert user.user_info.date_of_birth == datetime.date.fromisoformat('2021-09-01')


def test_registration_university(client, test_country_native, test_region, test_city, test_university):
    from user.models import User
    pre_date = datetime.datetime.utcnow()
    request = {
        "auth_info": {
            "email": "university@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "University",
        "student_info": {
            "dwelling": {
                "city": "test",
                "country": "native",
                "region": "test",
                "rural": False
            },
            "grade": 5,
            "phone": "8 (800) 555 35 35",
            "university": {
                "university": "test"
            }
        }
    }
    resp = client.post('/university', json=request)
    post_date = datetime.datetime.utcnow()
    assert resp.status_code == 200
    assert 'id' in resp.json
    assert resp.json['role'] == 'Participant'
    assert resp.json['type'] == 'University'
    assert resp.json['username'] == 'university@example.com'

    user = User.query.filter_by(id=resp.json['id']).one_or_none()
    assert user is not None
    assert user.id == resp.json['id']
    assert user.username == 'university@example.com'
    assert user.role.value == 'Participant'
    assert user.type.value == 'University'
    assert pre_date < user.registration_date < post_date
    assert user.user_info.email == 'university@example.com'
    assert user.user_info.first_name == 'string'
    assert user.user_info.middle_name == 'string'
    assert user.user_info.second_name == 'string'
    assert user.user_info.date_of_birth == datetime.date.fromisoformat('2021-09-01')
    assert user.user_info.phone == '8 (800) 555 35 35'
    assert user.user_info.dwelling.russian
    assert user.user_info.dwelling.city_name == 'test'
    assert user.user_info.dwelling.region_name == 'test'
    assert not user.user_info.dwelling.rural
    assert user.student_info.grade == 5
    assert user.student_info.university.known
    assert user.student_info.university.university.name == 'test'


def test_registration_existing(client):
    request = {
        "auth_info": {
            "email": "existing@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "School"
    }
    client.post('/school', json=request)
    resp = client.post('/school', json=request)
    assert resp.status_code == 409


def test_captcha(client):
    from user.models import Captcha
    test_app.config['ORGMEPHI_CAPTCHA_ENABLE'] = True
    resp = client.get('/captcha')
    assert resp.status_code == 200
    answer = Captcha.query.first().answer

    request = {
        "auth_info": {
            "email": "captcha@example.com",
            "password": "qwertyA*1"
        },
        "captcha": answer,
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "School"
    }

    resp = client.post('/school', json=request)
    assert resp.status_code == 200
    assert not test_app.db.session.query(Captcha.query.filter_by(answer=answer).exists()).scalar()

    test_app.config['ORGMEPHI_CAPTCHA_ENABLE'] = False


def test_captcha_fail(client):
    test_app.config['ORGMEPHI_CAPTCHA_ENABLE'] = True

    request = {
        "auth_info": {
            "email": "captcha@example.com",
            "password": "qwertyA*1"
        },
        "captcha": "totally wrong captcha",
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "School"
    }

    resp = client.post('/school', json=request)
    assert resp.status_code == 409

    test_app.config['ORGMEPHI_CAPTCHA_ENABLE'] = False


def test_preregister(client):
    from user.models import User, UserRoleEnum, UserTypeEnum
    test_password = 'test-password'
    password_hash = test_app.password_policy.hash_password(test_password, False)
    user = User(username='unconfirmed', password_hash=password_hash, role=UserRoleEnum.unconfirmed,
                type=UserTypeEnum.pre_register)
    test_app.db.session.add(user)
    test_app.db.session.commit()
    request = {
        "auth_info": {
            "email": "unconfirmed@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_confirm": {
            "password": test_password,
            "registration_number": user.id
        },
        "register_type": "PreUniversity"
    }

    resp = client.post('/school', json=request)
    assert resp.status_code == 200


def test_preregister_wrong_id(client):
    request = {
        "auth_info": {
            "email": "unconfirmed_wrong_id@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_confirm": {
            "password": "test-password",
            "registration_number": 1
        },
        "register_type": "PreUniversity"
    }

    resp = client.post('/school', json=request)
    assert resp.status_code == 404


def test_preregister_wrong_password(client):
    from user.models import User, UserRoleEnum, UserTypeEnum
    test_password = 'test-password'
    password_hash = test_app.password_policy.hash_password(test_password, False)
    user = User(username='unconfirmed', password_hash=password_hash, role=UserRoleEnum.unconfirmed,
                type=UserTypeEnum.pre_register)
    test_app.db.session.add(user)
    test_app.db.session.commit()
    request = {
        "auth_info": {
            "email": "unconfirmed_wrong_pass@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_confirm": {
            "password": "wrong password",
            "registration_number": user.id
        },
        "register_type": "PreUniversity"
    }
    resp = client.post('/school', json=request)
    assert resp.status_code == 401


def test_register_over_unconfirmed(client):
    from user.models import User, UserRoleEnum, UserTypeEnum, UserInfo
    test_password = 'test-password'
    password_hash = test_app.password_policy.hash_password(test_password, False)
    user = User(username='replace@example.com', password_hash=password_hash, role=UserRoleEnum.unconfirmed,
                type=UserTypeEnum.school)
    user.registration_date = datetime.date.today() - datetime.timedelta(days=365)
    user.user_info = UserInfo()
    user.user_info.first_name = 'Wrong first name'
    user.user_info.email = 'Wrong first name'
    test_app.db.session.add(user)
    test_app.db.session.commit()
    request = {
        "auth_info": {
            "email": "replace@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "PreUniversity"
    }
    resp = client.post('/school', json=request)
    assert resp.status_code == 200

    user = User.query.filter_by(id=user.id).one_or_none()
    assert user.user_info.first_name == 'string'


def test_email_confirm(client):
    from user.models import User
    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = True
    with test_app.mail.record_messages() as outbox:
        request = {
            "auth_info": {
                "email": "confirm@example.com",
                "password": "qwertyA*1"
            },
            "personal_info": {
                "date_of_birth": "2021-09-01",
                "first_name": "string",
                "middle_name": "string",
                "second_name": "string"
            },
            "register_type": "School"
        }
        resp = client.post('/school', json=request)
        assert resp.status_code == 200
        assert len(outbox) == 1
        assert outbox[0].recipients[0] == 'confirm@example.com'
        token = test_app.config['TESTING_LAST_EMAIL_TOKEN']
        assert token in outbox[0].body
        if outbox[0].html is not None:
            assert token in outbox[0].html

        user = User.query.filter_by(username='confirm@example.com').one_or_none()
        assert user.role.value == 'Unconfirmed'

        resp = client.post(f'/confirm/{token}')
        assert resp.status_code == 204
        user = User.query.filter_by(username='confirm@example.com').one_or_none()
        assert user.role.value == 'Participant'
        resp = client.post(f'/confirm/{token}')
        assert resp.status_code == 404

    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = False


def test_email_confirm_wrong(client):
    from user.models import User
    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = True
    request = {
        "auth_info": {
            "email": "confirm_wrong@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "School"
    }
    client.post('/school', json=request)
    token = test_app.config['TESTING_LAST_EMAIL_TOKEN']

    user = User.query.filter_by(username='confirm_wrong@example.com').one_or_none()
    test_app.db.session.delete(user)
    test_app.db.session.commit()

    resp = client.post(f'/confirm/{token}')
    assert resp.status_code == 404

    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = False


def test_email_confirm_invalid(client):
    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = True

    resp = client.post(f'/confirm/invalid_token')
    assert resp.status_code == 404

    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = False


def test_recover_password(client):
    from user.models import User
    test_app.config['ORGMEPHI_ENABLE_PASSWORD_RECOVERY'] = True
    with test_app.mail.record_messages() as outbox:
        request = {
            "auth_info": {
                "email": "forgot@example.com",
                "password": "qwertyA*1"
            },
            "personal_info": {
                "date_of_birth": "2021-09-01",
                "first_name": "string",
                "middle_name": "string",
                "second_name": "string"
            },
            "register_type": "School"
        }
        client.post('/school', json=request)

        resp = client.client.post('/user/registration/forgot/forgot@example.com')
        assert resp.status_code == 204
        assert len(outbox) == 1
        assert outbox[0].recipients[0] == 'forgot@example.com'
        token = test_app.config['TESTING_LAST_EMAIL_TOKEN']
        assert token in outbox[0].body
        if outbox[0].html is not None:
            assert token in outbox[0].html

        user = User.query.filter_by(username='forgot@example.com').one_or_none()
        user.password_changed = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
        test_app.db.session.commit()

        request = {'password': 'qwertyA*2'}
        resp = client.client.post(f'/user/registration/recover/{token}', json=request)
        assert resp.status_code == 204
        user = User.query.filter_by(username='forgot@example.com').one_or_none()
        test_app.password_policy.validate_password('qwertyA*2', user.password_hash)

        resp = client.client.post(f'/user/registration/recover/{token}', json=request)
        assert resp.status_code == 404

    test_app.config['ORGMEPHI_ENABLE_PASSWORD_RECOVERY'] = False


def test_token_wrong_type(client):
    test_app.config['ORGMEPHI_ENABLE_PASSWORD_RECOVERY'] = True
    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = True
    request = {
        "auth_info": {
            "email": "wrong_type@example.com",
            "password": "qwertyA*1"
        },
        "personal_info": {
            "date_of_birth": "2021-09-01",
            "first_name": "string",
            "middle_name": "string",
            "second_name": "string"
        },
        "register_type": "School"
    }
    client.post('/school', json=request)

    client.client.post('/forgot/wrong_type@example.com')
    token = test_app.config['TESTING_LAST_EMAIL_TOKEN']

    resp = client.client.post(f'/confirm/{token}')
    assert resp.status_code == 404

    test_app.config['ORGMEPHI_CONFIRM_EMAIL'] = False
    test_app.config['ORGMEPHI_ENABLE_PASSWORD_RECOVERY'] = False
