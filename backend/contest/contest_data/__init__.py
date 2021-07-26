import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
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
    db.init_app(current_app)
    db.create_all()


def init_api():
    import yaml
    from openapi_core import create_spec
    api_path = current_app.config['ORGMEPHI_API_PATH']
    with open(api_path, 'r') as spec_file:
        spec_dict = yaml.safe_load(spec_file)
    global openapi
    spec = create_spec(spec_dict)
    openapi = FlaskOpenAPIViewDecorator.from_spec(spec)


app = create_app()
db = SQLAlchemy()
openapi = None
app.app_context().push()
init_security(app)
init_db()
init_api()


@app.route('/login', methods=['POST'])
def kek():
    return 'keks', 502


from contest_data.views_tasks import *

if __name__ == "__main__":
    app.run()
