import io

from flask import request
from marshmallow import EXCLUDE

from common import get_current_app, get_current_module
from contest.tasks.creator.schemas import *
from contest.tasks.model_schemas.schemas import SimpleContestSchema, CompositeContestSchema, PlainTaskSchema, \
    RangeTaskSchema, MultipleChoiceTaskSchema
from contest.tasks.util import *

from flask import send_file

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/base_olympiad/create', methods=['POST'],
              input_schema=CreateBaseOlympiadRequestTaskCreatorSchema,
              output_schema=BaseOlympiadIdResponseTaskCreatorSchema)
def base_olympiad_create():
    """
    Create base olympiad
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateBaseOlympiadRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: BaseOlympiadIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow

    name = values['name']
    description = values['description']
    rules = values['rules']
    olympiad_type_id = values['olympiad_type_id']
    winning_condition = values['winning_condition']
    laureate_condition = values['laureate_condition']
    subject = values['subject']
    target_classes = set(values['target_classes'])

    db_get_or_raise(OlympiadType, "olympiad_type_id", values["olympiad_type_id"])
    base_contest = add_base_contest(db.session,
                                    description=description,
                                    name=name,
                                    certificate_template=None,
                                    winning_condition=winning_condition,
                                    laureate_condition=laureate_condition,
                                    rules=rules,
                                    olympiad_type_id=olympiad_type_id,
                                    subject=subject)

    base_contest.target_classes = target_classes

    db.session.commit()

    return {
               'base_contest_id': base_contest.base_contest_id
           }, 200


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
              input_schema=UpdateBaseOlympiadRequestTaskCreatorSchema,
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
            schema: UpdateBaseOlympiadRequestTaskCreatorSchema
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

    target_classes = set(values['target_classes'])
    del values["target_classes"]

    BaseContestSchema(load_instance=True).load(request.json, instance=base_contest, session=db.session,
                                               partial=False, unknown=EXCLUDE)

    if target_classes is not None:
        base_contest.target_classes = target_classes

    db.session.commit()

    return base_contest, 200


# Olympiads


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/createsimple', methods=['POST'],
              input_schema=CreateSimpleContestRequestTaskCreatorSchema,
              output_schema=ContestIdResponseTaskCreatorSchema)
def olympiad_create_simple(id_base_olympiad):
    """
    Create simple contest
    ---
    post:
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
            schema: CreateSimpleContestRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    visibility = values['visibility']
    start_time = values['start_time']
    end_time = values['end_time']
    previous_contest_id = values.get('previous_contest_id', None)
    location = values.get('location', None)
    previous_participation_condition = values.get('previous_participation_condition', None)

    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    contest = add_simple_contest(db.session,
                                 visibility=visibility,
                                 start_date=start_time,
                                 end_date=end_time,
                                 previous_participation_condition=previous_participation_condition,
                                 location=location,
                                 )
    if previous_contest_id is not None:
        prev_contest = db_get_or_raise(Contest, "contest_id", str(previous_contest_id))
        prev_contest.next_contests.append(contest)
    base_contest.child_contests.append(contest)

    db.session.commit()

    return {
               'contest_id': contest.contest_id
           }, 200


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/createcomposite', methods=['POST'],
              input_schema=CreateCompositeContestRequestTaskCreatorSchema,
              output_schema=ContestIdResponseTaskCreatorSchema)
def olympiad_create_composite(id_base_olympiad):
    """
    Create composite contest
    ---
    post:
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
            schema: CreateCompositeContestRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    visibility = values['visibility']

    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))
    contest = add_composite_contest(db.session,
                                    visibility=visibility)
    base_contest.child_contests.append(contest)

    db.session.commit()

    return {
               'contest_id': contest.contest_id
           }, 200


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
    contest = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db.session.delete(contest)
    db.session.commit()
    return {}, 200


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/<int:id_olympiad>', methods=['PATCH'],
              input_schema=UpdateContestRequestTaskCreatorSchema,
              output_schema=CompositeContestResponseTaskCreatorSchema)
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
            schema: UpdateContestRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CompositeContestResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))

    if contest.composite_type == ContestTypeEnum.SimpleContest:
        SimpleContestSchema(load_instance=True).load(request.json, instance=contest, session=db.session,
                                                     partial=False, unknown=EXCLUDE)
    else:
        CompositeContestSchema(load_instance=True).load(request.json, instance=contest, session=db.session,
                                                        partial=False, unknown=EXCLUDE)

    db.session.commit()
    return contest, 200


# Stage views


@module.route('/olympiad/<int:id_olympiad>/stage/create', methods=['POST'],
              input_schema=CreateStageRequestTaskCreatorSchema,
              output_schema=StageIdResponseTaskCreatorSchema)
def stage_create(id_olympiad):
    """
    Create stage
    ---
    post:
      parameters:
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
            schema: CreateStageRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: StageIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    stage_name = values['stage_name']
    stage_num = values['stage_num']
    condition = values['condition']
    this_stage_condition = values['this_stage_condition']

    contest = db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    if contest.composite_type == ContestTypeEnum.SimpleContest:
        raise InsufficientData('contest.composite_type', 'not composite')
    stage = add_stage(db.session,
                      stage_name=stage_name,
                      stage_num=stage_num,
                      condition=condition,
                      this_stage_condition=this_stage_condition,
                      )
    contest.stages.append(stage)
    db.session.commit()

    return {
               'stage_id': stage.stage_id
           }, 200


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
              input_schema=UpdateStageRequestTaskCreatorSchema,
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
            schema: UpdateStageRequestTaskCreatorSchema
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
@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/createsimple',
              methods=['POST'],
              input_schema=CreateSimpleContestRequestTaskCreatorSchema,
              output_schema=ContestIdResponseTaskCreatorSchema)
def contest_create_simple(id_olympiad, id_stage):
    """
    Create simple contest in stage
    ---
    post:
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
            schema: CreateSimpleContestRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow

    visibility = values['visibility']
    start_time = values['start_time']
    end_time = values['end_time']
    location = values.get('location', None)
    result_publication_date = values.get('result_publication_date', None)
    previous_contest_id = values.get('previous_contest_id', None)
    previous_participation_condition = values.get('previous_participation_condition', None)
    holding_type = values.get('holding_type', None)

    validate_contest_values(previous_contest_id, previous_participation_condition)

    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    main_contest = db_get_or_raise(Contest, "contest_id", str(id_olympiad))

    if main_contest.composite_type != ContestTypeEnum.CompositeContest:
        raise InsufficientData("composite_type", "not Composite")

    if stage not in main_contest.stages:
        raise InsufficientData("stage_id", "not in current stage")

    contest = add_simple_contest(db.session,
                                 visibility=visibility,
                                 start_date=start_time,
                                 end_date=end_time,
                                 holding_type=holding_type,
                                 previous_contest_id=previous_contest_id,
                                 previous_participation_condition=previous_participation_condition,
                                 result_publication_date=result_publication_date,
                                 location=location)

    stage.contests.append(contest)

    db.session.commit()

    return {
               'contest_id': contest.contest_id
           }, 200


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

    contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    db.session.delete(contest)
    db.session.commit()
    return {}, 200


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>',
    methods=['PATCH'],
    input_schema=UpdateContestRequestTaskCreatorSchema,
    output_schema=CompositeContestResponseTaskCreatorSchema)
def contest_patch(id_olympiad, id_stage, id_contest):
    """
    Update simple contest in stage
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
            schema: UpdateContestRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: CompositeContestResponseTaskCreatorSchema
        '400':
          description: Bad request
        '404':
          description: Not found
        '409':
          description: Olympiad type already in use
    """

    contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)

    SimpleContestSchema(load_instance=True).load(request.json, instance=contest, session=db.session,
                                                 partial=False, unknown=EXCLUDE)

    db.session.commit()
    return contest, 200


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/add_previous',
    methods=['PATCH'], input_schema=UpdatePreviousContestRequestTaskCreatorSchema)
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
            schema: UpdatePreviousContestRequestTaskCreatorSchema
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
    contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)
    values = request.marshmallow
    contest.change_previous(**values)
    db.session.commit()

    return {}, 200


@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/all',
              methods=['GET'], output_schema=AllOlympiadsResponseTaskCreatorSchema)
def contests_all(id_olympiad, id_stage):
    """
    Update composite contest in stage
    ---
    get:
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
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllOlympiadsResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    return {
               "olympiad_list": stage.contests
           }, 200


# Variant views


@module.route(
    '/contest/<int:id_contest>/variant/create',
    methods=['POST'],
    input_schema=CreateVariantRequestTaskCreatorSchema,
    output_schema=VariantIdResponseTaskCreatorSchema)
def variant_create(id_contest):
    """
    Variant creation
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
            schema: CreateVariantRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: VariantIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow
    contest = get_contest_if_possible(id_contest)
    last_variant_number = get_last_variant_in_contest(contest)
    variant_description = values['variant_description']

    variant = add_variant(db.session,
                          variant_number=last_variant_number + 1,
                          variant_description=variant_description,
                          )
    contest.variants.append(variant)

    db.session.add(variant)
    db.session.commit()

    return {
               "variant_id": variant.variant_id,
           }, 200


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
    methods=['GET'], output_schema=VariantResponseTaskCreatorSchema)
def variant_get(id_contest, variant_num):
    """
    Get variant
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
          description: Num of the variant
          name: variant_num
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
              schema: VariantResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    variant = get_variant_if_possible_by_number(id_contest, variant_num)
    return variant, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:variant_num>',
    methods=['PATCH'],
    input_schema=UpdateVariantRequestTaskCreatorSchema,
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
            schema: UpdateVariantRequestTaskCreatorSchema
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


@module.route(
    '/contest/<int:id_contest>/variant/all',
    methods=['GET'],
    output_schema=AllVariantsResponseTaskCreatorSchema)
def variant_all(id_contest):
    """
    All variants
    ---
    get:
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
          content:
            application/json:
              schema: AllVariantsResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    contest = get_contest_if_possible(id_contest)
    return {
               "variants_list": contest.variants.all()
           }, 200


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

    task = get_task_if_possible(id_contest, id_variant, id_task)
    task.image_of_task = image_of_task

    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createplain',
    methods=['POST'],
    input_schema=CreatePlainRequestTaskCreatorSchema,
    output_schema=TaskIdResponseTaskCreatorSchema)
def task_create_plain(id_contest, id_variant):
    """
    Create plain task
    ---
    post:
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
      requestBody:
        required: true
        content:
          application/json:
            schema: CreatePlainRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    num_of_task = values['num_of_task']
    recommended_answer = values['recommended_answer']
    show_answer_after_contest = values.get('show_answer_after_contest', None)
    task_points = values.get('task_points', None)

    variant = get_variant_if_possible(id_contest, id_variant)

    task = add_plain_task(db.session,
                          num_of_task=num_of_task,
                          recommended_answer=recommended_answer,
                          show_answer_after_contest=show_answer_after_contest,
                          task_points=task_points,
                          )

    variant.tasks.append(task)

    db.session.commit()

    return {
               "task_id": task.task_id,
           }, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createrange',
    methods=['POST'],
    input_schema=CreateRangeRequestTaskCreatorSchema, output_schema=TaskIdResponseTaskCreatorSchema)
def task_create_range(id_contest, id_variant):
    """
    Create range task
    ---
    post:
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
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateRangeRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow
    num_of_task = values['num_of_task']
    start_value = values['start_value']
    end_value = values['end_value']
    show_answer_after_contest = values.get('show_answer_after_contest', None)
    task_points = values.get('task_points', None)

    variant = get_variant_if_possible(id_contest, id_variant)
    task = add_range_task(db.session,
                          num_of_task=num_of_task,
                          start_value=start_value,
                          end_value=end_value,
                          show_answer_after_contest=show_answer_after_contest,
                          task_points=task_points,
                          )
    variant.tasks.append(task)
    db.session.commit()

    return {
               "task_id": task.task_id,
           }, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createmultiple',
    methods=['POST'],
    input_schema=CreateMultipleRequestTaskCreatorSchema, output_schema=TaskIdResponseTaskCreatorSchema)
def task_create_multiple(id_contest, id_variant):
    """
    Create multiple task
    ---
    post:
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
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateMultipleRequestTaskCreatorSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    num_of_task = values['num_of_task']
    answers = values['answers']
    show_answer_after_contest = values.get('show_answer_after_contest', None)
    task_points = values.get('task_points', None)

    variant = get_variant_if_possible(id_contest, id_variant)

    task = add_multiple_task(db.session,
                             num_of_task=num_of_task,
                             show_answer_after_contest=show_answer_after_contest,
                             task_points=task_points,
                             )
    variant.tasks.append(task)

    task.answers = [
        {
            "answer": answer['answer'],
            "is_right_answer": answer['is_right_answer']}
        for answer in answers]

    db.session.commit()

    return {
               "task_id": task.task_id,
           }, 200


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
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>',
    methods=['GET'],
    output_schema=TaskResponseTaskCreatorSchema)
def task_get(id_contest, id_variant, id_task):
    """
    Get task
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
          content:
            application/json:
              schema: TaskResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    task = get_task_if_possible(id_contest, id_variant, id_task)
    return task, 200


def check_existence(id_olympiad, id_stage, id_contest, id_variant):
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    db_get_or_raise(Contest, "contest_id", str(id_contest))
    db_get_or_raise(Variant, "variant_id", str(id_variant))


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/plain',
    methods=['PATCH'],
    input_schema=UpdatePlainRequestTaskCreatorSchema, output_schema=TaskResponseTaskCreatorSchema)
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
            schema: UpdatePlainRequestTaskCreatorSchema
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
    input_schema=UpdateRangeRequestTaskCreatorSchema, output_schema=TaskResponseTaskCreatorSchema)
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
            schema: UpdateRangeRequestTaskCreatorSchema
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
    input_schema=UpdateMultipleRequestTaskCreatorSchema, output_schema=TaskResponseTaskCreatorSchema)
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
            schema: UpdateMultipleRequestTaskCreatorSchema
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


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/all',
    methods=['GET'],
    output_schema=AllTasksResponseTaskCreatorSchema)
def task_all(id_contest, id_variant):
    """
    Update multiple task
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
          description: ID of the variant
          name: id_variant
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
              schema: AllTasksResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    tasks = get_tasks_if_possible(id_contest, id_variant)
    return {
               "tasks_list": tasks
           }, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/tasks/<int:id_task>/image',
    methods=['GET'])
def task_image(id_contest, id_variant, id_task):
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
    task = get_task_if_possible(id_contest, id_variant, id_task)

    if task.image_of_task is None:
        raise InsufficientData("task", "image_of_task")

    return send_file(io.BytesIO(task.image_of_task),
                     attachment_filename='task_image.png',
                     mimetype='image/jpeg'), 200
