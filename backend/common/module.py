import importlib

from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from flask import Blueprint, send_file
from typing import Callable, Any, Optional

from .access_levels import OrgMephiAccessLevel


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

    @property
    def full_name(self) -> str:
        """
        Full name of self, i.e. name that includes al parent names in format <parent.full_name>_<self.name>
        :return: Full name of self
        """
        return '_'.join(self._get_parents())

    @property
    def prefix(self) -> str:
        """
        URL prefix of self, equal to <this module prefix>/<child module name> except for top-level module, that has no
            prefix
        :return: URL prefix of self
        """
        return '' if self._parent is None else '%s/%s' % (self._parent.prefix, self._name)

    def route(self, rule: str, **options: Any) -> Callable:
        """
        Decorator factory to initialize a new route for self (see flask.Flask.route)
        :param rule: path for this rule
        :param refresh: If True, refresh JWT will be checked for current path instead of access JWT
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
            if self._access_level == OrgMephiAccessLevel.visitor:
                jwt_wrap = f
            elif self._access_level == OrgMephiAccessLevel.participant:
                jwt_wrap = jwt_required(refresh=refresh)(f)
            else:
                roles = [v.value[1] for v in OrgMephiAccessLevel if v.value[0] >= self._access_level.value[0]]
                jwt_wrap = jwt_required_role(roles=roles, refresh=refresh)(f)
            catch_error_wrap = _catch_request_error(jwt_wrap)
            if self._openapi is not None:
                openapi_wrap = self._openapi(catch_error_wrap)
            else:
                openapi_wrap = catch_error_wrap
            self._blueprint.route(rule, **options)(openapi_wrap)
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

    def prepare(self, api_path: str, development: bool):
        """
        Prepare this module for execution

        Load views, initialize openapi and swagger ui and recursively prepare child modules

        Should normally be only called by OrgMephiApp.prepare

        :param api_path: directory with ap files
        :param development: If True development-only options will be enabled (e.g. swagger ui wil be generated)
        """
        from . import _orgmephi_current_module

        if self._parent is None:
            self._blueprint = Blueprint(self._name, __name__)
        else:
            self._blueprint = Blueprint(self._name, __name__, url_prefix='/%s' % self._name)

        last_module = _orgmephi_current_module.get()
        _orgmephi_current_module.set(self)

        try:
            try:
                importlib.import_module('.views', self._package)
            except ModuleNotFoundError:
                pass

            self._init_api(api_path, development)

            for module in self._modules:
                module.prepare(api_path, development)
                self._blueprint.register_blueprint(module.blueprint)
        finally:
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

    def _init_api(self, api_path: Optional[str], development: bool):
        if api_path is None or self._api_file is None:
            return
        api_doc_path = '%s/%s' % (api_path, self._api_file)
        self._init_openapi(api_doc_path)
        if development:
            self._init_swagger(api_doc_path)
        else:
            self._swagger = None

    def _init_openapi(self, api_path: str):
        import yaml
        from openapi_core import create_spec
        with open(api_path, 'r') as spec_file:
            spec_dict = yaml.safe_load(spec_file)
        spec = create_spec(spec_dict)
        self._openapi = FlaskOpenAPIViewDecorator.from_spec(spec)

    def _init_swagger(self, api_doc_path: str):
        from flask_swagger_ui import get_swaggerui_blueprint
        full_name = self.full_name
        full_path = self.prefix
        swagger_ui_blueprint = get_swaggerui_blueprint(
            '%s/swagger_ui' % full_path,
            '%s/swagger_ui/api.yaml' % full_path,
            blueprint_name='%s_swagger_ui' % full_name,
            config={
                'app_name': "orgmephi_%s" % full_name
            }
        )

        @swagger_ui_blueprint.route('/api.yaml', methods=['GET'])
        def serve_api():
            nonlocal api_doc_path
            return send_file(api_doc_path)

        self._swagger = swagger_ui_blueprint

    def _get_parents(self):
        if self._parent is None:
            return [self._name]
        return self._parent._get_parents() + [self._name]
