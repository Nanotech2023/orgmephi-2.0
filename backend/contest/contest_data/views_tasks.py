import datetime

from flask import request, make_response
import re

from contest_data.models_task import *
from contest_data.errors import *
from contest_data import app, db, openapi


@app.route('/olympiad/create', methods=['POST'])
@openapi
def olympiad_create():
    try:
        values = request.openapi.body
        name = values['name']
        desc = values['description']
        rules = values['rules']

        # TODO Checking

        olympiad = Olympiad(
            name=name,
            description=desc,
            rules=rules,
        )
        db.session.add(olympiad)

        # Generate olympiad.id
        # db.session.flush()

        db.session.commit()
        return make_response(
            {
                "olympiad_id": olympiad.id,
            }, 200)

    except RequestError as err:
        db.session.rollback()
        return err.to_response()

