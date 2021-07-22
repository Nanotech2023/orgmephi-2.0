from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Testing database
# TODO: Put actual database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import contest_data.models_tasks

if __name__ == "__main__":

    from views_tasks import *
    from views_responses import *

    app.run(debug=True)
