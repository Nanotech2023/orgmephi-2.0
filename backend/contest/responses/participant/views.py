import io
from flask import request, send_file
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_get_id
from common.util import db_get_or_raise
from contest.responses.model_schemas.schemas import PlainAnswerSchema, RangeAnswerSchema, MultipleChoiceAnswerSchema
from contest.responses.util import *
from contest.responses.creator.schemas import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


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
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    if user_work.answers is None:
        raise NotFound('user_response.answers', 'for user %d' % self_user_id)
    answers = user_work.answers
    return {
               "user_id": user_work.user_id,
               "work_id": user_work.work_id,
               "contest_id": user_work.contest_id,
               "user_answers": answers
           }, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/plain/file', methods=['GET'])
def get_self_user_answer_for_task_plain_file(contest_id, task_id):
    """
    Get current user answer file for plain task
    ---
    get:
      security:
        - JWTAccessToken: []
      produces:
        - image/png
        - application/pdf
        - image/jpeg
        - image/gif
        - text/plain
        - application/msword
        - application/vnd.openxmlformats-officedocument.wordprocessingml.document
        - application/vnd.oasis.opendocument.text
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
          schema:
            type: string
            format: binary
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    user_answer = user_answer_get_file(self_user_id, contest_id, task_id)
    return send_file(io.BytesIO(user_answer.answer_file),
                     attachment_filename=f'userid_{self_user_id}_taskid_{task_id}.{user_answer.filetype.value}',
                     mimetype=get_mimetype(user_answer.filetype.value)), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/plain', methods=['GET'],
              output_schema=PlainAnswerSchema)
def self_user_answer_for_task_plain_text(contest_id, task_id):
    """
    Get current user answer text for plain task
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
              schema: PlainAnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    user_answer = user_answer_get(self_user_id, contest_id, task_id, PlainAnswer)
    return user_answer


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/range', methods=['GET'],
              output_schema=RangeAnswerSchema)
def self_user_answer_for_task_range(contest_id, task_id):
    """
    Get current user answer for range task
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
              schema: RangeAnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    user_answer = user_answer_get(self_user_id, contest_id, task_id, RangeAnswer)
    return user_answer


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/multiple', methods=['GET'],
              output_schema=MultipleChoiceAnswerSchema)
def self_user_answer_for_task_multiple(contest_id, task_id):
    """
    Get current user answer for multiple choice task
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
              schema: MultipleChoiceAnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    user_answer = user_answer_get(self_user_id, contest_id, task_id, MultipleUserAnswer)
    return user_answer


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
          description: Olympiad is over
    """
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
          description: OK
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
          description: Olympiad is over
    """
    values = request.marshmallow
    self_user_id = jwt_get_id()
    user_answer_post_plain_text(self_user_id, contest_id, task_id, values)
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
          description: OK
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
          description: Olympiad is over
    """
    values = request.marshmallow
    self_user_id = jwt_get_id()
    user_answer_post_range(self_user_id, contest_id, task_id, values)
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
          description: OK
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
          description: Olympiad is over
    """
    values = request.marshmallow
    self_user_id = jwt_get_id()
    user_answer_post_multiple(self_user_id, contest_id, task_id, values)
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
      requestBody:
        required: true
        content:
          application/json:
            schema: UserAnswerMarkResponseSchema
      responses:
        '200':
          description: OK
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    answer = db_get_or_raise(BaseAnswer, 'task_id', task_id)
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
    return calculate_time_left(user_work), 200

# TODO Проверка всех ответов (автоматических)
# TODO Закончить олимпиаду
# TODO ограничения по размеру файлов
