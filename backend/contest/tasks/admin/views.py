from flask import request

from common import get_current_module
from common.util import db_add_if_not_exists
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
    values = request.marshmallow
    olympiad_type = values['olympiad_type']

    new_olympiad_type = add_olympiad_type(olympiad_type=olympiad_type)

    db_add_if_not_exists(db.session, OlympiadType, new_olympiad_type, ['olympiad_type'])
    db.session.commit()

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


@module.route('/location/create_russia', methods=['POST'],
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
    current_location = db_get_or_raise(OlympiadLocation, "location_id", str(id_location))
    db.session.delete(current_location)
    db.session.commit()

    return {}, 200

# Group Restriction


@module.route('/contest/<int:contest_id>/restrictions', methods=['POST'],
              input_schema=CreateContestGroupRestrictionAdminSchema)
def contest_restriction_create(contest_id):
    """
    Add new restriction
    ---
    post:
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateContestGroupRestrictionAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '404':
          description: Contest or group not found
    """
    values = request.marshmallow
    groups = values['group_ids']
    restriction = values['restriction']
    current_contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    for group_id in groups:
        db_get_or_raise(Group, 'id', group_id)
        if current_contest.group_restrictions.filter_by(group_id=group_id).first() is not None:
            raise AlreadyExists(field='contest_id , group_id', value=f'{contest_id} , {group_id}')
        current_contest.group_restrictions.append(ContestGroupRestriction(contest_id=contest_id,
                                                                          group_id=group_id,
                                                                          restriction=restriction))
    db.session.commit()
    return {}, 200


@module.route('/contest/<int:contest_id>/restrictions', methods=['PATCH'],
              input_schema=CreateContestGroupRestrictionAdminSchema)
def contest_restriction_change(contest_id):
    """
    Change current contest restrictions
    ---
    patch:
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateContestGroupRestrictionAdminSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '404':
          description: Contest or group not found
    """
    values = request.marshmallow
    groups = values['group_ids']
    restriction = values['restriction']
    current_contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    for group_id in groups:
        restriction_elem: ContestGroupRestriction = current_contest.group_restrictions.\
            filter_by(group_id=group_id).first()
        if restriction_elem is None:
            raise NotFound(field='contest_id , group_id', value=f'{contest_id} , {group_id}')
        restriction_elem.restriction = restriction
    db.session.commit()
    return {}, 200


@module.route('/contest/<int:contest_id>/restrictions', methods=['GET'],
              output_schema=GetContestGroupRestrictionListAdminSchema)
def contest_restriction_get(contest_id):
    """
    Get current contest restrictions
    ---
    get:
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetContestGroupRestrictionListAdminSchema
        '400':
          description: Bad request
        '404':
          description: Contest or group not found
    """
    current_contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    restrictions = current_contest.group_restrictions.all()
    return {"restrictions": restrictions}, 200
