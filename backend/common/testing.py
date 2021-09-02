from typing import Optional
from datetime import timedelta

from flask.testing import FlaskClient

from common import OrgMephiApp, OrgMephiModule


class OrgMephiTestingClient:

    def __init__(self, client: FlaskClient):
        """
        Initialize test client
        :param client: Flask test client (app.test_client())
        """
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
        """
        Get stored flask test client
        :return: Flask test client
        """
        return self._client

    def login(self, url, username, password, remember_me=False, **kwargs):
        """
        Login with auth server
        :param url: URL for login
        :param username: Name of the user to login as
        :param password: User's password
        :param remember_me: Remember me flag
        :param kwargs: Additional arguments passed to FlaskClient.post
        :return: response object
        """
        json = {'username': username, 'password': password, 'remember_me': remember_me}
        resp = self._client.post(url, json=json, **kwargs)
        self._access_csrf = resp.json.get('csrf_access_token', None)
        self._refresh_csrf = resp.json.get('csrf_refresh_token', None)
        return resp

    def fake_login(self, username: str = 'school', role: str = 'Participant', user_id: int = 1):
        """
        Login without an auth server (for testing most of the modules)
        Login will always be successful regardless of server's state, thus user's name and role may differ from actual
            data stored on server
        :param username: Name of the user to login as
        :param role: User's role
        :param user_id: User's id
        """
        from flask_jwt_extended import create_access_token, create_refresh_token, get_csrf_token
        access_token = create_access_token(identity=user_id, additional_claims={"name": username, "role": role})
        refresh_token = create_refresh_token(identity=user_id,
                                             additional_claims={"remember": False, "orig_sub": user_id})
        self.client.set_cookie('', 'access_token_cookie', access_token)
        self.client.set_cookie('', 'refresh_token_cookie', refresh_token)
        self._access_csrf = get_csrf_token(access_token)
        self._refresh_csrf = get_csrf_token(refresh_token)

    def logout(self, *args, **kwargs):
        """
        Logout from server
        :param args: args passed to FlaskClient.post
        :param kwargs: kwargs passed to FlaskClient.post
        :return: response object
        """
        kwargs = self._add_csrf_token(False, kwargs)
        resp = self._client.post(*args, **kwargs)
        self._access_csrf = None
        self._refresh_csrf = None
        return resp

    def fake_logout(self):
        """
        Logout without an auth server (for testing most of the modules)
        """
        self.client.delete_cookie('', 'access_token_cookie')
        self.client.delete_cookie('', 'refresh_token_cookie')
        self._access_csrf = None
        self._refresh_csrf = None

    def refresh(self, *args, **kwargs):
        """
        Refresh login information
        :param args: args passed to FlaskClient.post
        :param kwargs: kwargs passed to FlaskClient.post
        :return: response object
        """
        kwargs = self._add_csrf_token(True, kwargs)
        resp = self._client.post(*args, **kwargs)
        self._access_csrf = resp.json.get('csrf_access_token', None)
        self._refresh_csrf = resp.json.get('csrf_refresh_token', None)
        return resp

    def get(self, *args, **kwargs):
        """
        See FlaskClient.get
        """
        return self._client.get(*args, **kwargs)

    def post(self, *args, **kwargs):
        """
        See FlaskClient.post
        """
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.post(*args, **kwargs)

    def put(self, *args, **kwargs):
        """
        See FlaskClient.put
        """
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.put(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        See FlaskClient.delete
        """
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.delete(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """
        See FlaskClient.patch
        """
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


def _generate_locations(app):
    from user.models import Country, Region, City, University
    country_native = Country(name='native')
    country_foreign = Country(name='foreign')
    region = Region(name='test')
    city = City(name='test')
    city.region = region
    university = University(name='test')
    university.country = country_native

    app.db.session.add(country_native)
    app.db.session.add(country_foreign)
    app.db.session.add(region)
    app.db.session.add(city)
    app.db.session.add(university)
    app.db.session.commit()


def get_test_app(module: OrgMephiModule, config: Optional[object], service_name: Optional[str] = None):
    """
    Generate application for testing
    :param module: Top-level module
    :param config: Configuration class, defaults to DefaultTestConfiguration
    :param service_name: Name of the service, defaults to module.name
    :return: OrgMephiApp object
    """
    if config is None:
        config = DefaultTestConfiguration()
    if service_name is None:
        service_name = module.name
    app = OrgMephiApp(service_name, module, security=True, test_config=config)
    app.app.testing = True
    app.set_current()
    app.prepare()
    _generate_users(app)
    _generate_locations(app)
    return app


def reset_db(app):
    """
    Reset database before/after a test case
    :param app: Test application object
    """
    app.db.drop_all()
    app.db.create_all()
    _generate_locations(app)
    _generate_users(app)


class DefaultTestConfiguration:
    """
    Default configuration for tests
    """
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
    ORGMEPHI_NATIVE_COUNTRY = 'native'
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
    MAIL_DEFAULT_SENDER = 'default@example.org'
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
