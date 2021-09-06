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
        self._prefix = ''

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

    def login(self, full_path, username, password, remember_me=False, **kwargs):
        """
        Login with auth server
        :param full_path: URL for login
        :param username: Name of the user to login as
        :param password: User's password
        :param remember_me: Remember me flag
        :param kwargs: Additional arguments passed to FlaskClient.post
        :return: response object
        """
        json = {'username': username, 'password': password, 'remember_me': remember_me}
        resp = self._client.post(full_path, json=json, **kwargs)
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
        self.client.set_cookie('localhost.local', 'access_token_cookie', access_token)
        self.client.set_cookie('localhost.local', 'refresh_token_cookie', refresh_token)
        self._access_csrf = get_csrf_token(access_token)
        self._refresh_csrf = get_csrf_token(refresh_token)

    def logout(self, full_path, *args, **kwargs):
        """
        Logout from server
        :param full_path: URL for logout
        :param args: args passed to FlaskClient.post
        :param kwargs: kwargs passed to FlaskClient.post
        :return: response object
        """
        kwargs = self._add_csrf_token(False, kwargs)
        resp = self._client.post(full_path, *args, **kwargs)
        self._access_csrf = None
        self._refresh_csrf = None
        return resp

    def fake_logout(self):
        """
        Logout without an auth server (for testing most of the modules)
        """
        self.client.delete_cookie('localhost.local', 'access_token_cookie')
        self.client.delete_cookie('localhost.local', 'refresh_token_cookie')
        self._access_csrf = None
        self._refresh_csrf = None

    def refresh(self, full_path, *args, **kwargs):
        """
        Refresh login information
        :param full_path: URL for refresh
        :param args: args passed to FlaskClient.post
        :param kwargs: kwargs passed to FlaskClient.post
        :return: response object
        """
        kwargs = self._add_csrf_token(True, kwargs)
        resp = self._client.post(full_path, *args, **kwargs)
        self._access_csrf = resp.json.get('csrf_access_token', None)
        self._refresh_csrf = resp.json.get('csrf_refresh_token', None)
        return resp

    def set_prefix(self, prefix: str):
        self._prefix = prefix

    def get(self, path, *args, **kwargs):
        """
        See FlaskClient.get
        """
        return self._client.get(self._prefix + path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        """
        See FlaskClient.post
        """
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.post(self._prefix + path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        """
        See FlaskClient.put
        """
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.put(self._prefix + path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        """
        See FlaskClient.delete
        """
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.delete(self._prefix + path, *args, **kwargs)

    def patch(self, path, *args, **kwargs):
        """
        See FlaskClient.patch
        """
        kwargs = self._add_csrf_token(False, kwargs)
        return self._client.patch(self._prefix + path, *args, **kwargs)


_test_app: Optional[OrgMephiApp] = None


def get_test_app(module: OrgMephiModule):
    """
    Generate application for testing
    :param module: Top-level module
    :return: OrgMephiApp object
    """
    global _test_app
    if _test_app is not None:
        app = _test_app
        app._module = module
    else:
        app = OrgMephiApp('test_app', module, security=True, test_config=DefaultTestConfiguration(), testing=True)
        app.config['JWT_SECRET_KEY'] = 'super-secret'
        _test_app = app
    app.set_current()
    app.prepare()
    reset_db(app)
    return app


def reset_db(app):
    """
    Reset database before/after a test case
    :param app: Test application object
    """
    app.db.drop_all()
    app.db.create_all()


class DefaultTestConfiguration:
    """
    Default configuration for tests
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGMEPHI_API_PATH = 'api'
    JWT_ALGORITHM = 'HS256'
    ORGMEPHI_UNIVERSITY_FILE = None
    ORGMEPHI_COUNTRY_FILE = None
    ORGMEPHI_REGION_FILE = None
    ORGMEPHI_CITY_FILE = None
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
