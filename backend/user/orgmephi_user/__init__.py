import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from openapi_core.contrib.flask.decorators import FlaskOpenAPIViewDecorator
from orgmephi_user.default_config import DefaultConfiguration
from orgmephi_user.security import init_security


def create_app(test_config=None):
    new_app = Flask(__name__)
    new_app.config.from_object('orgmephi_user.DefaultConfiguration')
    if test_config is not None:
        new_app.config.from_object(test_config)
    elif 'ORGMEPHI_AUTH_CONFIG' in os.environ:
        new_app.config.from_envvar('ORGMEPHI_AUTH_CONFIG')
    return new_app


def init_db():
    from orgmephi_user.models import populate_university, populate_country
    db.init_app(current_app)
    db.create_all()
    populate_university()
    populate_country()


def init_api():
    import yaml
    from openapi_core import create_spec
    api_path = current_app.config['ORGMEPHI_API_PATH']
    with open(api_path, 'r') as spec_file:
        spec_dict = yaml.safe_load(spec_file)
    global openapi
    spec = create_spec(spec_dict)
    openapi = FlaskOpenAPIViewDecorator.from_spec(spec)
    if app.config['DEBUG']:
        from flask_swagger_ui import get_swaggerui_blueprint
        swagger_ui_blueprint = get_swaggerui_blueprint(
            '/swagger_ui',
            '/api.yaml',
            config={
                'app_name': "orgmephi_user"
            }
        )
        app.register_blueprint(swagger_ui_blueprint)


def init_jwt():
    current_app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
    current_app.config['JWT_COOKIE_SAMESITE'] = "Strict"
    current_app.config['JWT_CSRF_IN_COOKIES'] = False
    key_path = current_app.config['ORGMEPHI_PRIVATE_KEY']
    pubkey_path = current_app.config['ORGMEPHI_PUBLIC_KEY']
    with open(key_path, 'r') as key_file:
        key = key_file.read()
    with open(pubkey_path, 'r') as key_file:
        pubkey = key_file.read()
    current_app.config['JWT_PRIVATE_KEY'] = key
    current_app.config['JWT_PUBLIC_KEY'] = pubkey
    return JWTManager(current_app)


app = create_app()
db = SQLAlchemy()
openapi = None
app.app_context().push()
init_security(app)
init_db()
init_api()
jwt = init_jwt()


from orgmephi_user.views import *

if __name__ == "__main__":
    app.run()
