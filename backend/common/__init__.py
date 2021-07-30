from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from contextvars import ContextVar
from typing import Optional, Callable, Any

import os

from .module import OrgMephiModule
from .password import OrgMephiPassword
from .access_levels import OrgMephiAccessLevel


def _path_to_absolute(path):
    if path[0] != '/':
        path = '%s/%s' % (os.getcwd(), path)
    return path


class OrgMephiApp:

    def __init__(self, service_name: str, top_module: OrgMephiModule, security: bool = False,
                 default_config: object = None, test_config: object = None):
        self._service_name: str = service_name
        self._db_prepare_actions: list[Callable] = []
        self._init_app(default_config, test_config)
        self._module: OrgMephiModule = top_module
        self._init_db()
        self._init_jwt()
        self._init_cors()
        self._init_security(security)

    def _init_app(self, default_config: object = None, test_config: object = None):
        self._app = Flask(__name__)
        if default_config is not None:
            self._app.config.from_object(default_config)
        config_var = 'ORGMEPHI_%s_CONFIG' % self._service_name.upper()
        if test_config is not None:
            self._app.config.from_object(test_config)
        elif config_var in os.environ:
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
        self._app.config['JWT_COOKIE_SAMESITE'] = "Strict"
        self._app.config['JWT_CSRF_IN_COOKIES'] = False
        
        self._read_key('SECRET')
        self._read_key('PRIVATE')
        self._read_key('PUBLIC')
        
        self._jwt = JWTManager(self._app)
    
    def _init_cors(self):
        self._cors = CORS(self._app)

    def _init_security(self, security: bool):
        if not security:
            self._password = None
        else:
            prefix = 'ORGMEPHI_%s_PASSWORD_' % self._service_name.upper()
            self._password = OrgMephiPassword(
                hash_schemes=self.app.config[prefix + 'HASH'],
                length=self.app.config[prefix + 'LENGTH'],
                uppercase=self.app.config[prefix + 'UPPERCASE'],
                numbers=self.app.config[prefix + 'NUMBERS'],
                special=self.app.config[prefix + 'SPECIAL'],
                nonletters=self.app.config[prefix + 'NONLETTERS']
            )

    @property
    def app(self):
        return self._app

    @property
    def db(self):
        return self._db

    @property
    def jwt(self):
        return self._jwt

    @property
    def password_policy(self):
        return self._password

    @property
    def config(self):
        return self._app.config

    @property
    def top_module(self):
        return self._module

    def prepare(self):
        last_app = get_current_app()
        self.set_current()
        try:
            api_var = 'ORGMEPHI_%s_API_PATH' % self._service_name.upper()
            if api_var in self._app.config:
                api_path = _path_to_absolute(self._app.config[api_var])
            else:
                api_path = None
            development = self._app.config['ENV'] == 'development'
            self._module.prepare(api_path, development)
            self._app.register_blueprint(self._module.blueprint)
            # swagger-ui does not work with nested blueprints
            for bp in self._module.get_swagger_blueprints():
                self._app.register_blueprint(bp)
            self._db.create_all()
            for act in self._db_prepare_actions:
                act()
        finally:
            _orgmephi_current_app.set(last_app)

    def run(self, **options: Any):
        self._app.run(**options)

    def set_current(self):
        _orgmephi_current_app.set(self)

    def db_prepare_action(self):
        def decorator(f: Callable) -> Callable:
            self._db_prepare_actions.append(f)
            return f
        return decorator


_orgmephi_current_app: ContextVar[Optional[OrgMephiApp]] = ContextVar('orgmephi_current_app', default=None)
_orgmephi_current_module: ContextVar[Optional[OrgMephiModule]] = ContextVar('orgmephi_current_module', default=None)


def get_current_app() -> OrgMephiApp:
    return _orgmephi_current_app.get()


def get_current_flask_app() -> Flask:
    return _orgmephi_current_app.get().app


def get_current_db() -> SQLAlchemy:
    return _orgmephi_current_app.get().db


def get_current_module() -> OrgMephiModule:
    return _orgmephi_current_module.get()
