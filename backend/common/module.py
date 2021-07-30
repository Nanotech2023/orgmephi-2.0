import importlib

from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from flask import Blueprint, send_file
from typing import Callable, Any, Union

from .access_levels import OrgMephiAccessLevel


class OrgMephiModule:
    def __init__(self, service_name: str, name: str, path: str, access_level: OrgMephiAccessLevel,
                 api_path: Union[str, None] = None, development=False):
        self._name = name
        self._blueprint = Blueprint(name, __name__, url_prefix='/%s' % name)
        self._init_api(api_path, service_name, development)
        self._path = path
        self._access_level = access_level

    def _init_api(self, api_path: Union[str, None], service_name: str, development: bool):
        if not development or api_path is None:
            self._openapi = None
            self._swagger = None
        else:
            api_doc_path = '%s/%s_%s.yaml' % (api_path, service_name, self._name)
            self._init_openapi(api_doc_path)
            if development:
                self._init_swagger(api_doc_path, service_name)
            else:
                self._swagger = None

    def _init_openapi(self, api_path: str):
        import yaml
        from openapi_core import create_spec
        with open(api_path, 'r') as spec_file:
            spec_dict = yaml.safe_load(spec_file)
        spec = create_spec(spec_dict)
        self._openapi = FlaskOpenAPIViewDecorator.from_spec(spec)

    def _init_swagger(self, api_path: str, service_name: str):
        from flask_swagger_ui import get_swaggerui_blueprint

        swagger_ui_blueprint = get_swaggerui_blueprint(
            '/%s/swagger_ui' % self._name,
            '/%s/swagger_ui/api.yaml' % self._name,
            blueprint_name='%s_swagger_ui' % self._name,
            config={
                'app_name': "orgmephi_%s_%s" % (service_name, self._name)
            }
        )

        @swagger_ui_blueprint.route('/api.yaml', methods=['GET'])
        def serve_api():
            nonlocal api_path
            return send_file(api_path)

        self._swagger = swagger_ui_blueprint

    def load(self):
        importlib.import_module('.views', self._path)

    @property
    def name(self):
        return self._name

    @property
    def blueprint(self):
        return self._blueprint

    @property
    def swagger(self):
        return self._swagger

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
