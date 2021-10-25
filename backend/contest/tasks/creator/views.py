import io

from flask import request
from flask import send_file
from common import get_current_module
from contest.tasks.creator.schemas import *
from contest.tasks.util import *

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

    winner_1_condition = values['winner_1_condition']
    winner_2_condition = values['winner_2_condition']
    winner_3_condition = values['winner_3_condition']
    diploma_1_condition = values['diploma_1_condition']
    diploma_2_condition = values['diploma_2_condition']
    diploma_3_condition = values['diploma_3_condition']

    subject = values['subject']
    level = values['level']

    db_get_or_raise(OlympiadType, "olympiad_type_id", values["olympiad_type_id"])
    base_contest = add_base_contest(db.session,
                                    description=description,
                                    name=name,
                                    certificate_template=None,
                                    winner_1_condition=winner_1_condition,
                                    winner_2_condition=winner_2_condition,
                                    winner_3_condition=winner_3_condition,
                                    diploma_1_condition=diploma_1_condition,
                                    diploma_2_condition=diploma_2_condition,
                                    diploma_3_condition=diploma_3_condition,
                                    rules=rules,
                                    olympiad_type_id=olympiad_type_id,
                                    subject=subject,
                                    level=level)

    db.session.commit()

    return {
               'base_contest_id': base_contest.base_contest_id
           }, 200


# Olympiads


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/create_simple', methods=['POST'],
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
    start_date = values['start_date']
    end_date = values['end_date']
    contest_duration = values.get('contest_duration', None)
    result_publication_date = values.get('result_publication_date', None)
    end_of_enroll_date = values.get('end_of_enroll_date', None)
    stage_id = values.get('stage_id', None)
    previous_contest_id = values.get('previous_contest_id', None)
    previous_participation_condition = values.get('previous_participation_condition', None)
    holding_type = values.get('holding_type', None)

    validate_contest_values(previous_contest_id, previous_participation_condition)

    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))

    current_contest = add_simple_contest(db.session,
                                         base_contest_id=id_base_olympiad,
                                         visibility=visibility,
                                         start_date=start_date,
                                         end_date=end_date,
                                         holding_type=holding_type,
                                         previous_contest_id=previous_contest_id,
                                         previous_participation_condition=previous_participation_condition,
                                         end_of_enroll_date=end_of_enroll_date,
                                         contest_duration=contest_duration,
                                         result_publication_date=result_publication_date)

    if previous_contest_id is not None:
        prev_contest = db_get_or_raise(Contest, "contest_id", str(previous_contest_id))
        prev_contest.next_contests.append(current_contest)

    if stage_id is not None:
        stage = db_get_or_raise(Stage, "stage_id", str(stage_id))
        stage.contests.append(current_contest)
    else:
        base_contest.child_contests.append(current_contest)

    db.session.commit()

    return {
               'contest_id': current_contest.contest_id
           }, 200


@module.route('/base_olympiad/<int:id_base_olympiad>/olympiad/create_composite', methods=['POST'],
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
    current_contest = add_composite_contest(db.session,
                                            visibility=visibility)
    base_contest.child_contests.append(current_contest)

    db.session.commit()

    return {
               'contest_id': current_contest.contest_id
           }, 200


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

    current_contest = get_composite_contest_if_possible(id_olympiad)

    stage = add_stage(db.session,
                      stage_name=stage_name,
                      stage_num=stage_num,
                      condition=condition,
                      this_stage_condition=this_stage_condition,
                      )
    current_contest.stages.append(stage)
    db.session.commit()

    return {
               'stage_id': stage.stage_id
           }, 200


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
    variant_description = values['variant_description']

    current_contest = get_contest_if_possible(id_contest)
    last_variant_number = get_last_variant_in_contest(current_contest)

    variant = add_variant(db.session,
                          variant_number=last_variant_number + 1,
                          variant_description=variant_description,
                          )
    current_contest.variants.append(variant)

    db.session.add(variant)
    db.session.commit()

    return {
               "variant_id": variant.variant_id,
           }, 200


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
    current_contest = get_contest_if_possible(id_contest)
    return {
               "variants_list": current_contest.variants.all()
           }, 200


# Task views

@module.route(
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/create_plain',
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
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/create_range',
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
    '/contest/<int:id_contest>/variant/<int:id_variant>/task/create_multiple',
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
    tasks_list = get_tasks_if_possible(id_contest, id_variant)
    return {
               "tasks_list": tasks_list
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


# Group Restriction


@module.route('/contest/<int:contest_id>/restrictions', methods=['PUT'],
              input_schema=ContestGroupRestrictionListAdminSchema)
def contest_restriction_create(contest_id):
    """
    Add new restriction
    ---
    put:
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
            schema: ContestGroupRestrictionListAdminSchema
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
    restrictions = values['restrictions']
    current_contest: Contest = db_get_or_raise(Contest, 'contest_id', contest_id)
    for old_restriction in current_contest.group_restrictions.all():
        db.session.delete(old_restriction)
    new_restrictions = []
    for restriction_elem in restrictions:
        group_name = restriction_elem['group_name']
        restriction = restriction_elem['restriction']
        group = db_get_or_raise(Group, 'name', group_name)
        new_restrictions.append(ContestGroupRestriction(contest_id=contest_id,
                                                        group_id=group.id,
                                                        restriction=restriction))
    current_contest.group_restrictions = new_restrictions
    db.session.commit()
    return {}, 200


@module.route('/contest/<int:contest_id>/restrictions', methods=['GET'],
              output_schema=ContestGroupRestrictionListAdminSchema)
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
              schema: ContestGroupRestrictionListAdminSchema
        '400':
          description: Bad request
        '404':
          description: Contest or group not found
    """
    current_contest: SimpleContest = db_get_or_raise(SimpleContest, 'contest_id', contest_id)
    restrictions = current_contest.group_restrictions.all()
    return {"restrictions": restrictions}, 200
