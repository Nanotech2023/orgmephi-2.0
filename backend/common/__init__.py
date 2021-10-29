import functools
import io

from flask import Flask, Config
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from contextvars import ContextVar
from typing import Optional, Callable, Any

import os

from .errors import MediaError, NotFound
from .module import OrgMephiModule, OrgMephiArea, org_mephi_area_by_name
from .password import OrgMephiPassword
from .access_levels import OrgMephiAccessLevel


def _path_to_absolute(path):
    if path[0] != '/':
        path = '%s/%s' % (os.getcwd(), path)
    return path


class OrgMephiApp:
    """
    Application class
    """

    def __init__(self, service_name: str, top_module: OrgMephiModule, security: bool = False,
                 default_config: object = None, test_config: object = None, testing: bool = False):
        """
        Create an application object

        To load custom configuration file put configuration file path into ORGMEPHI_<service_name>_CONFIG
            (all uppercase) environment variable

        :param service_name: Name of this service
        :param top_module: Top-level module
        :param security: If True application will initialize additional security components (currently this only
                         includes password operations)
        :param default_config: Configuration object with default settings (see flask.Flask.config.from_object)
        :param test_config: Configuration object with test settings (flask.Flask.config.from_object), applied after
                            (on top of) default configuration
        """
        self._service_name: str = service_name
        self._db_prepare_actions: list[Callable] = []
        self._init_app(default_config, test_config)
        self._module: OrgMephiModule = top_module
        self.app.testing = testing
        self._init_db()
        self._init_jwt()
        self._init_cors()
        self._init_security(security)
        self._init_mail()
        self._init_media()

    @property
    def name(self) -> str:
        """
        Service name
        :return: Service name of self
        """
        return self._service_name

    @property
    def app(self) -> Flask:
        """
        Flask application instance
        :return: Flask application instance of self
        """
        return self._app

    @property
    def db(self) -> SQLAlchemy:
        """
        Database object
        :return: Database object of self
        """
        return self._db

    @property
    def jwt(self) -> JWTManager:
        """
        JWT manager object
        :return: JWT manager of self
        """
        return self._jwt

    @property
    def mail(self) -> Mail:
        """
        Mail object
        :return: Mail object of self
        """
        return self._mail

    @property
    def password_policy(self) -> OrgMephiPassword:
        """
        Password policy
        :return: Password policy of self
        """
        return self._password

    @property
    def config(self) -> Config:
        """
        Configuration object (see flask.Config)
        :return: Configuration of self
        """
        return self._app.config

    @property
    def top_module(self) -> OrgMephiModule:
        """
        Top-level module
        :return: Top-level module of self
        """
        return self._module

    def db_prepare_action(self) -> Callable:
        """
        Decorator factory to set actions that must be executed to initialize database right after it's creation
                (e.g. populate reference tables)
        :return: Prepare db action decorator
        """
        def decorator(f: Callable) -> Callable:
            """
            Decorator to set actions that must be executed to initialize database right after it's creation
                (e.g. populate reference tables)
            :param f: Function to decorate
            :return: Provided function
            """
            self._db_prepare_actions.append(f)
            return f
        return decorator

    def set_current(self):
        """
        Sets self as a current application so that get_current_app will return self

        This is normally only needed if you are going to call get_current_app from within a view function,
        because self will be set as current automatically while executing OrgMephiApp.prepare
        """
        self.app.app_context().push()

    def prepare(self):
        """
        Prepares self for the execution

        Loads views, loads api, initializes swagger-ui, registers paths, creates database,
            prepares database (see OrgMephiApp.db_prepare_action)
        """
        with self.app.app_context():
            api_path = None
            api_var = 'ORGMEPHI_API_PATH'
            area_var = 'ORGMEPHI_AREA'
            if api_var in self._app.config:
                api_path = _path_to_absolute(self._app.config[api_var])
            development = self._app.config['ENV'] == 'development'
            area = org_mephi_area_by_name[self._app.config[area_var]]
            if self._module.appropriate_area(area):
                self._module.prepare(api_path, development, self._module, area)
                self._app.register_blueprint(self._module.blueprint)
                # swagger-ui does not work with nested blueprints
                for bp in self._module.get_swagger_blueprints():
                    self._app.register_blueprint(bp)
            self._db.create_all()
            for act in self._db_prepare_actions:
                act()

    def run(self, **options: Any):
        """
        Runs self
        :param options: Flask.run options (see flask.Flask.run)
        """
        self._app.run(**options)

    @property
    def store_manager(self):
        """
        Get media store manager
        :return:
        """
        return self._store_manager

    def get_media_store_id(self, key: str):
        """
        Get media store id for this app
        :param key: Original store key
        :return: Media store id for this app
        """
        return self._media_key(key)

    def io_to_media(self, store_key: str, obj: object, field: str, data: io, cls, mimetype: str = None):
        """
        Convert bytes to a media object
        :param store_key: Key for media store
        :param obj: Model object
        :param field: Field to hold media data
        :param data: Media bytes
        :param cls: Media data class
        :param mimetype: media content type
        """
        from common import get_current_app
        with self._store_manager:
            media = cls.create_from(
                attachable=data,
                store_id=self.get_media_store_id(store_key),
                content_type=mimetype
            )
            setattr(obj, field, media)

    def media_to_io(self, media) -> io:
        """
        Convert media object to io
        :param media: Media object
        :return: io with media bytes
        """
        from common import get_current_app
        if media is None:
            raise NotFound('', 'media')
        with self._store_manager:
            store = media.get_store()
            return store.open(media.path)

    def store_media(self, store_key: str, obj: object, field: str, cls):
        """
        Store media content from flask request
        :param store_key: Key for media store
        :param obj: Model object
        :param field: Field to hold media data
        :param cls: Media data class
        :return: Created media object
        """
        from flask import request
        self.io_to_media(store_key, obj, field, io.BytesIO(request.data), cls)

    def send_media(self, media):
        """
        Send media content
        :param media: Media object
        :return: Flask response
        """
        from flask import send_file
        return send_file(self.media_to_io(media), media.content_type)

    def _init_app(self, default_config: object = None, test_config: object = None):
        self._app = Flask(__name__, root_path=os.getcwd())
        self._app.config['ORGMEPHI_APP'] = self
        if default_config is not None:
            self._app.config.from_object(default_config)
        config_var = 'ORGMEPHI_%s_CONFIG' % self._service_name.upper()
        if test_config is not None:
            self._app.config.from_object(test_config)
        elif config_var in os.environ:
            path = _path_to_absolute(os.environ[config_var])
            os.environ[config_var] = path
            self._app.config.from_envvar(config_var)

    def _init_db(self):
        self._db = SQLAlchemy(self._app)

    def _read_key(self, key_type):
        var_name = 'ORGMEPHI_%s_KEY' % key_type.upper()
        jwt_var_name = 'JWT_%s_KEY' % key_type.upper()
        if var_name in self._app.config:
            key_path = _path_to_absolute(self._app.config[var_name])
            with open(key_path, 'r') as key_file:
                key = key_file.read()
            self._app.config[jwt_var_name] = key

    def _init_jwt(self):
        self._app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
        self._app.config['JWT_CSRF_IN_COOKIES'] = False
        if 'ORGMEPHI_JWT_SAMESITE' in self._app.config and self._app.config['ORGMEPHI_JWT_SAMESITE'] is not None:
            self._app.config['JWT_COOKIE_SAMESITE'] = self._app.config['ORGMEPHI_JWT_SAMESITE']
        else:
            self._app.config['JWT_COOKIE_SAMESITE'] = "Strict"

        self._app.config['JWT_COOKIE_SECURE'] = self.config['ENV'] != 'development'

        self._read_key('SECRET')
        self._read_key('PRIVATE')
        self._read_key('PUBLIC')
        
        self._jwt = JWTManager(self._app)
    
    def _init_cors(self):
        if self._app.config['ORGMEPHI_CORS_ENABLED']:
            self._app.config['CORS_SUPPORTS_CREDENTIALS'] = True
            self._cors = CORS(self._app)
        else:
            self._cors = None

    def _init_security(self, security: bool):
        if not security:
            self._password = None
        else:
            self._password = OrgMephiPassword(
                hash_schemes=self.app.config['ORGMEPHI_PASSWORD_HASH'],
                length=self.app.config['ORGMEPHI_PASSWORD_LENGTH'],
                uppercase=self.app.config['ORGMEPHI_PASSWORD_UPPERCASE'],
                numbers=self.app.config['ORGMEPHI_PASSWORD_NUMBERS'],
                special=self.app.config['ORGMEPHI_PASSWORD_SPECIAL'],
                nonletters=self.app.config['ORGMEPHI_PASSWORD_NONLETTERS']
            )

    def _init_mail(self):
        self._mail = Mail(self._app)

    def _media_key(self, key):
        return f'{self.config["ORGMEPHI_MEDIA_KEY"]}_{key}'

    def _init_media(self):
        from sqlalchemy_media import StoreManager, FileSystemStore
        media_stores: dict = self.config['ORGMEPHI_MEDIA_STORES']
        root_path = self.config['ORGMEPHI_MEDIA_ROOT_PATH']
        if not os.path.isabs(root_path):
            root_path = os.path.join(os.path.abspath(self._app.root_path), root_path)
        for val in media_stores.items():
            StoreManager.register(
                self._media_key(val[0]),
                functools.partial(FileSystemStore, f'{root_path}/{val[1]}', f'{val[1]}'),
                default=False
            )
        self._store_manager = StoreManager(self._db.session, delete_orphan=True)


_orgmephi_current_module: ContextVar[Optional[OrgMephiModule]] = ContextVar('orgmephi_current_module', default=None)


def get_current_app() -> OrgMephiApp:
    """
    Get current application
    :return: Current application
    """
    from flask import current_app
    return current_app.config.get('ORGMEPHI_APP', None)


def get_current_flask_app() -> Flask:
    """
    Get flask app of current application, synonym to get_current_app().app
    :return: Flask app of current application
    """
    return get_current_app().app


def get_current_db() -> SQLAlchemy:
    """
    Get database object of current application, synonym to get_current_app().db
    :return: Database object of current application
    :return:
    """
    return get_current_app().db


def get_current_module() -> OrgMephiModule:
    """
    Get current module (i.e. a module that is currently being initialized)
    :return: Current module
    """
    return _orgmephi_current_module.get()
