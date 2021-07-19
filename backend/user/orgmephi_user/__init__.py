import os

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from orgmephi_user.default_config import DefaultConfiguration


def create_app(test_config=None):
    new_app = Flask(__name__)
    new_app.config.from_object('orgmephi_user.DefaultConfiguration')
    if test_config is not None:
        new_app.config.from_object(test_config)
    elif 'ORGMEPHI_AUTH_CONFIG' in os.environ:
        new_app.config.from_envvar('ORGMEPHI_AUTH_CONFIG')
    return new_app


def init_db():
    from orgmephi_user.models import populate_role, populate_university, populate_country
    db.init_app(current_app)
    db.create_all()
    populate_role()
    populate_university()
    populate_country()


app = create_app()
db = SQLAlchemy()
app.app_context().push()
init_db()

if __name__ == "__main__":
    app.run()
