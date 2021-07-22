import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

app = Flask(__name__)

# Testing database
# TODO: Put actual database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from contest_data.models_tasks import *
from contest_data.models_responses import *

if __name__ == "__main__":
    app.run(debug=True)
