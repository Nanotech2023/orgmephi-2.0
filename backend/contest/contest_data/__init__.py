import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    new_app = Flask(__name__)
    new_app.config.from_object('contest_data.DefaultConfiguration')
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
    api_path = current_app.config['STUDENTRESPONSES_API_PATH']
    with open(api_path, 'r') as spec_file:
        spec_dict = yaml.safe_load(spec_file)
    global openapi
    spec = create_spec(spec_dict)
    openapi = FlaskOpenAPIViewDecorator.from_spec(spec)


app = create_app()
db = SQLAlchemy()
openapi = None
app.app_context().push()
init_db()
init_api()

import contest_data.models_tasks
import contest_data.models_responses
from views_tasks import *

if __name__ == "__main__":
    app.run()
