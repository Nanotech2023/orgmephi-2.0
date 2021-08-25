import io

from flask import abort, send_file

from common import get_current_app, get_current_module
from common.errors import AlreadyExists
from contest.tasks.control_users.schemas import UserCertificateResponseTaskControlUsersSchema
from contest.tasks.model_schemas.contest import VariantSchema
from contest.tasks.model_schemas.olympiad import ContestSchema
from contest.tasks.participant.schemas import *
from contest.tasks.unauthorized.schemas import AllOlympiadsResponseTaskUnauthorizedSchema
from contest.tasks.util import *
from user.models import SchoolInfo

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


# Enroll in Contest


@module.route('/contest/<int:id_contest>/enroll', methods=['POST'])
def enroll_in_contest(id_contest):
    """
    Enroll in contest
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
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
          description: User already enrolled
    """

    user_id = jwt_get_id()

    current_user: User = db_get_or_raise(User, "id", user_id)

    if current_user.student_info is not None:
        grade = TargetClassEnum("student")
    else:
        school_info: SchoolInfo = current_user.school_info
        if school_info is None:
            raise InsufficientData('school_info', "school_info")
        grade = TargetClassEnum(str(school_info.grade))

    current_contest = get_contest_if_possible(id_contest)
    current_base_contest = get_base_contest(current_contest)
    target_classes = current_base_contest.target_classes

    if is_user_in_contest(user_id, current_contest):
        raise AlreadyExists('user_id', str(user_id))

    if grade not in target_classes:
        raise InsufficientData('base_contest_id', "current grade of user")

    current_contest.users.append(UserInContest(user_id=user_id,
                                               show_results_to_user=False,
                                               variant_id=generate_variant(id_contest, user_id),
                                               user_status=UserStatusEnum.Participant))

    db.session.commit()
    return {}, 200


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

    current_user = db_get_or_raise(UserInContest, "user_id", str(jwt_get_id()))

    if current_user.completed_the_contest:
        return {
                   "tasks_list": []
               }, 200

    tasks_list = get_user_tasks_if_possible(id_contest)
    return {
               "tasks_list": tasks_list
           }, 200


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

    current_user = db_get_or_raise(UserInContest, "user_id", str(jwt_get_id()))

    if current_user.completed_the_contest:
        return {}, 200

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
    current_olympiad = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    if current_olympiad.composite_type != ContestTypeEnum.CompositeContest or stage not in current_olympiad.stages:
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
    current_contest = get_user_contest_if_possible(id_olympiad, id_stage, id_contest)
    return current_contest, 200
