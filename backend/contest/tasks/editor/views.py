from flask import request
from marshmallow import EXCLUDE

from common import get_current_module
from contest.tasks.creator.schemas import BaseOlympiadResponseTaskCreatorSchema, StageResponseTaskCreatorSchema, \
    ContestResponseTaskCreatorSchema, TaskResponseTaskCreatorSchema, VariantResponseTaskCreatorSchema
from contest.tasks.editor.schemas import *
from contest.tasks.model_schemas.contest import StageSchema, VariantSchema
from contest.tasks.model_schemas.olympiad import BaseContestSchema, SimpleContestSchema, CompositeContestSchema
from contest.tasks.model_schemas.tasks import PlainTaskSchema, RangeTaskSchema, MultipleChoiceTaskSchema
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/base_olympiad/<int:id_base_olympiad>/upload_certificate', methods=['POST'])
def base_olympiad_upload(id_base_olympiad):
    """
    Upload base olympiad certificate
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
          description: Id of the olympiad
          name: id_base_olympiad
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

    certificate_template = request.data

    validate_file_size(certificate_template)

    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)
    base_contest.certificate_template = certificate_template
    db.session.commit()

    return {}, 200


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
                                               partial=False, unknown=EXCLUDE)

    db.session.commit()

    return base_contest, 200


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
                                         partial=False, unknown=EXCLUDE)

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


# Variant views


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/remove',
    methods=['POST'])
def variant_remove(id_contest, id_variant):
    """
    Delete a contest
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the variant
          name: id_variant
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

    variant = get_variant_if_possible(id_contest, id_variant)
    db.session.delete(variant)
    db.session.commit()
    return {}, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:variant_num>',
    methods=['PATCH'],
    input_schema=UpdateVariantRequestTaskEditorSchema,
    output_schema=VariantResponseTaskCreatorSchema)
def variant_patch(id_contest, variant_num):
    """
    Variant patch
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
          description: Num of the variant
          name: variant_num
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateVariantRequestTaskEditorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: VariantResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    variant = get_variant_if_possible_by_number(id_contest, variant_num)

    VariantSchema(load_instance=True).load(request.json, instance=variant, session=db.session,
                                           partial=False, unknown=EXCLUDE)

    db.session.commit()

    return variant, 200


# Task views


@module.route('/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/upload_image',
              methods=['POST'])
def task_image_upload(id_contest, id_variant, id_task):
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
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the variant
          name: id_variant
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

    image_of_task = request.data

    validate_file_size(image_of_task)

    task = get_task_if_possible(id_contest, id_variant, id_task)
    task.image_of_task = image_of_task

    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/remove',
    methods=['POST'])
def task_remove(id_contest, id_variant, id_task):
    """
    Delete a task
    ---
    post:
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      parameters:
        - in: path
          description: ID of the contest
          name: id_contest
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the variant
          name: id_variant
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

    task = get_task_if_possible(id_contest, id_variant, id_task)
    db.session.delete(task)
    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/plain',
    methods=['PATCH'],
    input_schema=UpdatePlainRequestTaskEditorSchema, output_schema=TaskResponseTaskCreatorSchema)
def task_patch_plain(id_contest, id_variant, id_task):
    """
    Update plain task
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
          description: ID of the variant
          name: id_variant
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
            schema: UpdatePlainRequestTaskEditorSchema
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
    task = get_task_if_possible(id_contest, id_variant, id_task)

    PlainTaskSchema(load_instance=True).load(request.json, instance=task, session=db.session,
                                             partial=False, unknown=EXCLUDE)

    db.session.commit()

    return task, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/range',
    methods=['PATCH'],
    input_schema=UpdateRangeRequestTaskEditorSchema, output_schema=TaskResponseTaskCreatorSchema)
def task_patch_range(id_contest, id_variant, id_task):
    """
    Update range task
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
          description: ID of the variant
          name: id_variant
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
            schema: UpdateRangeRequestTaskEditorSchema
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
    task = get_task_if_possible(id_contest, id_variant, id_task)

    RangeTaskSchema(load_instance=True).load(request.json, instance=task, session=db.session,
                                             partial=False, unknown=EXCLUDE)

    db.session.commit()

    return task, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/multiple',
    methods=['PATCH'],
    input_schema=UpdateMultipleRequestTaskEditorSchema, output_schema=TaskResponseTaskCreatorSchema)
def task_patch_multiple(id_contest, id_variant, id_task):
    """
    Update multiple task
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
          description: ID of the variant
          name: id_variant
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
            schema: UpdateMultipleRequestTaskEditorSchema
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
    values = request.marshmallow
    task = get_task_if_possible(id_contest, id_variant, id_task)
    answers = values['answers']
    del values['answers']

    MultipleChoiceTaskSchema(load_instance=True).load(values, instance=task, session=db.session,
                                                      partial=False, unknown=EXCLUDE)
    task.answers = [
        {
            "answer": answer['answer'],
            "is_right_answer": answer['is_right_answer']}
        for answer in answers]

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
