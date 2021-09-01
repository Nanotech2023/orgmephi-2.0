from typing import Optional
from datetime import timedelta

from flask.testing import FlaskClient

from common import OrgMephiApp, OrgMephiModule


class OrgMephiTestingClient:

    def __init__(self, client: FlaskClient):
        self._client: FlaskClient = client
        self._access_csrf = None
        self._refresh_csrf = None

    def _add_csrf_token(self, refresh: bool, kwargs):
        headers = kwargs.pop('headers', None)
        if headers is None:
            headers = dict()
        headers['X-CSRF-TOKEN'] = self._refresh_csrf if refresh else self._access_csrf
        kwargs['headers'] = headers
        return kwargs

    @property
    def client(self):
        return self._client

    def login(self, *args, **kwargs):
        resp = self._client.post(*args, **kwargs)
        self._access_csrf = resp.json.get('csrf_access_token', None)
        self._refresh_csrf = resp.json.get('csrf_refresh_token', None)
        return resp

    def logout(self, *args, **kwargs):
        kwargs = self._add_csrf_token(False, kwargs)
        resp = self._client.post(*args, **kwargs)
        self._access_csrf = None
        self._refresh_csrf = None
        return resp

    def refresh(self, *args, **kwargs):
        kwargs = self._add_csrf_token(True, kwargs)
        resp = self._client.post(*args, **kwargs)
        self._access_csrf = resp.json.get('csrf_access_token', None)
        self._refresh_csrf = resp.json.get('csrf_refresh_token', None)
        return resp

    def get(self, *args, **kwargs):
        return self._client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.delete(*args, **kwargs)

    def patch(self, *args, **kwargs):
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.patch(*args, **kwargs)


def _generate_users(app):
    from user.models import init_user, UserTypeEnum, UserRoleEnum
    for user_data in [('admin', UserRoleEnum.admin, UserTypeEnum.internal),
                      ('creator', UserRoleEnum.creator, UserTypeEnum.internal),
                      ('school', UserRoleEnum.participant, UserTypeEnum.school),
                      ('university', UserRoleEnum.participant, UserTypeEnum.university)]:
        password_hash = app.password_policy.hash_password('test-password', False)
        user = init_user(user_data[0], password_hash, user_data[1], user_data[2])
        app.db.session.add(user)

    app.db.session.commit()


def get_test_app(module: OrgMephiModule, config: Optional[object], service_name: Optional[str] = None):
    if service_name is None:
        service_name = module.name
    app = OrgMephiApp(service_name, module, security=True, test_config=config)
    app.app.testing = True
    app.set_current()
    app.prepare()
    _generate_users(app)
    return app


class DefaultTestConfiguration:
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_API_PATH = 'api'
    JWT_ALGORITHM = 'RS256'
    ORGMEPHI_PUBLIC_KEY = 'id_rsa.pub'
    ORGMEPHI_PRIVATE_KEY = 'id_rsa'
    ORGMEPHI_UNIVERSITY_FILE = 'user/universities.txt'
    ORGMEPHI_COUNTRY_FILE = 'user/countries.txt'
    ORGMEPHI_REGION_FILE = 'user/regions.txt'
    ORGMEPHI_CITY_FILE = 'user/cities.txt'
    ORGMEPHI_PASSWORD_HASH = 'pbkdf2_sha256'
    ORGMEPHI_PASSWORD_LENGTH = 8
    ORGMEPHI_PASSWORD_UPPERCASE = 1
    ORGMEPHI_PASSWORD_NUMBERS = 1
    ORGMEPHI_PASSWORD_SPECIAL = 1
    ORGMEPHI_PASSWORD_NONLETTERS = 0
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    ORGMEPHI_REMEMBER_ME_TIME = timedelta(days=30)
    ORGMEPHI_CORS_ENABLED = True
    ORGMEPHI_NATIVE_COUNTRY = 'Россия'
    ORGMEPHI_NATIVE_DOCUMENT = 'Паспорт гражданина РФ'
    ORGMEPHI_INTERNATIONAL_DOCUMENT = 'Заграничный паспорт гражданина РФ'
    ORGMEPHI_FOREIGN_DOCUMENT = 'Паспорт гражданина иностранного государства'
    ORGMEPHI_AREA = 'both'
    ORGMEPHI_DAILY_THREAD_LIMIT = 5
    ORGMEPHI_DAILY_MESSAGE_LIMIT = 10
    ORGMEPHI_CONFIRM_EMAIL = False
    ORGMEPHI_ENABLE_PASSWORD_RECOVERY = False
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    ORGMEPHI_MAIL_CONFIRM_KEY = b'\r\xa2\x96\xef\t\x8c\xfe\xa8\x83\xb5\x89\x10\xf4i\x9cL'
    ORGMEPHI_MAIL_CONFIRM_SALT = b'\xcd\x985a\xd5^:-\xcd\x01\xbdN\xac\x9e\xec\xd5'
    ORGMEPHI_MAIL_CONFIRM_EXPIRATION = timedelta(days=1)
    ORGMEPHI_MAIL_CONFIRM_SUBJECT = 'Подтверждение почтового адреса'
    ORGMEPHI_MAIL_RECOVER_SUBJECT = 'Сброс пароля'
    ORGMEPHI_PREREGISTER_PASSWORD_LENGTH = 8
    ORGMEPHI_MAX_FILE_SIZE = 1e7
    ORGMEPHI_CAPTCHA_ENABLE = False
    ORGMEPHI_CAPTCHA_LENGTH = 6
    ORGMEPHI_CAPTCHA_EXPIRATION = timedelta(minutes=5)
