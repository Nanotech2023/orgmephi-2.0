from flask import request
from marshmallow import EXCLUDE

from common import get_current_module
from contest.tasks.creator.schemas import BaseOlympiadResponseTaskCreatorSchema, StageResponseTaskCreatorSchema, \
    ContestResponseTaskCreatorSchema, TaskResponseTaskCreatorSchema
from contest.tasks.editor.schemas import *
from contest.tasks.model_schemas.certificate import CertificateTypeSchema, CertificateSchema
from contest.tasks.model_schemas.olympiad import BaseContestSchema, SimpleContestSchema, CompositeContestSchema, \
    StageSchema
from contest.tasks.model_schemas.tasks import PlainTaskSchema, RangeTaskSchema, MultipleChoiceTaskSchema, \
    TaskPoolSchema, ContestTaskSchema
from contest.tasks.models.certificate import Certificate, CertificateType
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/base_olympiad/<int:id_base_olympiad>/remove', methods=['POST'])
def base_olympiad_remove(id_base_olympiad):
    """
    Delete a base olympiad
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the base olympiad
          name: id_base_olympiad
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: Group not found
    """

    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    db.session.delete(base_contest)
    db.session.commit()
    return {}, 200


@module.route('/base_olympiad/<int:id_base_olympiad>', methods=['PATCH'],
              input_schema=UpdateBaseOlympiadRequestTaskEditorSchema,
              output_schema=BaseOlympiadResponseTaskCreatorSchema)
def base_olympiad_patch(id_base_olympiad):
    """
    Patch base olympiad
    ---
    patch:
      parameters:
        - in: path
          description: ID of the base olympiad
          name: id_base_olympiad
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateBaseOlympiadRequestTaskEditorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: BaseOlympiadResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    db_get_or_raise(OlympiadType, "olympiad_type_id", values["olympiad_type_id"])

    BaseContestSchema(load_instance=True).load(request.json, instance=base_contest, session=db.session,
                                               partial=True, unknown=EXCLUDE)

    db.session.commit()

    return base_contest, 200


# Task Pool


@module.route('/base_olympiad/<int:id_base_olympiad>/task_pool/<int:id_task_pool>/remove',
              methods=['POST'])
def task_pool_remove(id_base_olympiad, id_task_pool):
    """
    Delete a task pool
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the base olympiad
          name: id_base_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the task pool
          name: id_task_pool
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: TaskPool not found
    """

    db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    task_pool = db_get_or_raise(TaskPool, "task_pool_id", id_task_pool)
    db.session.delete(task_pool)
    db.session.commit()
    return {}, 200


@module.route('/base_olympiad/<int:id_base_olympiad>/task_pool/<int:id_task_pool>',
              methods=['PATCH'])
def task_pool_patch(id_base_olympiad, id_task_pool):
    """
    Update task pool
    ---
    patch:
      parameters:
        - in: path
          description: ID of the base olympiad
          name: id_base_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the task pool
          name: id_task_pool
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: TaskPoolSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: TaskPool not found
    """

    db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    task_pool = db_get_or_raise(TaskPool, "task_pool_id", id_task_pool)

    TaskPoolSchema(load_instance=True).load(request.json, instance=task_pool, session=db.session,
                                            partial=True, unknown=EXCLUDE)

    db.session.commit()

    return {}, 200


# Contest task


@module.route('/contest/<int:id_contest>/contest_task/<int:id_contest_task>/remove',
              methods=['POST'])
def contest_task_remove(id_contest, id_contest_task):
    """
    Delete a task pool
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the base olympiad
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the contest task
          name: id_contest_task
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: TaskPool not found
    """

    db_get_or_raise(Contest, "contest_id", id_contest)
    contest_task = db_get_or_raise(ContestTask, "contest_task_id", id_contest_task)
    db.session.delete(contest_task)
    db.session.commit()
    return {}, 200


@module.route('/contest/<int:id_contest>/contest_task/<int:id_contest_task>', methods=['PATCH'])
def contest_task_edit(id_contest, id_contest_task):
    """
    Create contest task
    ---
    patch:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the contest task
          name: id_contest_task
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: ContestTaskSchema
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
    """

    values = request.json
    pool_changed = values.get('task_pools', None) is not None

    contest_ = db_get_or_raise(Contest, "contest_id", id_contest)
    contest_task = db_get_or_raise(ContestTask, "contest_task_id", id_contest_task)
    ContestTaskSchema(load_instance=True).load(request.json, instance=contest_task, session=db.session,
                                               partial=True, unknown=EXCLUDE)

    if pool_changed:
        previous_pools = set(
            [task_pool_
             for contest_task_ in contest_.contest_tasks.all()
             for task_pool_ in contest_task_.task_pools]
        )

        if len(previous_pools) != 0:
            if previous_pools & set(contest_task.task_pools):
                raise AlreadyExists("task_pool", "task_pool_id")

    db.session.commit()

    return {}, 200


# Contest views

# Olympiads


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>/remove', methods=['POST'])
def olympiad_remove(id_base_olympiad, id_olympiad):
    """
    Delete a olympiad
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the base olympiad
          name: id_base_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: Olympiad not found
    """

    db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    current_contest = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db.session.delete(current_contest)
    db.session.commit()
    return {}, 200


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['PATCH'],
              input_schema=UpdateContestRequestTaskEditorSchema,
              output_schema=ContestResponseTaskCreatorSchema)
def olympiad_patch(id_base_olympiad, id_olympiad):
    """
    Update composite contest
    ---
    patch:
      parameters:
        - in: path
          description: ID of the base olympiad
          name: id_base_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateContestRequestTaskEditorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    current_contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))

    if current_contest.composite_type == ContestTypeEnum.SimpleContest:
        SimpleContestSchema(load_instance=True).load(request.json, instance=current_contest, session=db.session,
                                                     partial=True, unknown=EXCLUDE)
    else:
        CompositeContestSchema(load_instance=True).load(request.json, instance=current_contest, session=db.session,
                                                        partial=True, unknown=EXCLUDE)

    db.session.commit()
    return current_contest, 200


# Stage


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/remove',
              methods=['POST'])
def stage_remove(id_olympiad, id_stage):
    """
    Delete a stage
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the stage
          name: id_stage
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: Olympiad not found
    """

    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    db.session.delete(stage)
    db.session.commit()
    return {}, 200


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>',
              methods=['PATCH'],
              input_schema=UpdateStageRequestTaskEditorSchema,
              output_schema=StageResponseTaskCreatorSchema)
def stage_patch(id_olympiad, id_stage):
    """
    Update stage
    ---
    patch:
      parameters:
        - in: path
          description: ID of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the stage
          name: id_stage
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateStageRequestTaskEditorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: StageResponseTaskCreatorSchema
        '403':
          description: Invalid role of current user
        '404':
          description: Stage not found
    """

    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))

    StageSchema(load_instance=True).load(request.json, instance=stage, session=db.session,
                                         partial=True, unknown=EXCLUDE)

    db.session.commit()

    return stage, 200


# Contest views


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest'
    '>/remove',
    methods=['POST'])
def contest_remove(id_olympiad, id_stage, id_contest):
    """
    Delete a contest in stage
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the stage
          name: id_stage
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: Olympiad not found
    """

    current_contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    db.session.delete(current_contest)
    db.session.commit()
    return {}, 200


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/add_previous',
    methods=['PATCH'], input_schema=UpdatePreviousContestRequestTaskEditorSchema)
def contest_add_previous(id_olympiad, id_stage, id_contest):
    """
    Update composite contest in stage
    ---
    patch:
      parameters:
        - in: path
          description: ID of the olympiad
          name: id_olympiad
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the stage
          name: id_stage
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdatePreviousContestRequestTaskEditorSchema
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
    """
    current_contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    values = request.marshmallow
    current_contest.change_previous(**values)
    db.session.commit()

    return {}, 200


@module.route('/task_pool/<int:id_task_pool>/task/<int:id_task>/upload_image',
              methods=['POST'])
def task_image_upload(id_task_pool, id_task):
    """
    Upload task image
    ---
    post:
      requestBody:
        required: true
        content:
          application/octet-stream:
            schema:
              type: string
              format: binary
      parameters:
        - in: path
          description: ID of the task pool
          name: id_task_pool
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
        '400':
          description: Bad request
        '404':
          description: Base contest not found
        '409':
          description: Wrong value
    """
    task = get_task_in_pool_if_possible(id_task_pool, id_task)
    app.store_media('TASK', task, 'image_of_task', TaskImage)
    db.session.commit()
    return {}, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/<int:id_task>/remove',
    methods=['POST'])
def task_remove(id_task_pool, id_task):
    """
    Delete a task
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the task pool
          name: id_task_pool
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the task
          name: id_task
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Invalid role of current user
        '404':
          description: Olympiad not found
    """

    task = get_task_in_pool_if_possible(id_task_pool, id_task)
    db.session.delete(task)
    db.session.commit()

    return {}, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/<int:id_task>/plain',
    methods=['PATCH'], output_schema=TaskResponseTaskCreatorSchema)
def task_patch_plain(id_task_pool, id_task):
    """
    Update plain task
    ---
    patch:
      parameters:
        - in: path
          description: ID of the task pool
          name: id_task_pool
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the task
          name: id_task
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: PlainTaskSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    task = get_task_in_pool_if_possible(id_task_pool, id_task)

    PlainTaskSchema(load_instance=True).load(request.json, instance=task, session=db.session,
                                             partial=True, unknown=EXCLUDE)

    db.session.commit()

    return task, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/<int:id_task>/range',
    methods=['PATCH'], output_schema=TaskResponseTaskCreatorSchema)
def task_patch_range(id_task_pool, id_task):
    """
    Update range task
    ---
    patch:
      parameters:
        - in: path
          description: ID of the task pool
          name: id_task_pool
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the task
          name: id_task
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: RangeTaskSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    task = get_task_in_pool_if_possible(id_task_pool, id_task)

    RangeTaskSchema(load_instance=True).load(request.json, instance=task, session=db.session,
                                             partial=True, unknown=EXCLUDE)

    db.session.commit()

    return task, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/<int:id_task>/multiple',
    methods=['PATCH'], output_schema=TaskResponseTaskCreatorSchema)
def task_patch_multiple(id_task_pool, id_task):
    """
    Update multiple task
    ---
    patch:
      parameters:
        - in: path
          description: ID of the task pool
          name: id_task_pool
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the task
          name: id_task
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: MultipleChoiceTaskSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.json
    task = get_task_in_pool_if_possible(id_task_pool, id_task)
    MultipleChoiceTaskSchema(load_instance=True).load(values, instance=task, session=db.session,
                                                      partial=True, unknown=EXCLUDE)
    db.session.commit()

    return task, 200


# Location


@module.route('/contest/<int:id_contest>/add_location', methods=['POST'],
              input_schema=UpdateLocationOfContestRequestTaskEditorSchema)
def add_locations_to_contest(id_contest):
    """
    Add locations to contest
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateLocationOfContestRequestTaskEditorSchema
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
    """

    values = request.marshmallow
    locations = values['locations']

    current_contest = get_contest_if_possible(id_contest)

    for location_id in locations:
        current_location = db_get_or_raise(OlympiadLocation, "location_id", str(location_id))
        if current_location not in current_contest.locations:
            current_contest.locations.append(current_location)

    db.session.commit()
    return {}, 200


@module.route('/contest/<int:id_contest>/remove_location', methods=['POST'],
              input_schema=UpdateLocationOfContestRequestTaskEditorSchema)
def remove_locations_from_contest(id_contest):
    """
    Remove location from contest
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateLocationOfContestRequestTaskEditorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '409':
          description: Location already in use
    """

    values = request.marshmallow

    locations = values['locations']

    current_contest = get_contest_if_possible(id_contest)

    for location_id in locations:
        current_location = db_get_or_raise(OlympiadLocation, "location_id", str(location_id))
        if current_location in current_contest.locations:
            current_contest.locations.remove(current_location)
        else:
            raise NotFound("contest.locations", str(location_id))

    db.session.commit()
    return {}, 200


# Target classes


@module.route('/base_olympiad/<int:id_base_olympiad>/add_target_classes', methods=['POST'],
              input_schema=UpdateTargetClassesOfContestRequestTaskEditorSchema)
def add_target_classes_to_contest(id_base_olympiad):
    """
    Add target classes to contest
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
          name: id_base_olympiad
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateTargetClassesOfContestRequestTaskEditorSchema
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
    """

    values = request.marshmallow
    target_classes = values['target_classes_ids']

    current_base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))

    for target_class_id in target_classes:
        target_class = db_get_or_raise(TargetClass, "target_class_id", str(target_class_id))
        current_base_contest.target_classes.append(target_class)

    db.session.commit()
    return {}, 200


@module.route('/base_olympiad/<int:id_base_olympiad>/remove_target_classes', methods=['POST'],
              input_schema=UpdateTargetClassesOfContestRequestTaskEditorSchema)
def remove_target_classes_from_contest(id_base_olympiad):
    """
    Remove target class from contest
    ---
    post:
      parameters:
        - in: path
          description: ID of the target class
          name: id_base_olympiad
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateTargetClassesOfContestRequestTaskEditorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
        '400':
          description: Bad request
        '409':
          description: Location already in use
    """
    values = request.marshmallow

    target_classes = values['target_classes_ids']

    current_base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))

    for target_class_id in target_classes:
        target_class = db_get_or_raise(TargetClass, "target_class_id", str(target_class_id))
        if target_class in current_base_contest.target_classes:
            current_base_contest.target_classes.remove(target_class)
        else:
            raise NotFound("current_base_contest.target_classes", str(target_class_id))

    db.session.commit()
    return {}, 200


@module.route('/certificate_type', methods=['GET'],
              output_schema=CertificateGetResponseTaskEditorSchema(exclude=[
                  'certificate_types.certificates.text_x',
                  'certificate_types.certificates.text_y',
                  'certificate_types.certificates.text_width',
                  'certificate_types.certificates.text_size',
                  'certificate_types.certificates.text_style',
                  'certificate_types.certificates.text_spacing',
                  'certificate_types.certificates.text_color',
                  'certificate_types.certificates.certificate_type_id'
              ]))
def get_certificate_types():
    """
    Get all certificate types
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CertificateGetResponseTaskEditorSchema
    """
    certificate_types = CertificateType.query.all()
    return {'certificate_types': certificate_types}, 200


@module.route('/certificate_type/<int:certificate_type_id>', methods=['GET'],
              output_schema=CertificateTypeSchema(exclude=[
                  'certificates.text_x',
                  'certificates.text_y',
                  'certificates.text_width',
                  'certificates.text_size',
                  'certificates.text_style',
                  'certificates.text_spacing',
                  'certificates.text_color',
                  'certificates.certificate_type_id'
              ]))
def get_certificate_type_by_id(certificate_type_id):
    """
    Get one certificate type
    ---
    get:
      parameters:
        - in: path
          description: ID of the certificate type
          name: certificate_type_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CertificateTypeSchema
        '404':
          description: Certificate type not found
    """
    certificate_type = db_get_or_raise(CertificateType, 'certificate_type_id', certificate_type_id)
    return certificate_type, 200


@module.route('/certificate/<int:certificate_id>', methods=['GET'], output_schema=CertificateSchema)
def get_certificate_by_id(certificate_id):
    """
    Get one certificate
    ---
    get:
      parameters:
        - in: path
          description: ID of the certificate
          name: certificate_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CertificateSchema
        '404':
          description: Certificate not found
    """
    certificate = db_get_or_raise(Certificate, 'certificate_id', certificate_id)
    return certificate, 200


@module.route('/certificate/<int:certificate_id>/image', methods=['GET'])
def get_certificate_image(certificate_id):
    """
    Get certificate image
    ---
    get:
      parameters:
        - in: path
          description: ID of the certificate
          name: certificate_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            image/png:
              schema:
                type: string
                format: binary
            image/jpeg:
              schema:
                type: string
                format: binary
        '404':
          description: Certificate not found
    """
    certificate = db_get_or_raise(Certificate, 'certificate_id', certificate_id)
    return app.send_media(certificate.certificate_image)
