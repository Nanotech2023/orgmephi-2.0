import importlib
from functools import wraps

from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from marshmallow import Schema
from typing import Type
from flask import Blueprint, send_file
from typing import Callable, Any, Optional

from .access_levels import OrgMephiAccessLevel


def _enum_allowed_values(enum_type, validator):
    from marshmallow import validate
    if isinstance(validator, validate.OneOf):
        return {v for v in validator.choices}
    if isinstance(validator, validate.And):
        return _enum_allowed_values_list(enum_type, validator.validators)
    return set(enum_type)


def _enum_allowed_values_list(enum_type, validators):
    allowed = set(enum_type)
    for val in validators:
        dd = _enum_allowed_values(enum_type, val)
        allowed = allowed & _enum_allowed_values(enum_type, val)
    return allowed


def _enum2properties(self, field, **kwargs):
    import marshmallow_enum
    if isinstance(field, marshmallow_enum.EnumField):
        allowed = _enum_allowed_values_list(field.enum, field.validators)
        return {'type': 'string', 'enum': [m.value for m in field.enum if m in allowed]}
    return {}


class OrgMephiModule:
    """
    Application module
    """
    def __init__(self, name: str, package: str, access_level: Optional[OrgMephiAccessLevel],
                 api_file: Optional[str] = None):
        """
        Create a new module
        :param name: name of the module (equals to its path prefix)
        :param package: package representing this module (usually should be set to __package__)
        :param access_level: access level of this module, only users with this level or higher will be able to access
                             module's views. Alternatively, can be set to None to manually configure allowed roles with
                             jwt_required_role.
        :param api_file: name of the file with this module's api. If omitted (or set to None), requests will not be
                         automatically verified in this module and swagger ui will not be generated
        """
        self._name = name
        self._package = package
        self._blueprint: Optional[Blueprint] = None
        self._access_level = access_level if access_level is not None else OrgMephiAccessLevel.visitor
        self._modules: list[OrgMephiModule] = []
        self._parent: Optional[OrgMephiModule] = None
        self._openapi = None
        self._swagger = None
        self._api_file = api_file

    @property
    def name(self) -> str:
        """
        Name of self
        :return: Name of self
        """
        return self._name

    @property
    def blueprint(self) -> Blueprint:
        """
        Blueprint of self (see flask.Blueprint)
        :return: Blueprint of self
        """
        return self._blueprint

    @property
    def swagger(self) -> Blueprint:
        """
        Swagger blueprint of self (see flask.Blueprint)
        :return: Swagger blueprint of self
        """
        return self._swagger

    def get_full_name(self, top=None) -> str:
        """
        Full name of self, i.e. name that includes all parent names in format <parent.full_name>_<self.name>
        :return: Full name of self
        """
        return '_'.join(self._get_parents(top))

    def get_prefix(self, top=None) -> str:
        """
        URL prefix of self, equal to <this module prefix>/<child module name> except for top-level module, that has no
            prefix
        :return: URL prefix of self
        """
        prefix = '/'.join(self._get_parents(top)[1:])
        return '' if prefix == '' else '/' + prefix

    def route(self, rule: str, **options: Any) -> Callable:
        """
        Decorator factory to initialize a new route for self (see flask.Flask.route)
        :param rule: path for this rule
        :param refresh: If True, refresh JWT will be checked for current path instead of access JWT
        :param input_schema: Marshmallow schema to input data
        :param output_schema: Marshmallow schema to output data
        :param options: flask.Flask.route options
        :return: decorator
        """
        def decorator(f: Callable) -> Callable:
            """
            Decorator to initialize a new route for self (see flask.Flask.route)
            :param f: function to wrap
            :return: Provided function
            """
            if 'refresh' in options:
                refresh = options.pop('refresh')
            else:
                refresh = False
            from .jwt_verify import jwt_required, jwt_required_role
            from .errors import _catch_request_error

            func_wrapped = f

            func_wrapped = self._wrap_db_commit(f)

            output_schema = options.pop('output_schema', None)
            if output_schema is not None:
                func_wrapped = self._wrap_marshmallow_output(func_wrapped, output_schema)

            input_schema = options.pop('input_schema', None)
            if input_schema is not None:
                func_wrapped = self._wrap_marshmallow_input(func_wrapped, input_schema)

            if self._access_level == OrgMephiAccessLevel.visitor:
                pass
            elif self._access_level == OrgMephiAccessLevel.participant:
                func_wrapped = jwt_required(refresh=refresh)(func_wrapped)
            else:
                roles = [v.value[1] for v in OrgMephiAccessLevel if v.value[0] >= self._access_level.value[0]]
                func_wrapped = jwt_required_role(roles=roles, refresh=refresh)(func_wrapped)

            func_wrapped = _catch_request_error(func_wrapped)

            if self._openapi is not None:
                func_wrapped = self._openapi(func_wrapped)

            self._blueprint.route(rule, **options)(func_wrapped)
            return f
        return decorator

    def add_module(self, module):
        """
        Add a child module

        Path to the child module will have a prefix of <this module prefix>/<child module name>

        :param module: child module
        """
        self._modules.append(module)
        module._parent = self

    def prepare(self, api_path: str, development: bool, top, marshmellow_api: bool):
        """
        Prepare this module for execution

        Load views, initialize openapi and swagger ui and recursively prepare child modules

        Should normally be only called by OrgMephiApp.prepare

        :param api_path: directory with ap files
        :param development: If True development-only options will be enabled (e.g. swagger ui wil be generated)
        :param top: Top-level module
        :param marshmellow_api: If True then openapi will be generated from apispec
        """
        from . import _orgmephi_current_module
        api_doc_path = None
        if (not marshmellow_api) and (self._api_file is not None and api_path is not None):
            api_doc_path = f'{api_path}/{self._api_file}'

        if self._parent is None or self == top:
            self._blueprint = Blueprint(self._name, __name__)
        else:
            self._blueprint = Blueprint(self._name, __name__, url_prefix='/%s' % self._name)

        last_module = _orgmephi_current_module.get()
        _orgmephi_current_module.set(self)

        try:
            if api_doc_path is not None:
                self._init_openapi(api_doc_path)
            try:
                importlib.import_module('.views', self._package)
            except ModuleNotFoundError:
                pass
            for module in self._modules:
                module.prepare(api_path, development, top, marshmellow_api)
                self._blueprint.register_blueprint(module.blueprint)
            if development and (api_doc_path is not None or marshmellow_api):
                self._init_swagger(top)
                if marshmellow_api:
                    self._api_from_marshmallow(top)
                else:
                    self._api_from_file(api_doc_path)
        except Exception:
            _orgmephi_current_module.set(last_module)
            raise
        _orgmephi_current_module.set(last_module)

    def get_swagger_blueprints(self) -> list[Blueprint]:
        """
        Get a list of swagger blueprints for self and all child modules

        Should normally only be used to register swagger ui blueprints in OrgMephiApp.prepare because swagger ui does
        not support blueprint nesting

        :return: list of swagger ui blueprints
        """
        import itertools
        if self._swagger is None:
            return list(itertools.chain(*[mod.get_swagger_blueprints() for mod in self._modules]))
        else:
            return list(itertools.chain([self._swagger], *[mod.get_swagger_blueprints() for mod in self._modules]))

    def _init_openapi(self, api_path: str):
        import yaml
        from openapi_core import create_spec
        with open(api_path, 'r') as spec_file:
            spec_dict = yaml.safe_load(spec_file)
        spec = create_spec(spec_dict)
        self._openapi = FlaskOpenAPIViewDecorator.from_spec(spec)

    def _init_swagger(self, top):
        from flask_swagger_ui import get_swaggerui_blueprint
        full_name = self.get_full_name(top)
        full_path = self.get_prefix(top)
        swagger_ui_blueprint = get_swaggerui_blueprint(
            '%s/swagger_ui' % full_path,
            '%s/swagger_ui/api.yaml' % full_path,
            blueprint_name='%s_swagger_ui' % full_name,
            config={
                'app_name': "orgmephi_%s" % full_name
            }
        )
        self._swagger = swagger_ui_blueprint

    def _api_from_file(self, api_doc_path: str):
        @self._swagger.route('/api.yaml', methods=['GET'])
        def serve_api():
            nonlocal api_doc_path
            return send_file(api_doc_path)

    _jwt_access_token_schema = {'type': 'apiKey', 'in': 'cookie', 'name': 'access_token_cookie'}
    _jwt_refresh_token_schema = {'type': 'apiKey', 'in': 'cookie', 'name': 'refresh_token_cookie'}
    _csrf_access_token_schema = {'type': 'apiKey', 'in': 'header', 'name': 'X-CSRF-TOKEN'}
    _csrf_refresh_token_schema = {'type': 'apiKey', 'in': 'header', 'name': 'X-CSRF-TOKEN'}

    def _api_from_marshmallow(self, top):
        from flask import Flask
        from apispec import APISpec
        from apispec_webframeworks.flask import FlaskPlugin
        from apispec_oneofschema import MarshmallowPlugin

        plugin = MarshmallowPlugin()

        spec = APISpec(
            title=self.get_full_name(top),
            version='1.0.0',
            openapi_version='3.0.2',
            plugins=[FlaskPlugin(), plugin]
        )

        plugin.converter.add_attribute_function(_enum2properties)

        spec.components.security_scheme('JWTAccessToken', self._jwt_access_token_schema)
        spec.components.security_scheme('JWTRefreshToken', self._jwt_refresh_token_schema)
        spec.components.security_scheme('CSRFAccessToken', self._csrf_access_token_schema)
        spec.components.security_scheme('CSRFRefreshToken', self._csrf_refresh_token_schema)

        tmp_app = Flask('tmp_app')
        tmp_app.register_blueprint(self._blueprint)

        static_endpoint = tmp_app.view_functions.get('static', None)

        with tmp_app.test_request_context():
            for endpoint in tmp_app.view_functions.values():
                if endpoint.__doc__ is not None and endpoint != static_endpoint:
                    spec.path(view=endpoint)

        api = spec.to_yaml()

        @self._swagger.route('/api.yaml', methods=['GET'])
        def serve_api():
            nonlocal api
            return api, 200, {'Content-Type': 'text/plain'}

    def _get_parents(self, top=None):
        if self._parent is None or self == top:
            return [self._name]
        return self._parent._get_parents() + [self._name]

    @staticmethod
    def _wrap_marshmallow_input(f: Callable, schema: Type[Schema]):

        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import request, make_response
            from marshmallow import ValidationError, EXCLUDE
            from marshmallow_sqlalchemy import SQLAlchemySchema
            try:
                if issubclass(schema, SQLAlchemySchema):
                    sch = schema()
                    sch.__class__ = Schema
                    request.marshmallow = sch.load(data=request.json, unknown=EXCLUDE)
                else:
                    request.marshmallow = schema().load(data=request.json, unknown=EXCLUDE)
            except ValidationError as err:
                return make_response({
                    "class": err.__class__.__name__,
                    "status": 400,
                    "title": str(err)
                }, 400)
            return f(*args, **kwargs)

        return wrapper

    @staticmethod
    def _wrap_marshmallow_output(f: Callable, schema: Type[Schema]):

        @wraps(f)
        def wrapper(*args, **kwargs):
            from flask import make_response
            result = f(*args, **kwargs)
            if len(result) == 0:
                return make_response()
            serialized = schema().dump(obj=result[0])
            return make_response(serialized, *result[1:])

        return wrapper

    @staticmethod
    def _wrap_db_commit(f: Callable):
        from . import get_current_db

        @wraps(f)
        def wrapper(*args, **kwargs):
            db = get_current_db()
            try:
                result = f(*args, **kwargs)
            except Exception:
                db.session.rollback()
                raise
            db.session.rollback()
            return result

        return wrapper
