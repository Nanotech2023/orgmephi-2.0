import os
import importlib

from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from flask import Blueprint, send_file
from typing import Callable, Any, Union


class OrgMephiModule:
    def __init__(self, service_name: str, name: str, api_path: Union[str, None] = None, development=False):
        self._name = name
        self._db_prepare_actions: list[Callable] = []
        self._blueprint = Blueprint(name, __name__, url_prefix='/%s' % name)
        self._init_api(api_path, service_name, development)

    def _init_api(self, api_path: Union[str, None], service_name: str, development: bool):
        if not development or api_path is None:
            self._openapi = None
            self._swagger = None
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

    def load(self, service_name):
        importlib.import_module('.models', '%s.%s' % (service_name, self._name))
        importlib.import_module('.views', '%s.%s' % (service_name, self._name))

    def prepare_db(self):
        for act in self._db_prepare_actions:
            act()

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
            from .errors import _catch_request_error
            catch_error_wrap = _catch_request_error(f)
            openapi_wrap = self._openapi(catch_error_wrap)
            self._blueprint.route(rule, **options)(openapi_wrap)
            return f
        return decorator

    def db_prepare_action(self):
        def decorator(f: Callable) -> Callable:
            self._db_prepare_actions.append(f)
            return f
        return decorator


def get_module(name: str) -> OrgMephiModule:
    from . import _orgmephi_current_app
    return _orgmephi_current_app.get().get_module(name)
