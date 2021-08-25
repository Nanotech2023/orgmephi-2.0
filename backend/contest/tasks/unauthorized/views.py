from flask import request

from common import get_current_app, get_current_module
from common.util import db_get_all
from contest.tasks.unauthorized.schemas import *
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Olympiad types


@module.route('/olympiad_type/all', methods=['GET'],
              output_schema=AllOlympiadTypesResponseTaskUnauthorizedSchema)
def olympiad_type_all():
    """
    Get all olympiad types
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllOlympiadTypesResponseTaskUnauthorizedSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    olympiad_types = db_get_all(OlympiadType)
    return {
               "olympiad_types": olympiad_types
           }, 200


@module.route('/olympiad_type/<int:id_olympiad_type>', methods=['GET'],
              output_schema=OlympiadTypeSchema)
def olympiad_type_get(id_olympiad_type):
    """
    Get olympiad type by id
    ---
    get:
      parameters:
        - in: path
          description: Id of the olympiad type
          name: id_olympiad_type
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: OlympiadTypeSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    current_olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
    return current_olympiad, 200


# Location


@module.route('/location/all', methods=['GET'],
              output_schema=AllLocationResponseTaskUnauthorizedSchema)
def location_all():
    """
    Get all locations
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllLocationResponseTaskUnauthorizedSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    locations = db_get_all(OlympiadLocation)
    return {
               "locations": locations
           }, 200


@module.route('/location/<int:id_location>', methods=['GET'],
              output_schema=OlympiadLocationSchema)
def id_location_get(id_location):
    """
    Get location by id
    ---
    get:
      parameters:
        - in: path
          description: Id of the location
          name: id_location
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: OlympiadLocationSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    current_location = db_get_or_raise(OlympiadLocation, "location_id", str(id_location))
    return current_location, 200


# Olympiad
# TODO Target class checking ???


@module.route('/base_olympiad/all', methods=['GET'],
              output_schema=AllBaseContestResponseTaskUnauthorizedSchema)
def base_olympiads_all():
    """
    Get base olympiads list
    ---
    get:
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllBaseContestResponseTaskUnauthorizedSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    olympiads = db_get_all(BaseContest)
    return {
               "olympiad_list": olympiads
           }, 200


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['GET'],
              output_schema=BaseContestSchema)
def base_olympiad_get(id_base_olympiad):
    """
    Get base olympiad
    ---
    get:
      parameters:
        - in: path
          description: Id of the base contest
          name: id_base_olympiad
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: BaseContestSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    return base_contest, 200


@module.route('/olympiad/all', methods=['GET'],
              output_schema=FilterSimpleContestResponseSchema)
def olympiads_all():
    """
    Get olympiads list
    ---
    get:
      parameters:
        - in: query
          name: offset
          required: false
          schema:
            type: integer
        - in: query
          name: limit
          required: false
          schema:
            type: integer
        - in: query
          name: base_contest_id
          required: false
          schema:
            type: integer
        - in: query
          name: location_id
          required: false
          schema:
            type: integer
        - in: query
          name: end_date
          required: false
          schema:
            format: date-time
            type: string
        - in: query
          name: target_classes
          required: false
          schema:
            type: string
            enum: ['5', '6', '7', '8', '9', '10', '11', 'student']
        - in: query
          name: only_count
          required: false
          schema:
            type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FilterSimpleContestResponseSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """

    return filter_olympiad_query(request.args)


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['GET'],
              output_schema=ContestSchema)
def olympiad_get(id_base_olympiad, id_olympiad):
    """
    Get olympiad
    ---
    get:
      parameters:
        - in: path
          description: Id of the base contest
          name: id_base_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    current_contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    return current_contest, 200


# Stage


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>', methods=['GET'],
              output_schema=StageSchema)
def stage_get(id_olympiad, id_stage):
    """
    Get stage
    ---
    get:
      parameters:
        - in: path
          description: Id of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the stage
          name: id_stage
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: StageSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    current_olympiad = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    if current_olympiad.composite_type != ContestTypeEnum.CompositeContest or stage not in current_olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    return stage, 200


@module.route('/olympiad/<int:id_olympiad>/stage/all', methods=['GET'],
              output_schema=AllStagesResponseTaskUnauthorizedSchema)
def stages_all(id_olympiad):
    """
    Get stage
    ---
    get:
      parameters:
        - in: path
          description: Id of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllStagesResponseTaskUnauthorizedSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    current_contest = db_get_or_raise(CompositeContest, "contest_id", str(id_olympiad))
    all_stages = [stage for stage in current_contest.stages]
    return {
               "stages_list": all_stages
           }, 200
