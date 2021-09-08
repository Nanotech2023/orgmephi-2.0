import io

from flask import abort, send_file

from common import get_current_app, get_current_module
from contest.tasks.control_users.schemas import UserCertificateResponseTaskControlUsersSchema
from contest.tasks.model_schemas.schemas import VariantSchema, ContestSchema
from contest.tasks.participant.schemas import *
from contest.tasks.unauthorized.schemas import AllOlympiadsResponseTaskUnauthorizedSchema
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Variant

@module.route(
    '/contest/<int:id_contest>/variant/self',
    methods=['GET'], output_schema=VariantSchema)
def variant_self(id_contest):
    """
    Get variant for user in current contest
    ---
    get:
      parameters:
        - in: path
          description: Id of the contest
          name: id_contest
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
              schema: VariantSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """

    variant = get_user_variant_if_possible(id_contest)
    return variant, 200


# Task


@module.route(
    '/contest/<int:id_contest>/tasks/self',
    methods=['GET'], output_schema=AllTaskResponseTaskParticipantSchema)
def task_all(id_contest):
    """
    Get tasks for user in current variant
    ---
    get:
      parameters:
        - in: path
          description: Id of the contest
          name: id_contest
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
              schema: AllTaskResponseTaskParticipantSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """
    # TODO SIMPLIFY
    tasks = get_user_tasks_if_possible(id_contest)
    return {
               "tasks_list": tasks
           }, 200


@module.route(
    '/contest/<int:id_contest>/tasks/<int:id_task>/self',
    methods=['GET'], output_schema=TaskSchema)
def task_get(id_contest, id_task):
    """
    Get task for user in current variant
    ---
    get:
      parameters:
        - in: path
          description: Id of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: id_task
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
              schema: TaskSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """

    task = get_user_task_if_possible(id_contest, id_task)
    return task, 200


@module.route(
    '/contest/<int:id_contest>/tasks/<int:id_task>/image/self',
    methods=['GET'])
def task_image(id_contest, id_task):
    """
    Get task image
    ---
    get:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the task
          name: id_task
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
            image/jpeg:
              schema:
                type: string
                format: binary
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    task = get_user_task_if_possible(id_contest, id_task)

    if task.image_of_task is None:
        raise InsufficientData("task", "image_of_task")

    return send_file(io.BytesIO(task.image_of_task),
                     attachment_filename='task_image.png',
                     mimetype='image/jpeg'), 200


# Certificate


@module.route(
    '/contest/<int:id_contest>/certificate/self',
    methods=['GET'], output_schema=UserCertificateResponseTaskControlUsersSchema)
def users_certificate(id_contest):
    """
    Get user certificate
    ---
    get:
      parameters:
        - in: path
          description: Id of the contest
          name: id_contest
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
          description: User not found
    """
    # contest = get_user_contest_if_possible(id_contest)
    # certificate = None
    abort(502)


# Contest


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
    methods=['GET'], output_schema=AllOlympiadsResponseTaskUnauthorizedSchema)
def contest_all_self(id_olympiad, id_stage):
    """
    Get all contests in stage
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
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllOlympiadsResponseTaskUnauthorizedSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """
    olympiad = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    if olympiad.composite_type != ContestTypeEnum.CompositeContest or stage not in olympiad.stages:
        raise InsufficientData('stage_id', 'not in current olympiad')
    all_contest = [contest_
                   for contest_ in stage.contests
                   if is_user_in_contest(jwt_get_id(), contest_)]
    return {
               "contest_list": all_contest
           }, 200


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['GET'], output_schema=ContestSchema)
def contest_self(id_olympiad, id_stage, id_contest):
    """
    Get current contest in stage
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
        - in: path
          description: Id of the contest
          name: id_contest
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
              schema: ContestSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """
    contest = get_user_contest_if_possible(id_olympiad, id_stage, id_contest)
    return contest, 200
