from flask import make_response

from common import get_current_app, get_current_module
from common.util import db_get_all
from contest.tasks.model_schemas.schemas import OlympiadTypeSchema, BaseContestSchema, ContestSchema, StageSchema
from contest.tasks.unauthorized.schemas import AllOlympiadTypesSchema, AllBaseContestSchema, AllOlympiadsSchema, \
    AllStagesSchema
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Olympiad types


@module.route('/olympiad_type/all', methods=['GET'],
              output_schema=AllOlympiadTypesSchema)
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
              schema: AllOlympiadTypesSchema
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
    olympiad = db_get_or_raise(OlympiadType, "olympiad_type_id", str(id_olympiad_type))
    return olympiad, 200


# Olympiad
# TODO Target class checking ???


@module.route('/base_olympiad/all', methods=['GET'],
              output_schema=AllBaseContestSchema)
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
              schema: AllBaseContestSchema
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


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/all', methods=['GET'],
              output_schema=AllOlympiadsSchema)
def olympiads_all(id_base_olympiad):
    """
    Get olympiads list
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
              schema: AllOlympiadsSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    all_olympiads = [olympiad for olympiad in base_contest.child_contests]
    return {
               "contest_list": all_olympiads
           }, 200


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
    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    return contest, 200


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
    olympiad = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    if olympiad.composite_type != ContestTypeEnum.CompositeContest or stage not in olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    return stage, 200


@module.route('/olympiad/<int:id_olympiad>/stage/all', methods=['GET'],
              output_schema=AllStagesSchema)
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
              schema: AllStagesSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: Olympiad type not found
    """
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    contest = db_get_or_raise(CompositeContest, "contest_id", str(id_olympiad))
    all_stages = [stage for stage in contest.stages]
    return {
               "stages_list": all_stages
           }, 200



