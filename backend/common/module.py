import importlib

from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from flask import Blueprint, send_file
from typing import Callable, Any, Optional

from .access_levels import OrgMephiAccessLevel


class OrgMephiModule:
    def __init__(self, name: str, package: str, access_level: OrgMephiAccessLevel, api_file: Optional[str] = None):
        self._name = name
        self._package = package
        self._blueprint: Optional[Blueprint] = None
        self._access_level = access_level
        self._modules: list[OrgMephiModule] = []
        self._parent: Optional[OrgMephiModule] = None
        self._openapi = None
        self._swagger = None
        self._api_file = api_file

    def add_module(self, module):
        self._modules.append(module)
        module._parent = self

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

    def prepare(self, api_path: str, development: bool):
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

    @property
    def name(self):
        return self._name

    @property
    def blueprint(self):
        return self._blueprint

    @property
    def swagger(self):
        return self._swagger

    @property
    def full_name(self):
        return '_'.join(self._get_parents())

    @property
    def prefix(self):
        return '' if self._parent is None else '%s/%s' % (self._parent.prefix, self._name)

    def get_swagger_blueprints(self) -> list[Blueprint]:
        import itertools
        if self._swagger is None:
            return list(itertools.chain(*[mod.get_swagger_blueprints() for mod in self._modules]))
        else:
            return list(itertools.chain([self._swagger], *[mod.get_swagger_blueprints() for mod in self._modules]))

    def _get_parents(self):
        if self._parent is None:
            return [self._name]
        return self._parent._get_parents() + [self._name]

    def route(self, rule: str, **options: Any) -> Callable:
        def decorator(f: Callable) -> Callable:
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
