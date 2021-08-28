import io
from flask import request, send_file
from common import get_current_app, get_current_module
from common.util import db_get_or_raise, db_get_list
from contest.responses.util import *
from contest.responses.model_schemas.schemas import AnswerSchema
from .schemas import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/user/<int:user_id>/response', methods=['GET'],
              output_schema=AllUserAnswersResponseSchema)
def get_user_all_answers(contest_id, user_id):
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
          description: Not enough rights for current user
        '404':
          description: User or contest not found
    """
    return get_all_user_answers(user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/plain/file', methods=['GET'])
def user_answer_for_task_by_id_plain_file(contest_id, task_id, user_id):
    """
    Get user answer file for plain task
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
        - in: path
          description: Id of the user
          name: user_id
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
    user_answer = user_answer_get_file(user_id, contest_id, task_id)
    return send_file(io.BytesIO(user_answer.answer_file),
                     attachment_filename=f'userid_{user_id}_taskid_{task_id}.{user_answer.filetype.value}',
                     mimetype=get_mimetype(user_answer.filetype.value)), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>', methods=['GET'],
              output_schema=AnswerSchema)
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
              schema: AnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    return user_answer_get(user_id, contest_id, task_id), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/<string:filetype>', methods=['POST'])
def user_answer_for_task_by_id_post_plain_file(contest_id, task_id, user_id, filetype):
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
    check_task_type(task_id, answer_dict['PlainAnswer'])
    user_answer_post_file(request.data, filetype, user_id, contest_id, task_id)
    return {}, 200


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
    check_task_type(task_id, answer_dict['PlainAnswer'])
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
    check_task_type(task_id, answer_dict['MultipleChoiceAnswer'])
    values = request.marshmallow
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
          description: Invalid role of current user
        '404':
          description: User or contest not found
    """
    values = request.marshmallow
    user_work = get_user_in_contest_work(user_id, contest_id)
    user_work.status = values['status']
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
        '404':
          description: Contest not found
    """
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
          content:
            application/json:
              schema: UserAnswerMarkResponseSchema
        '404':
          description: User or contest not found
    """
    values = request.marshmallow
    user_work = get_user_in_contest_work(user_id, contest_id)
    answer = db_get_or_raise(BaseAnswer, 'task_id', task_id)
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
        '404':
          description: User or contest not found
    """
    get_user_in_contest_work(user_id, contest_id)
    answer = db_get_or_raise(BaseAnswer, 'task_id', task_id)
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
          content:
            application/json:
              schema: UserTimeResponseRequestSchema
        '404':
          description: User or contest not found
    """
    user_work = get_user_in_contest_work(user_id, contest_id)
    return calculate_time_left(user_work), 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/time', methods=['POST'],
              input_schema=UserTimeResponseRequestSchema)
def user_by_id_extend_time(contest_id, user_id):
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
        '404':
          description: User or contest not found
    """
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
          description: Id of the user
          name: user_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
        '404':
          description: User or contest not found
    """
    user_work = get_user_in_contest_work(user_id, contest_id)
    finish_contest(user_work)
    return {}, 200


@module.route('/contest/<int:contest_id>/check', methods=['POST'])
def auto_check_users_answers(contest_id):
    """
    Auto check all users' responses for contest
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
        '404':
          description: Contest not found
        '409':
          description: Contest is not over
    """
    is_contest_over(contest_id)
    users_in_contest = db_get_list(Response, 'contest_id', contest_id)
    for user_work in users_in_contest:
        if user_work.status == work_status['InProgress'] or user_work.status == work_status['NotChecked']:
            check_user_work(user_work)
    return {}, 200
