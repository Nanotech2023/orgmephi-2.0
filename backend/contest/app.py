from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Testing database
# TODO: Put actual database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

if __name__ == "__main__":

    from views_tasks import *
    from views_responses import *

    app.run(debug=True)
