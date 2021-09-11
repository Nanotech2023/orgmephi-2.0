import io

from flask import send_file, request

from common import get_current_module
from common.errors import AlreadyExists, TimeOver
from common.util import send_pdf
from contest.responses.models import ResponseStatusEnum
from contest.responses.util import get_user_in_contest_work
from contest.tasks.model_schemas.contest import VariantSchema
from contest.tasks.model_schemas.olympiad import ContestSchema
from contest.tasks.participant.schemas import *
from contest.tasks.unauthorized.schemas import AllOlympiadsResponseTaskUnauthorizedSchema, \
    FilterSimpleContestResponseSchema
from contest.tasks.unauthorized.util import filter_olympiad_query
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


# Variant

@module.route(
    '/contest/<int:id_contest>/variant/self',
    methods=['GET'], output_schema=VariantSchema)
def get_variant_self(id_contest):
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

    current_user = db_get_or_raise(UserInContest, "user_id", str(jwt_get_id()))
    current_response = get_user_in_contest_work(str(jwt_get_id()), id_contest)

    # Contest not started
    if current_response.status != ResponseStatusEnum.in_progress:
        raise ContestContentAccessDenied()

    # Contest ended
    if current_user.completed_the_contest:
        raise TimeOver("olympiad")

    variant = get_user_variant_if_possible(id_contest)
    return variant, 200


# Enroll in Contest


@module.route('/contest/<int:id_contest>/enroll', methods=['POST'],
              input_schema=EnrollRequestTaskParticipantSchema)
def enroll_in_contest(id_contest):
    """
    Enroll in contest
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: EnrollRequestTaskParticipantSchema
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

    values = request.marshmallow

    user_id = jwt_get_id()
    current_contest: SimpleContest = get_contest_if_possible(id_contest)

    # Id user doesn't win previous contest
    if not check_previous_contest_condition_if_possible(id_contest, user_id):
        raise ContestContentAccessDenied()

    # Can't enroll after deadline
    if datetime.utcnow() > current_contest.end_of_enroll_date:
        raise TimeOver("Time for enrolling is over")

    location_id = values.get('location_id', None)

    # Can't add without location
    if location_id is not None:
        db_get_or_raise(OlympiadLocation, "location_id", location_id)

    # User is already enrolled
    if is_user_in_contest(user_id, current_contest):
        raise AlreadyExists('user_id', str(user_id))

    current_base_contest = get_base_contest(current_contest)

    target_classes = current_base_contest.target_classes
    current_user = db_get_or_raise(User, "id", user_id)
    grade = check_user_unfilled_for_enroll(current_user)

    # Wrong user class
    if grade not in target_classes:
        raise InsufficientData('base_contest_id', "current grade of user")

    current_contest.users.append(UserInContest(user_id=user_id,
                                               show_results_to_user=False,
                                               variant_id=generate_variant(id_contest, user_id),
                                               location_id=location_id,
                                               user_status=UserStatusEnum.Participant))

    db.session.commit()
    return {}, 200


@module.route('/contest/<int:id_contest>/change_location', methods=['POST'],
              input_schema=EnrollRequestTaskParticipantSchema)
def change_user_location_in_contest(id_contest):
    """
    EChange user location
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: EnrollRequestTaskParticipantSchema
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

    values = request.marshmallow

    location_id = values.get('location_id', None)
    user_id = jwt_get_id()

    current_contest: SimpleContest = get_contest_if_possible(id_contest)

    # Can't enroll after deadline
    if datetime.utcnow().date() > current_contest.end_of_enroll_date:
        raise TimeOver("Time for enrolling is over")

    if location_id is not None:
        db_get_or_raise(OlympiadLocation, "location_id", location_id)

    current_user = current_contest.users.filter_by(
        **{
            "user_id": str(user_id)
        }
    ).one_or_none()

    current_user.location_id = location_id

    db.session.commit()
    return {}, 200


# Task


@module.route(
    '/contest/<int:id_contest>/tasks/self',
    methods=['GET'], output_schema=AllTaskResponseTaskParticipantSchema)
def get_all_tasks_self(id_contest):
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
    current_response = get_user_in_contest_work(str(jwt_get_id()), id_contest)

    # Contest not started
    if current_response.status != ResponseStatusEnum.in_progress:
        raise ContestContentAccessDenied()

    # Contest ended
    if current_user.completed_the_contest:
        raise TimeOver("olympiad")

    tasks_list = get_user_tasks_if_possible(id_contest)
    return {
               "tasks_list": tasks_list
           }, 200


@module.route(
    '/contest/<int:id_contest>/tasks/<int:id_task>/image/self',
    methods=['GET'])
def get_task_image_self(id_contest, id_task):
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
    current_response = get_user_in_contest_work(str(jwt_get_id()), id_contest)

    # Contest not started
    if current_response.status != ResponseStatusEnum.in_progress:
        raise ContestContentAccessDenied()

    # Contest ended
    if current_user.completed_the_contest:
        raise TimeOver("olympiad")

    task = get_user_task_if_possible(id_contest, id_task)

    if task.image_of_task is None:
        raise DataConflict("Task does not have image")

    return send_file(io.BytesIO(task.image_of_task),
                     attachment_filename='task_image.png',
                     mimetype='image/jpeg'), 200


# Certificate


@module.route(
    '/contest/<int:id_contest>/certificate/self',
    methods=['GET'])
def get_user_certificate_self(id_contest):
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
          content:
            application/pdf:
              schema:
                type: string
                format: binary
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
        '404':
          description: User not found
    """

    current_contest: SimpleContest = get_contest_if_possible(id_contest)

    # Try to see the results before contest
    if datetime.utcnow().date() < current_contest.result_publication_date:
        raise ContestIsStillOnReview()

    current_contest = get_contest_if_possible(id_contest)
    current_user = db_get_or_raise(User, 'id', jwt_get_id())
    unfilled = current_user.unfilled()
    if len(unfilled) > 0:
        raise InsufficientData('user', str(unfilled))

    mark = get_user_in_contest_work(jwt_get_id(), id_contest).mark
    user_status = db_get_or_raise(UserInContest, 'user_id', jwt_get_id()).user_status

    return send_pdf('user_certificate.html', u=user, mark=mark, user_status=user_status,
                    back=current_contest)


# Contest


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
    methods=['GET'], output_schema=AllOlympiadsResponseTaskUnauthorizedSchema)
def get_all_contests_in_stage_self(id_olympiad, id_stage):
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

    if is_stage_in_contest(current_olympiad, stage):
        contest_list = [contest_
                        for contest_ in stage.contests
                        if is_user_in_contest(jwt_get_id(), contest_)]
        return {
                   "contest_list": contest_list
               }, 200


@module.route(
    '/olympiad/all',
    methods=['GET'], output_schema=FilterSimpleContestResponseSchema)
def get_all_contests_self():
    """
    Get all contests for user
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
    return filter_olympiad_query(request.args)


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['GET'], output_schema=ContestSchema)
def get_contest_in_stage_self(id_olympiad, id_stage, id_contest):
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


@module.route(
    '/olympiad/<int:id_olympiad>',
    methods=['GET'], output_schema=ContestSchema)
def get_contest_self(id_olympiad):
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
    current_contest = get_user_simple_contest_if_possible(id_olympiad)
    return current_contest, 200
