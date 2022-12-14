from flask import request
from common import get_current_module
from contest.responses.util import *
from common.jwt_verify import jwt_get_id, jwt_get_role
from contest.responses.model_schemas.schemas import UserAnswerSchema
from .schemas import *
from contest.tasks.models.olympiad import ContestGroupRestrictionEnum

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/user/<int:user_id>/create', methods=['POST'])
def create_user_response_for_contest(contest_id, user_id):
    """
    Create user's response for contest
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Permission Denied
        '404':
          description: User or contest not found
        '409':
          description: Timing error
    """
    creator_id = jwt_get_id()
    check_user_role(creator_id)
    create_user_response(contest_id, user_id)
    return {}, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/response', methods=['GET'],
              output_schema=AllUserAnswersResponseSchema)
def get_user_by_id_all_answers(contest_id, user_id):
    """
    Get all user answers for the contest
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllUserAnswersResponseSchema
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_response)
    return get_all_user_answers(user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/mark', methods=['GET'],
              output_schema=AllUserMarksResponseSchema)
def get_user_by_id_all_marks(contest_id, user_id):
    """
    Get all user marks for the contest
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllUserMarksResponseSchema
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_mark_and_user_status)
    return get_all_user_answers(user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/results', methods=['GET'],
              output_schema=UserResultForContestResponseSchema)
def get_user_by_id_results_for_contest(contest_id, user_id):
    """
    Get user results for contest
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserResultForContestResponseSchema
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
        '409':
          description: Olympiad isn't over
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_mark_and_user_status)
    if_user_ended_his_response(user_id, contest_id)
    return get_user_results_and_variant(user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/plain/file', methods=['GET'])
def user_answer_for_task_by_id_plain_file(contest_id, task_id, user_id):
    """
    Get user answer file for plain task
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            image/png: {schema: {format: binary, type: string}}
            application/pdf: {schema: {format: binary, type: string}}
            image/jpeg: {schema: {format: binary, type: string}}
            image/gif: {schema: {format: binary, type: string}}
            text/plain: {schema: {format: binary, type: string}}
            application/msword: {schema: {format: binary, type: string}}
            application/zip: {schema: {format: binary, type: string}}
        '403':
          description: Restriction error
        '404':
          description: User, contest or task not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_response)
    user_answer = user_answer_get(user_id, contest_id, task_id, 'PlainAnswerFile')
    return app.send_media(user_answer.answer_content)


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>', methods=['GET'],
              output_schema=UserAnswerSchema)
def user_answer_for_task_by_id(contest_id, task_id, user_id):
    """
    Get user answer for task
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserAnswerSchema
        '403':
          description: Restriction error
        '404':
          description: User, contest or task not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_response)
    return user_answer_get(user_id, contest_id, task_id), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/plain/file', methods=['POST'])
def user_answer_for_task_by_id_post_plain_file(contest_id, task_id, user_id):
    """
    Add user answer for a task
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        content:
          image/png: {schema: {format: binary, type: string}}
          application/pdf: {schema: {format: binary, type: string}}
          image/jpeg: {schema: {format: binary, type: string}}
          image/gif: {schema: {format: binary, type: string}}
          text/plain: {schema: {format: binary, type: string}}
          application/msword: {schema: {format: binary, type: string}}
          application/zip: {schema: {format: binary, type: string}}
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error or file is too large
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    check_task_type(task_id, answer_dict['PlainAnswerFile'])
    user_answer_post_file(user_id, contest_id, task_id)
    return {}, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/<string:filetype>', methods=['POST'])
def user_answer_for_task_by_id_post_plain_file_old(contest_id, task_id, user_id, filetype):
    """
    Add user answer for a task
    ---
    post:
      deprecated: true
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
        - in: path
          description: Filetype
          name: filetype
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/octet-stream:
            schema:
              type: string
              format: binary
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error or file is too large
    """
    return user_answer_for_task_by_id_post_plain_file(contest_id, task_id, user_id)


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/plain', methods=['POST'],
              input_schema=PlainAnswerRequestSchema)
def user_answer_for_task_by_id_post_plain_text(contest_id, task_id, user_id):
    """
    Add user answer for a task
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema: PlainAnswerRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    check_task_type(task_id, answer_dict['PlainAnswerText'])
    values = request.marshmallow
    user_answer_post(user_id, contest_id, task_id, values, 'PlainAnswerText')
    return {}, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/range', methods=['POST'],
              input_schema=RangeAnswerRequestSchema)
def user_answer_for_task_by_id_range(contest_id, task_id, user_id):
    """
    Add user answer for a task
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema: RangeAnswerRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    check_task_type(task_id, answer_dict['RangeAnswer'])
    values = request.marshmallow
    user_answer_post(user_id, contest_id, task_id, values, 'RangeAnswer')
    return {}, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/multiple', methods=['POST'],
              input_schema=MultipleAnswerRequestSchema)
def user_answer_for_task_by_id_multiple(contest_id, task_id, user_id):
    """
    Add user answer for a task
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema: MultipleAnswerRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error or wrong answers
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    check_task_type(task_id, answer_dict['MultipleChoiceAnswer'])
    values = request.marshmallow
    check_user_multiple_answers(values['answers'], task_id)
    user_answer_post(user_id, contest_id, task_id, values, 'MultipleChoiceAnswer')
    return {}, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status', methods=['POST'],
              input_schema=UserResponseStatusResponseSchema)
def user_status_for_response_by_id_post(contest_id, user_id):
    """
    Set user's status for response, only for inspector
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UserResponseStatusResponseSchema
      responses:
        '200':
          description: OK
        '400':
          description: Incorrect mark or status
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    values = request.marshmallow
    user_work = get_user_in_contest_work(user_id, contest_id)
    user_work.work_status = values['status']
    db.session.commit()
    return {}, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status', methods=['GET'],
              output_schema=UserResponseStatusResponseSchema)
def user_status_for_response_by_id(contest_id, user_id):
    """
    Get user's status for response, only for inspector
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserResponseStatusResponseSchema
        '400':
          description: Incorrect mark or status
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_mark_and_user_status)
    user_work = get_user_in_contest_work(user_id, contest_id)
    return user_work, 200


@module.route('/contest/<int:contest_id>/list', methods=['GET'],
              output_schema=ContestResultSheetResponseSchema)
def get_list_for_stage(contest_id):
    """
    Get the consolidated sheets within a single competition or stage
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ContestResultSheetResponseSchema
        '403':
          description: Restriction error
        '404':
          description: Contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_mark_and_user_status)
    users_in_contest = db_get_list(Response, 'contest_id', contest_id)
    return {
               'contest_id': contest_id,
               'user_row': users_in_contest
           }, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/mark', methods=['POST'],
              input_schema=UserAnswerMarkResponseSchema)
def user_answer_task_mark_post(contest_id, user_id, task_id):
    """
    Add mark for user's response
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UserAnswerMarkResponseSchema
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
        '409':
          description: Mark or timing error
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_mark)
    check_timing_for_mark_editing_and_appeal(contest_id, jwt_get_role())
    values = request.marshmallow
    user_work = get_user_in_contest_work(user_id, contest_id)
    answer = get_answer_by_task_id_and_work_id(BaseAnswer, task_id, user_work.work_id)
    if answer is None:
        raise NotFound('task_id for user_id', f'{task_id, user_id}')
    check_mark_for_task(values['mark'], answer)
    answer.mark = values['mark']
    db.session.commit()
    return {}, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/mark', methods=['GET'],
              output_schema=UserAnswerMarkResponseSchema)
def user_answer_task_mark(contest_id, user_id, task_id):
    """
    Get mark for user's response
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the task
          name: task_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserAnswerMarkResponseSchema
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_mark_and_user_status)
    user_work = get_user_in_contest_work(user_id, contest_id)
    answer = get_answer_by_task_id_and_work_id(BaseAnswer, task_id, user_work.work_id)
    if answer is None:
        raise NotFound('task_id for user_id', f'{task_id, user_id}')
    return answer, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/time', methods=['GET'],
              output_schema=UserTimeResponseRequestSchema)
def user_by_id_time_left(contest_id, user_id):
    """
    Get time left for user's contest
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserTimeResponseRequestSchema
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_response)
    user_work = get_user_in_contest_work(user_id, contest_id)
    return {
        "time": calculate_time_left(user_work)
           }, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/time/extra', methods=['GET'],
              output_schema=UserTimeResponseRequestSchema)
def get_user_by_id_extra_time(contest_id, user_id):
    """
    Get extended time for user
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserTimeResponseRequestSchema
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.view_response)
    user_work = get_user_in_contest_work(user_id, contest_id)
    return {
        "time": user_work.time_extension
           }, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/time/extra', methods=['POST'],
              input_schema=UserTimeResponseRequestSchema)
def user_by_id_extra_time(contest_id, user_id):
    """
    Extend contest duration for user
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: UserTimeResponseRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    values = request.marshmallow
    user_work: Response = get_user_in_contest_work(user_id, contest_id)
    user_work.time_extension = values['time']
    db.session.commit()
    return {}, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/finish', methods=['POST'])
def user_by_id_finish_contest(contest_id, user_id):
    """
    Finish user's contest
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: User or contest not found
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    user_work = get_user_in_contest_work(user_id, contest_id)
    finish_contest(user_work)
    return {}, 200


@module.route('/contest/<int:contest_id>/check', methods=['POST'])
def auto_check_users_answers(contest_id):
    """
    Auto check all users' responses for contest
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: Contest not found
        '409':
          description: Olympiad error
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_mark)
    is_contest_over(contest_id)
    users_in_contest = db_get_list(Response, 'contest_id', contest_id)
    for user_work in users_in_contest:
        if user_work.status == ResponseStatusEnum.in_progress or user_work.status == ResponseStatusEnum.not_checked:
            check_user_work(user_work)
    return {}, 200


@module.route('/contest/<int:contest_id>/winning', methods=['POST'])
def set_status_by_result(contest_id):
    """
    Set new statuses to user in contest
    ---
    post:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      parameters:
        - in: path
          description: Id of the contest
          name: contest_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '403':
          description: Restriction error
        '404':
          description: Contest not found
        '409':
          description: Olympiad error
    """
    creator_id = jwt_get_id()
    check_contest_restriction(creator_id, contest_id, ContestGroupRestrictionEnum.edit_user_status)
    is_contest_over(contest_id)
    is_all_checked(contest_id)
    set_user_statuses(contest_id)
    return {}, 200


@module.route('/contest/user/<int:user_id>/results', methods=['GET'],
              output_schema=AllUserResultsResponseSchema)
def all_user_results(user_id):
    """
    Get all user results for all contests
    ---
    get:
      security:
        - JWTAccessToken: []
      parameters:
        - in: path
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllUserResultsResponseSchema
        '404':
          description: User not found
    """
    return get_all_user_responses(user_id), 200
