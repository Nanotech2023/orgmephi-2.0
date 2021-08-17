from flask import request, make_response
from contest.responses.models import *
from common import get_current_app, get_current_module
from common.jwt_verify import jwt_required, jwt_required_role, jwt_get_id
from common.util import db_get_list, db_get_or_raise
from contest.responses.util import *
from contest.responses.model_schemas.schemas import ResponseAnswerSchema, ResponseStatusSchema, AppealSchema
from contest.responses.creator.schemas import UserResponseHistorySchema, AppealMessageSchema, AppealCreateInfoSchema

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self', methods=['GET'],
              output_schema=ResponseAnswerSchema)
def user_answer_for_task(contest_id, task_id):
    """
    Get current user answer for the task
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
              schema: ResponseAnswerSchema      #TODO return FILE
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    user_answer = user_answer_get(self_user_id, contest_id, task_id)
    return user_answer, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/self/<string:filetype>', methods=['POST'])
def user_answer_for_task_post(contest_id, task_id, filetype):
    """
    Add current user answer for the task
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
          description: Type of file
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
        '404':
          description: User, contest or task not found
    """
    self_user_id = jwt_get_id()
    user_answer_post(request.data, filetype, self_user_id, contest_id, task_id)
    return {}, 200


@module.route('/contest/<int:contest_id>/answer/<int:answer_id>', methods=['GET'],
              output_schema=ResponseAnswerSchema)
def get_user_answer_by_id(contest_id, answer_id):
    """
    Get user's answer by id
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
          description: Id of the answer
          name: answer_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ResponseAnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User or contest not found
   """
    user_answer = db_get_or_raise(ResponseAnswer, 'answer_id', answer_id)
    return  user_answer, 200    # TODO Test BLOB


@module.route('/contest/<int:contest_id>/user/self/status', methods=['GET'],
              output_schema=ResponseStatusSchema)
def user_status_and_mark_for_response(contest_id):
    """
    Get user's status and mark for response
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
              schema: ResponseStatusSchema
        '403':
          description: Invalid role of current user
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    return user_answer_status_get(self_user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/user/self/status/history', methods=['GET'],
              output_schema=UserResponseHistorySchema)
def user_status_history_for_response(contest_id):
    """
    Get status history of current user's work
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
              schema: UserResponseHistorySchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    user_work = get_user_in_contest_work(self_user_id, contest_id)
    status = user_work.statuses
    return {
            'user_id': self_user_id,
            'contest_id': contest_id,
            'history': status
            }, 200


@module.route('/contest/<int:contest_id>/user/self/appeal', methods=['POST'],
              input_schema=AppealMessageSchema, output_schema=AppealCreateInfoSchema)
def user_response_appeal(contest_id):
    """
    Create appeal for current user's response
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
      requestBody:
        required: true
        content:
          application/json:
            schema: AppealMessageSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AppealCreateInfoSchema
        '404':
          description: User or contest not found
    """
    self_user_id = jwt_get_id()
    values = request.marshmallow
    return user_response_appeal_create(values, self_user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/appeal/<int:appeal_id>', methods=['GET'],
              output_schema=AppealSchema)
def get_appeal_info_by_id(contest_id, appeal_id):
    """
    Get appeal info
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
          description: Id of the appeal
          name: appeal_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AppealSchema
        '404':
          description: Appeal or contest not found
    """
    appeal = db_get_or_raise(Appeal, 'appeal_id', appeal_id)
    return appeal, 200
