import io

from flask import request, send_file
from common import get_current_app, get_current_module
from common.util import db_get_or_raise, db_get_list, db_get_one_or_none
from contest.responses.util import *
from contest.responses.model_schemas.schemas import ResponseStatusSchema, AppealSchema
from .schemas import *

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>', methods=['GET'])
def user_answer_for_task_by_id(contest_id, task_id, user_id):
    """
    Get user answer for the task
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
    user_answer = user_answer_get(user_id, contest_id, task_id)
    return send_file(io.BytesIO(user_answer.answer),
                     attachment_filename=f'userid_{user_id}_taskid_{task_id}.{user_answer.filetype.value}',
                     mimetype=get_mimetype(user_answer.filetype.value)), 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/<string:filetype>', methods=['POST'])
def user_answer_for_task_by_id_post(contest_id, task_id, user_id, filetype):
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
    """
    user_answer_post(request.data, filetype, user_id, contest_id, task_id)
    return {}, 200


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
    user_work = get_user_in_contest_work(user_id, contest_id)
    if user_work.answers is None:
        raise NotFound('user_response.answers', 'for user %d' % user_id)
    answers = user_work.answers
    return {
               "user_id": user_work.user_id,
               "work_id": user_work.work_id,
               "contest_id": user_work.contest_id,
               "user_answers": answers
           }, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status', methods=['GET'],
              output_schema=ResponseStatusSchema)
def user_status_and_mark_for_response_by_id(contest_id, user_id):
    """
    Get user's status and mark for response
    ---
    get:
      summary:
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
              schema: ResponseStatusSchema
        '403':
          description: Invalid role of current user
        '404':
          description: User or contest not found
    """
    return user_answer_status_get(user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status', methods=['POST'],
              input_schema=UserResponseStatusMarkResponseSchema)
def user_status_and_mark_for_response_by_id_post(contest_id, user_id):
    """
    Set user's status and mark for response, only for inspector
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
            schema: UserResponseStatusMarkResponseSchema
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
    user_answer_status_post(values, user_id, contest_id)
    return {}, 200


@module.route('/contest/<int:contest_id>/user/<int:user_id>/status/history', methods=['GET'],
              output_schema=UserResponseStatusHistoryResponseSchema)
def user_status_history_for_response_by_id(contest_id, user_id):
    """
    Get status history of user's work
    ---
    get:
      summary:
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
              schema: UserResponseStatusHistoryResponseSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User or contest not found
    """
    user_work = get_user_in_contest_work(user_id, contest_id)
    status = user_work.statuses
    return {
               'user_id': user_id,
               'contest_id': contest_id,
               'history': status
           }, 200


@module.route('/contest/<int:contest_id>/list/', methods=['GET'],
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


@module.route('/contest/<int:contest_id>/user/<int:user_id>/appeal', methods=['POST'],
              input_schema=AppealMessageRequestSchema, output_schema=AppealCreateInfoResponseSchema)
def user_response_appeal_by_id(contest_id, user_id):
    """
    Create appeal for user's response
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
            schema: AppealMessageRequestSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AppealCreateInfoResponseSchema
        '404':
          description: User or contest not found
    """
    values = request.marshmallow
    return user_response_appeal_create(values, user_id, contest_id), 200


@module.route('/contest/<int:contest_id>/appeal/<int:appeal_id>/reply', methods=['POST'],
              input_schema=AppealReplyRequestSchema, output_schema=AppealSchema)
def reply_to_user_appeal(contest_id, appeal_id):
    """
    Reply appeal for the user's response
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
          description: Id of the appeal
          name: appeal_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: AppealReplyRequestSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: AppealSchema
        '404':
          description: User or contest not found
    """
    values = request.marshmallow
    message = values['message']
    accepted = values['accepted']
    if accepted:
        appeal_new_status = appeal_status['AppealAccepted']
        response_new_status = 'Accepted'
    else:
        appeal_new_status = appeal_status['AppealRejected']
        response_new_status = 'Rejected'
    appeal = db_get_or_raise(Appeal, 'appeal_id', appeal_id)
    appeal.reply_to_appeal(message, appeal_new_status)
    db.session.commit()
    last_status = db_get_one_or_none(ResponseStatus, 'status_id', appeal.work_status)
    if 'mark' in values and accepted:
        new_mark = values['mark']
    else:
        new_mark = last_status.mark
    new_response_status = add_response_status(last_status.work_id, status=response_new_status,
                                              mark=new_mark)
    db.session.add(new_response_status)
    db.session.commit()
    return appeal, 200
