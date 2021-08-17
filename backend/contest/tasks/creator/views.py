from flask import request

from common import get_current_app, get_current_module
from contest.tasks.creator.schemas import *
from contest.tasks.util import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/base_olympiad/create', methods=['POST'],
              input_schema=CreateBaseOlympiadSchema, output_schema=BaseOlympiadIdSchema)
def base_olympiad_create():
    """
    Create base olympiad
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateBaseOlympiadSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: BaseOlympiadIdSchema
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


@module.route('/base_olympiad/<int:id_base_olympiad>/upload_certificate', methods=['POST'],
              input_schema=BaseCertificateSchema)
def base_olympiad_upload(id_base_olympiad):
    """
    Upload base olympiad certificate
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: BaseCertificateSchema
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
              input_schema=UpdateBaseOlympiadSchema, output_schema=GetBaseOlympiadSchema)
def base_olympiad_patch(id_base_olympiad):
    """
    Patch base olympiad
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
            schema: UpdateBaseOlympiadSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetBaseOlympiadSchema
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

    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=base_contest, session=db.session, partial=True)

    if target_classes is not None:
        base_contest.target_classes = target_classes

    db.session.commit()

    return base_contest.serialize, 200


# Olympiads


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/createsimple', methods=['POST'],
              input_schema=CreateSimpleContestSchema, output_schema=ContestIdSchema)
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
            schema: CreateSimpleContestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestIdSchema
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
              input_schema=CreateCompositeContestSchema, output_schema=ContestIdSchema)
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
            schema: CreateCompositeContestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestIdSchema
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
              input_schema=UpdateContestSchema, output_schema=GetCompositeContestSchema)
def olympiad_patch(id_base_olympiad, id_olympiad):
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
            schema: UpdateContestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetCompositeContestSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow

    contest = db_get_or_raise(Contest, "contest_id", id_olympiad)
    db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))

    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=contest, session=db.session, partial=True)

    db.session.commit()

    return contest, 200


# Stage views


@module.route('/olympiad/<int:id_olympiad>/stage/create', methods=['POST'],
              input_schema=CreateStageSchema, output_schema=StageIdSchema)
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
            schema: CreateStageSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: StageIdSchema
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
              input_schema=UpdateStageSchema, output_schema=GetStageSchema)
def stage_patch(id_olympiad, id_stage):
    """
    Update stage
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
            schema: CreateStageSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: StageIdSchema
        '403':
          description: Invalid role of current user
        '404':
          description: Stage not found
    """

    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    values = request.marshmallow

    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=stage, session=db.session, partial=True)
    db.session.commit()

    return stage.serialize(), 200


# Contest views
@module.route('/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/createsimple',
              methods=['POST'],
              input_schema=CreateSimpleContestSchema, output_schema=ContestIdSchema)
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
            schema: CreateSimpleContestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestIdSchema
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
    previous_contest_id = values.get('previous_contest_id', None)
    previous_participation_condition = values.get('previous_participation_condition', None)

    try:
        validate_contest_values(previous_contest_id, previous_participation_condition)

        stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
        db_get_or_raise(Contest, "contest_id", str(id_olympiad))

        contest = add_simple_contest(db.session,
                                     visibility=visibility,
                                     start_date=start_time,
                                     end_date=end_time,
                                     previous_contest_id=previous_contest_id,
                                     previous_participation_condition=previous_participation_condition,
                                     location=location)

        stage.contests.append(contest)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
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
    input_schema=UpdateContestSchema, output_schema=GetCompositeContestSchema)
def contest_patch(id_olympiad, id_stage, id_contest):
    """
    Update composite contest in stage
    ---
    post:
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
            schema: UpdateContestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetCompositeContestSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    values = request.marshmallow
    contest = get_contest_if_possible_from_stage(id_olympiad, id_stage, id_contest)

    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=contest, session=db.session, partial=True)
    db.session.commit()
    return contest, 200


@module.route(
    '/olympiad/<int:id_olympiad>/stage/<int:id_stage>/contest/<int:id_contest>/add_previous',
    methods=['PATCH'], input_schema=UpdatePreviousContestSchema)
def contest_add_previous(id_olympiad, id_stage, id_contest):
    """
    Update composite contest in stage
    ---
    post:
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
            schema: UpdatePreviousContestSchema
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
              methods=['GET'], output_schema=GetAllStagesSchema)
def contests_all(id_olympiad, id_stage):
    """
    Update composite contest in stage
    ---
    post:
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
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetAllStagesSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    db_get_or_raise(Contest, "contest_id", str(id_olympiad))
    db_get_or_raise(Stage, "stage_id", str(id_stage))
    stage = db_get_or_raise(Stage, "stage_id", str(id_stage))
    all_contests = [contest.serialize() for contest in stage.contests]
    return {"olympiad_list": all_contests}, 200


# Variant views


@module.route(
    '/contest/<int:id_contest>/variant/create',
    methods=['POST'],
    input_schema=CreateVariantSchema, output_schema=VariantIdSchema)
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
            schema: UpdatePreviousContestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: StageIdSchema
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
    methods=['GET'], output_schema=GetVariantSchema)
def variant_get(id_contest, variant_num):
    """
    Get variant
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
              schema: GetVariantSchema
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
    input_schema=UpdateVariantSchema, output_schema=GetVariantSchema)
def variant_patch(id_contest, variant_num):
    """
    Variant patch
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
          description: Num of the variant
          name: variant_num
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateVariantSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetVariantSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    variant = get_variant_if_possible_by_number(id_contest, variant_num)

    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=variant, session=db.session, partial=True)
    db.session.commit()

    return variant, 200


@module.route(
    '/contest/<int:id_contest>/variant/all',
    methods=['GET'],
    input_schema=GetAllVariantsSchema)
def variant_all(id_contest):
    """
    All variants
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
          content:
            application/json:
              schema: GetAllVariantsSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    contest = get_contest_if_possible(id_contest)
    all_variants = [variant for variant in contest.variants.all()]
    return {
               "variants_list": all_variants
           }, 200


# Task views


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createplain',
    methods=['POST'],
    input_schema=CreatePlainSchema, output_schema=TaskIdSchema)
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
            schema: CreatePlainSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskIdSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    num_of_task = values['num_of_task']
    image_of_task = values['image_of_task']
    recommended_answer = values['recommended_answer']

    try:
        variant = get_variant_if_possible(id_contest, id_variant)

        task = add_plain_task(db.session,
                              num_of_task=num_of_task,
                              image_of_task=image_of_task,
                              recommended_answer=recommended_answer,
                              )

        variant.tasks.append(task)

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return {
               "task_id": task.task_id,
           }, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createrange',
    methods=['POST'],
    input_schema=CreateRangeSchema, output_schema=TaskIdSchema)
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
            schema: CreateRangeSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskIdSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow
    num_of_task = values['num_of_task']
    image_of_task = values['image_of_task']
    start_value = values['start_value']
    end_value = values['end_value']

    try:
        variant = get_variant_if_possible(id_contest, id_variant)
        task = add_range_task(db.session,
                              num_of_task=num_of_task,
                              image_of_task=image_of_task,
                              start_value=start_value,
                              end_value=end_value
                              )
        variant.tasks.append(task)
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise
    return {
               "task_id": task.task_id,
           }, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/createmultiple',
    methods=['POST'],
    input_schema=CreateMultipleSchema, output_schema=TaskIdSchema)
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
            schema: CreateRangeSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskIdSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    num_of_task = values['num_of_task']
    image_of_task = values['image_of_task']
    answers = values['answers']
    try:
        variant = get_variant_if_possible(id_contest, id_variant)

        task = add_multiple_task(db.session,
                                 num_of_task=num_of_task,
                                 image_of_task=image_of_task
                                 )
        variant.tasks.append(task)

        task.answers = [
            (answer['task_answer'], answer['is_right_answer'])
            for answer in answers]

        db.session.commit()

    except Exception:
        db.session.rollback()
        raise

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
    output_schema=GetTaskSchema)
def task_get(id_contest, id_variant, id_task):
    """
    Get task
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
        - in: path
          description: ID of the variant
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
              schema: TaskIdSchema
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
    input_schema=UpdatePlainSchema, output_schema=GetTaskSchema)
def task_patch_plain(id_contest, id_variant, id_task):
    """
    Update plain task
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
        - in: path
          description: ID of the ефыл
          name: id_task
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdatePlainSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetTaskSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow

    task = get_task_if_possible(id_contest, id_variant, id_task)

    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=task, session=db.session, partial=True)

    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/range',
    methods=['PATCH'],
    input_schema=UpdateRangeSchema, output_schema=GetTaskSchema)
def task_patch_range(id_contest, id_variant, id_task):
    """
    Update range task
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
        - in: path
          description: ID of the ефыл
          name: id_task
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateRangeSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetTaskSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow
    task = get_task_if_possible(id_contest, id_variant, id_task)
    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=task, session=db.session, partial=True)

    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/<int:id_task>/multiple',
    methods=['PATCH'],
    input_schema=UpdateMultipleSchema, output_schema=GetTaskSchema)
def task_patch_multiple(id_contest, id_variant, id_task):
    """
    Update multiple task
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
        - in: path
          description: ID of the ефыл
          name: id_task
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UpdateMultipleSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetTaskSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    values = request.marshmallow
    task = get_task_if_possible(id_contest, id_variant, id_task)
    answers = values['answers']
    del values['answers']

    serializer = CreateBaseOlympiadSchema()
    serializer.load(values, instance=task, session=db.session, partial=True)

    task.answers = [
        (answer['task_answer'], answer['is_right_answer'])
        for answer in answers]

    db.session.commit()

    return {}, 200


@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/all',
    methods=['GET'],
    output_schema=GetAllTasksSchema)
def task_all(id_contest, id_variant):
    """
    Update multiple task
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
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: GetAllTasksSchema
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
    methods=['GET'],
    output_schema=GetTaskImageSchema)
def task_image(id_contest, id_variant, id_task):
    """
    Get task image
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
        - in: path
          description: ID of the ефыл
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
              schema: GetTaskImageSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    task = get_task_if_possible(id_contest, id_variant, id_task)

    return {
               'task_id': task.task_id,
               'image_of_task': task.image_of_task
           }, 200
