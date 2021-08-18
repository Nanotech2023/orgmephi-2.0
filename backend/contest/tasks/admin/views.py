from flask import request

from common import get_current_app, get_current_module
from common.errors import AlreadyExists
from contest.tasks.admin.schemas import *
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Olympiad types


@module.route('/olympiad_type/create', methods=['POST'],
              input_schema=CreateOlympiadTypeRequestAdminSchema, output_schema=CreateOlympiadTypeSchema)
def olympiad_type_create():
    """
    Add olympiad type
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOlympiadTypeRequestAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CreateOlympiadTypeSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    import sqlalchemy.exc
    values = request.marshmallow
    olympiad_type = values['olympiad_type']

    try:
        new_olympiad_type = add_olympiad_type(db.session,
                                              olympiad_type=olympiad_type)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise AlreadyExists('olympiad_type', olympiad_type)
    return {
               "olympiad_type_id": new_olympiad_type.olympiad_type_id
           }, 200


@module.route('/olympiad_type/<int:id_olympiad_type>/remove', methods=['POST'])
def olympiad_type_remove(id_olympiad_type):
    """
    Remove olympiad type
    ---
    post:
      parameters:
        - in: path
          description: Id of the olympiad type
          name: id_olympiad_type
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
    db.session.delete(olympiad)
    db.session.commit()

    return {}, 200
