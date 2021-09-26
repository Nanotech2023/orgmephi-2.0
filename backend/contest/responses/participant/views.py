import io
from flask import request, send_file
from common import get_current_module
from common.jwt_verify import jwt_get_id
from contest.responses.model_schemas.schemas import AnswerSchema
from contest.responses.util import *
from contest.responses.creator.schemas import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/user/self/create', methods=['POST'])
def create_user_self_response_for_contest(contest_id):
    """
    Create current user's response for contest
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
        '404':
          description: User or contest not found
        '409':
          description: Timing error
    """
    check_contest_type(contest_id)
    self_user_id = jwt_get_id()
    create_user_response(contest_id, self_user_id)
    return {}, 200


@module.route('/contest/<int:contest_id>/user/self/response', methods=['GET'],
              output_schema=AllUserAnswersResponseSchema)
def get_self_user_all_answers(contest_id):
    """
    Get all current user answers for the contest
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
              schema: AllUserAnswersResponseSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    return get_all_user_answers(self_user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/user/self/mark', methods=['GET'],
              output_schema=AllUserMarksResponseSchema)
def get_user_by_id_all_marks(contest_id):
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
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllUserMarksResponseSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User or contest not found
        '409':
          description: The results have not yet been published
    """
    self_user_id = jwt_get_id()
    check_user_show_results(contest_id, self_user_id)
    check_time_publishing(contest_id)
    return get_all_user_answers(self_user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/plain/file', methods=['GET'])
def get_self_user_answer_for_task_plain_file(contest_id, task_id):
    """
    Get current user answer file for plain task
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
            application/vnd.openxmlformats-officedocument.wordprocessingml.document: {schema: {format: binary, type: string}}
            application/vnd.oasis.opendocument.text: {schema: {format: binary, type: string}}
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    user_answer = user_answer_get(self_user_id, contest_id, task_id, 'PlainAnswerFile')
    return send_file(io.BytesIO(user_answer.answer_file),
                     attachment_filename=f'userid_{self_user_id}_taskid_{task_id}.{user_answer.filetype.value}',
                     mimetype=get_mimetype(user_answer.filetype.value)), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self', methods=['GET'],
              output_schema=AnswerSchema)
def user_answer_for_task_self(contest_id, task_id):
    """
    Get current user answer for task
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
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    return user_answer_get(self_user_id, contest_id, task_id), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/<string:filetype>', methods=['POST'])
def self_user_answer_for_task_post_plain_file(contest_id, task_id, filetype):
    """
    Add current user answer for a task
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
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error or file is too large
    """
    check_task_type(task_id, answer_dict['PlainAnswerFile'])
    self_user_id = jwt_get_id()
    user_answer_post_file(request.data, filetype, self_user_id, contest_id, task_id)
    return {}, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/plain', methods=['POST'],
              input_schema=PlainAnswerRequestSchema)
def self_user_answer_for_task_post_plain_text(contest_id, task_id):
    """
    Add current user answer for a task
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
      requestBody:
        content:
          application/json:
            schema: PlainAnswerRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error
    """
    check_task_type(task_id, answer_dict['PlainAnswerText'])
    values = request.marshmallow
    self_user_id = jwt_get_id()
    user_answer_post(self_user_id, contest_id, task_id, values, 'PlainAnswerText')
    return {}, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/range', methods=['POST'],
              input_schema=RangeAnswerRequestSchema)
def self_user_answer_for_task_range(contest_id, task_id):
    """
    Add current user answer for a task
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
      requestBody:
        content:
          application/json:
            schema: RangeAnswerRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error
    """
    check_task_type(task_id, answer_dict['RangeAnswer'])
    values = request.marshmallow
    self_user_id = jwt_get_id()
    user_answer_post(self_user_id, contest_id, task_id, values, 'RangeAnswer')
    return {}, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/multiple', methods=['POST'],
              input_schema=MultipleAnswerRequestSchema)
def self_user_answer_for_task_multiple(contest_id, task_id):
    """
    Add current user answer for a task
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
      requestBody:
        content:
          application/json:
            schema: MultipleAnswerRequestSchema
      responses:
        '200':
          description: OK
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
        '409':
          description: Timing error
    """
    check_task_type(task_id, answer_dict['MultipleChoiceAnswer'])
    values = request.marshmallow
    self_user_id = jwt_get_id()
    check_user_multiple_answers(values['answers'], task_id)
    user_answer_post(self_user_id, contest_id, task_id, values, 'MultipleChoiceAnswer')
    return {}, 200


@module.route('/contest/<int:contest_id>/user/self/status', methods=['GET'],
              output_schema=UserResponseStatusResponseSchema)
def self_user_status_for_response(contest_id):
    """
    Get current user's status for response
    ---
    get:
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
          content:
            application/json:
              schema: UserResponseStatusResponseSchema
        '400':
          description: Incorrect mark or status
        '403':
          description: Invalid role of current user
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    return user_work, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/mark', methods=['GET'],
              output_schema=UserAnswerMarkResponseSchema)
def self_user_answer_task_mark(contest_id, task_id):
    """
    Get mark for user's response
    ---
    get:
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
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserAnswerMarkResponseSchema
        '404':
          description: User or contest not found
        '409':
          description: The results have not yet been published
    """
    self_user_id = jwt_get_id()
    check_user_show_results(contest_id, self_user_id)
    check_time_publishing(contest_id)
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    answer = get_answer_by_task_id_and_work_id(BaseAnswer, task_id, user_work.work_id)
    if answer is None:
        raise NotFound('task_id for user_id', f'{task_id, self_user_id}')
    return answer, 200


@module.route('/contest/<int:contest_id>/user/self/time', methods=['GET'],
              output_schema=UserTimeResponseRequestSchema)
def self_user_time_left(contest_id):
    """
    Get time left for current user's contest
    ---
    get:
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
          content:
            application/json:
              schema: UserTimeResponseRequestSchema
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    return {
        "time": calculate_time_left(user_work)
           }, 200


@module.route('/contest/<int:contest_id>/user/self/finish', methods=['POST'])
def self_user_finish_contest(contest_id):
    """
    Finish current user's contest
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
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    finish_contest(user_work)
    return {}, 200


@module.route('/contest/user/self/results', methods=['GET'],
              output_schema=AllUserResultsResponseSchema)
def all_user_results():
    """
    Get all user results for all contests
    ---
    get:
      security:
        - JWTAccessToken: []
        - CSRFAccessToken: []
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AllUserResultsResponseSchema
        '404':
          description: User not found
    """
    self_user_id = jwt_get_id()
    return get_all_user_responses(self_user_id), 200
