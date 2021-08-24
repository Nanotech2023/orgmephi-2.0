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
              input_schema=CreateOlympiadTypeRequestTaskAdminSchema, output_schema=OlympiadTypeResponseTaskAdminSchema)
def olympiad_type_create():
    """
    Add olympiad type
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOlympiadTypeRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: OlympiadTypeResponseTaskAdminSchema
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
    current_olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
    db.session.delete(current_olympiad)
    db.session.commit()

    return {}, 200


# Location


@module.route('/location/create_online', methods=['POST'],
              input_schema=CreateOnlineLocationRequestTaskAdminSchema, output_schema=LocationResponseTaskAdminSchema)
def online_location_create():
    """
    Add new online location
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOnlineLocationRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: LocationResponseTaskAdminSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    url = values['url']

    new_location = add_online_location(db.session,
                                       url=url)
    db.session.commit()

    return {
               "location_id": new_location.location_id
           }, 200


@module.route('/location/create/russia', methods=['POST'],
              input_schema=CreateRussiaLocationRequestTaskAdminSchema, output_schema=LocationResponseTaskAdminSchema)
def location_create_russia():
    """
    Add new location
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateRussiaLocationRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: LocationResponseTaskAdminSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    city_name = values['city_name']
    region_name = values['region_name']
    address = values['address']

    new_location = add_russia_location(db.session,
                                       city_name=city_name,
                                       region_name=region_name,
                                       address=address)
    db.session.commit()

    return {
               "location_id": new_location.location_id
           }, 200


@module.route('/location/create_other', methods=['POST'],
              input_schema=CreateOtherLocationRequestTaskAdminSchema, output_schema=LocationResponseTaskAdminSchema)
def location_create_other():
    """
    Add new location
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateOtherLocationRequestTaskAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: LocationResponseTaskAdminSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    country_name = values['country_name']
    location_ = values['location']

    new_location = add_other_location(db.session,
                                      country_name=country_name,
                                      location=location_)
    db.session.commit()

    return {
               "location_id": new_location.location_id
           }, 200


@module.route('/location/<int:id_location>/remove', methods=['POST'])
def location_remove(id_location):
    """
    Remove location
    ---
    post:
      parameters:
        - in: path
          description: Id of the location
          name: id_location
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
    location = db_get_or_raise(OlympiadLocation, "location_id", str(id_location))
    db.session.delete(location)
    db.session.commit()

    return {}, 200
