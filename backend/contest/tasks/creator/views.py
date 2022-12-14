from flask import request
from marshmallow import EXCLUDE

from common import get_current_module
from contest.tasks.creator.schemas import *
from contest.tasks.model_schemas.tasks import TaskPoolSchema, ContestTaskSchema, PlainTaskSchema, RangeTaskSchema, \
    MultipleChoiceTaskSchema
from contest.tasks.model_schemas.user import UserInContestSchema
from contest.tasks.util import *
from common.util import db_get_all

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/base_olympiad/create', methods=['POST'],
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
            schema: BaseContestSchema
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
    base_contest = BaseContestSchema().load(request.json, session=db.session, partial=False, unknown=EXCLUDE)
    db.session.add(base_contest)
    db.session.commit()

    return {
               'base_contest_id': base_contest.base_contest_id
           }, 200


@module.route('contest/<int:contest_id>/user/<int:user_id>/proctor_data', methods=['POST'],
              input_schema=UserProctoringDataRequestTaskCreatorSchema)
def set_proctor_data(contest_id, user_id):
    """
    Set proctor data
    ---
    post:
      parameters:
        - in: path
          description: ID of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the contest
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UserProctoringDataRequestTaskCreatorSchema
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
    current_user = UserInContest.query.filter_by(user_id=user_id, contest_id=contest_id).one_or_none()
    UserInContestSchema(load_instance=True).load(request.json, instance=current_user, session=db.session,
                                                 partial=True, unknown=EXCLUDE)
    db.session.commit()

    return {}, 200


@module.route('contest/<int:contest_id>/user/<int:user_id>/proctor_data', methods=['GET'],
              output_schema=UserProctoringDataRequestTaskCreatorSchema)
def get_proctor_data(contest_id, user_id):
    """
    Get proctor data
    ---
    get:
      parameters:
        - in: path
          description: ID of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: ID of the contest
          name: user_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
       responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserProctoringDataRequestTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    current_user = UserInContest.query.filter_by(user_id=user_id, contest_id=contest_id).one_or_none()
    return {
               "proctoring_login": current_user.proctoring_login,
               "proctoring_password": current_user.proctoring_password,
           }, 200


# Tasks Pool

@module.route('/base_olympiad/<int:id_base_olympiad>/task_pool/create', methods=['POST'],
              output_schema=TaskPoolIdResponseTaskCreatorSchema)
def task_pool_create(id_base_olympiad):
    """
    Create task pool
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
            schema: TaskPoolSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskPoolIdResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    base_contest = db_get_or_raise(BaseContest, "base_contest_id", id_base_olympiad)

    task_pool = TaskPoolSchema().load(data=request.json, partial=False, session=db.session, unknown=EXCLUDE)

    db.session.add(task_pool)
    base_contest.task_pools.append(task_pool)
    db.session.commit()

    return {
               'task_pool_id': task_pool.task_pool_id
           }, 200


@module.route('/base_olympiad/<int:id_base_olympiad>/task_pool/<int:id_task_pool>', methods=['GET'],
              output_schema=TaskPoolSchema)
def task_pool_get(id_base_olympiad, id_task_pool):
    """
    Create task pool
    ---
    get:
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
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: TaskPoolSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    task_pool = db_get_or_raise(TaskPool, "task_pool_id", id_task_pool)
    return task_pool, 200


@module.route('/task_pool/all', methods=['GET'],
              output_schema=AllTaskPoolsResponseTaskCreatorSchema)
def task_pool_get_all():
    """
    Create task pool
    ---
    get:
      parameters:
        - in: query
          name: base_contest_id
          required: false
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
              schema: AllTaskPoolsResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    args = request.args
    marshmallow = FilterTaskPoolAllRequestSchema().load(args)
    base_contest_id = marshmallow.get('base_contest_id', None)
    if base_contest_id is not None:
        base_contest = db_get_or_raise(BaseContest, "base_contest_id", base_contest_id)
        task_pools = base_contest.task_pools
    else:
        task_pools = db_get_all(TaskPool)
    return {
               "task_pools_list": task_pools
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
    deadline_for_appeal = values.get('deadline_for_appeal', None)
    show_result_after_finish = values.get('show_result_after_finish', False)
    stage_id = values.get('stage_id', None)
    previous_contest_id = values.get('previous_contest_id', None)
    show_answer_after_contest = values.get('show_answer_after_contest', None)
    previous_participation_condition = values.get('previous_participation_condition', None)

    holding_type = values.get('holding_type', None)

    regulations = values.get('regulations', None)

    validate_contest_values(previous_contest_id, previous_participation_condition)

    base_contest = db_get_or_raise(BaseContest, "base_contest_id", str(id_base_olympiad))

    current_contest = add_simple_contest(db.session,
                                         base_contest_id=id_base_olympiad,
                                         visibility=visibility,
                                         start_date=start_date,
                                         end_date=end_date,
                                         holding_type=holding_type,
                                         regulations=regulations,
                                         show_answer_after_contest=show_answer_after_contest,
                                         previous_contest_id=previous_contest_id,
                                         previous_participation_condition=previous_participation_condition,
                                         end_of_enroll_date=end_of_enroll_date,
                                         deadline_for_appeal=deadline_for_appeal,
                                         contest_duration=contest_duration,
                                         show_result_after_finish=show_result_after_finish,
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


# Contest task


@module.route('/contest/<int:id_contest>/contest_task/create', methods=['POST'],
              output_schema=ContestTaskResponseTaskCreatorSchema)
def contest_task_create(id_contest):
    """
    Create contest task
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: ContestTaskSchema
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
              schema: ContestTaskResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    contest_task = ContestTaskSchema().load(data=request.json, partial=False, session=db.session, unknown=EXCLUDE)
    contest_: Contest = db_get_or_raise(Contest, "contest_id", id_contest)

    previous_pools = {
        task_pool_
        for contest_task_ in contest_.contest_tasks.all()
        for task_pool_ in contest_task_.task_pools}

    if len(previous_pools) != 0:
        if previous_pools & set(contest_task.task_pools):
            raise AlreadyExists("task_pool", "task_pool_id")

    contest_.contest_tasks.append(contest_task)
    db.session.commit()

    return {
               'contest_task_id': contest_task.contest_task_id
           }, 200


@module.route('/contest/<int:id_contest>/contest_task/<int:id_contest_task>', methods=['GET'],
              output_schema=ContestTaskSchema)
def contest_task_get(id_contest, id_contest_task):
    """
    Create contest task
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
          description: ID of the contest task
          name: id_contest_task
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
              schema: ContestTaskSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """

    contest_task = db_get_or_raise(ContestTask, "contest_task_id", id_contest_task)
    return contest_task, 200


@module.route('/contest/<int:id_contest>/contest_task/all', methods=['GET'],
              output_schema=AllContestTaskResponseTaskCreatorSchema)
def contest_task_get_all(id_contest):
    """
    Get all contest task
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
              schema: AllContestTaskResponseTaskCreatorSchema
        '400':
          description: Bad request
        '404':
          description: Contest not found
        '409':
          description: Olympiad type already in use
    """

    contest_: Contest = db_get_or_raise(Contest, "contest_id", id_contest)
    return {
               "contest_task_list": contest_.contest_tasks
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
    '/task_pool/<int:id_task_pool>/task/create_plain',
    methods=['POST'],
    output_schema=TaskIdResponseTaskCreatorSchema)
def task_create_plain(id_task_pool):
    """
    Create plain task
    ---
    post:
      parameters:
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
            schema: PlainTaskSchema
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
    task_pool = db_get_or_raise(TaskPool, "task_pool_id", id_task_pool)

    task = PlainTaskSchema().load(request.json, session=db.session, partial=False, unknown=EXCLUDE)
    db.session.add(task)

    task_pool.tasks.append(task)

    db.session.commit()

    return {
               "task_id": task.task_id,
           }, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/create_range',
    methods=['POST'],
    output_schema=TaskIdResponseTaskCreatorSchema)
def task_create_range(id_task_pool):
    """
    Create range task
    ---
    post:
      parameters:
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
            schema: RangeTaskSchema
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
    task_pool = db_get_or_raise(TaskPool, "task_pool_id", id_task_pool)
    task = RangeTaskSchema().load(request.json, session=db.session, partial=False, unknown=EXCLUDE)
    db.session.add(task)

    task_pool.tasks.append(task)
    db.session.commit()

    return {
               "task_id": task.task_id,
           }, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/create_multiple',
    methods=['POST'],
    output_schema=TaskIdResponseTaskCreatorSchema)
def task_create_multiple(id_task_pool):
    """
    Create multiple task
    ---
    post:
      parameters:
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
            schema: MultipleChoiceTaskSchema
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
    values = request.json
    task_pool = db_get_or_raise(TaskPool, "task_pool_id", id_task_pool)
    task = MultipleChoiceTaskSchema().load(request.json, session=db.session, partial=False, unknown=EXCLUDE)
    db.session.add(task)
    task_pool.tasks.append(task)
    db.session.commit()

    return {
               "task_id": task.task_id,
           }, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/<int:id_task>',
    methods=['GET'],
    output_schema=TaskResponseTaskCreatorSchema)
def task_get(id_task_pool, id_task):
    """
    Get task
    ---
    get:
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
          content:
            application/json:
              schema: TaskResponseTaskCreatorSchema
        '400':
          description: Bad request
        '409':
          description: Olympiad type already in use
    """
    task = get_task_in_pool_if_possible(id_task_pool, id_task)
    return task, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/all',
    methods=['GET'],
    output_schema=AllTasksResponseTaskCreatorSchema)
def task_all(id_task_pool):
    """
    Update multiple task
    ---
    get:
      parameters:
        - in: path
          description: ID of the task pool
          name: id_task_pool
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

    task_pool = db_get_or_raise(TaskPool, "task_pool_id", id_task_pool)
    tasks_list = task_pool.tasks
    return {
               "tasks_list": tasks_list
           }, 200


@module.route(
    '/task_pool/<int:id_task_pool>/task/<int:id_task>/image',
    methods=['GET'])
def task_image(id_task_pool, id_task):
    """
    Get task image
    ---
    get:
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
    task = get_task_in_pool_if_possible(id_task_pool, id_task)
    return app.send_media(task.image_of_task)


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
