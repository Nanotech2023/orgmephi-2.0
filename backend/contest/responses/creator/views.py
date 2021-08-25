import io
from flask import request, send_file
from common import get_current_app, get_current_module
from common.util import db_get_or_raise, db_get_list
from contest.responses.util import *
from contest.responses.model_schemas.schemas import PlainAnswerSchema, RangeAnswerSchema, MultipleChoiceAnswerSchema
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


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/plain', methods=['GET'],
              output_schema=PlainAnswerSchema)
def user_answer_for_task_by_id_plain_text(contest_id, task_id, user_id):
    """
    Get user answer text for plain task
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
              schema: PlainAnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    user_answer = user_answer_get(user_id, contest_id, task_id, PlainAnswer)
    return user_answer


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/range', methods=['GET'],
              output_schema=RangeAnswerSchema)
def user_answer_for_task_by_id_range(contest_id, task_id, user_id):
    """
    Get user answer for range task
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
              schema: RangeAnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    user_answer = user_answer_get(user_id, contest_id, task_id, RangeAnswer)
    return user_answer


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/multiple', methods=['GET'],
              output_schema=MultipleChoiceAnswerSchema)
def user_answer_for_task_by_id_multiple(contest_id, task_id, user_id):
    """
    Get user answer for multiple choice task
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
              schema: MultipleChoiceAnswerSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    user_answer = user_answer_get(user_id, contest_id, task_id, MultipleUserAnswer)
    return user_answer


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/<string:filetype>', methods=['POST'],
              output_schema=UserAnswerPostResponseSchema)
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
          content:
            application/json:
              schema: UserAnswerPostResponseSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
        ''
    """
    message = user_answer_post_file(request.data, filetype, user_id, contest_id, task_id)
    return message, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/plain', methods=['POST'],
              input_schema=PlainAnswerRequestSchema, output_schema=UserAnswerPostResponseSchema)
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
        - in: path
          description: Filetype
          name: filetype
          required: true
          schema:
            type: string
      requestBody:
        content:
          description: OK
          content:
            application/json:
              schema: PlainAnswerRequestSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserAnswerPostResponseSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    values = request.marshmallow
    user_work: Response = get_user_in_contest_work(user_id, contest_id)
    flag, message = check_contest_duration(user_work)
    if flag:
        finish_contest(user_work)
        return message, 200
    user_work.finish_time = datetime.utcnow()
    answer = db_get_one_or_none(PlainAnswer, 'task_id', task_id)
    if answer is None:
        add_plain_answer(user_work.work_id, task_id, text=values['answer_text'])
    else:
        PlainAnswerSchema(load_instance=True).load(values, session=db.session, instance=answer)
    db.session.commit()
    return message, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/range', methods=['POST'],
              input_schema=RangeAnswerRequestSchema, output_schema=UserAnswerPostResponseSchema)
def user_answer_for_task_by_id_range_text(contest_id, task_id, user_id):
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
          description: OK
          content:
            application/json:
              schema: RangeAnswerRequestSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserAnswerPostResponseSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    values = request.marshmallow
    user_work: Response = get_user_in_contest_work(user_id, contest_id)
    flag, message = check_contest_duration(user_work)
    if flag:
        finish_contest(user_work)
        return message, 200
    user_work.finish_time = datetime.utcnow()
    answer = db_get_one_or_none(RangeAnswer, 'task_id', task_id)
    if answer is None:
        add_range_answer(user_work.work_id, task_id, values['answer'])
    else:
        RangeAnswerSchema(load_instance=True).load(values, session=db.session, instance=answer)
    db.session.commit()
    return message, 200


@module.route('/contest/<int:contest_id>/task/<int:task_id>/user/<int:user_id>/multiple', methods=['POST'],
              input_schema=MultipleAnswerRequestSchema, output_schema=UserAnswerPostResponseSchema)
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
        - in: path
          description: Filetype
          name: filetype
          required: true
          schema:
            type: string
      requestBody:
        content:
          description: OK
          content:
            application/json:
              schema: MultipleAnswerRequestSchema
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: UserAnswerPostResponseSchema
        '403':
          description: Not enough rights for current user
        '404':
          description: User, contest or task not found
    """
    values = request.marshmallow
    user_work: Response = get_user_in_contest_work(user_id, contest_id)
    flag, message = check_contest_duration(user_work)
    if flag:
        finish_contest(user_work)
        return message, 200
    user_work.finish_time = datetime.utcnow()
    answer = db_get_one_or_none(MultipleChoiceAnswer, 'task_id', task_id)
    if answer is None:
        add_range_answer(user_work.work_id, task_id, values['answers'])
    else:
        update_multiple_answers(values['answers'], answer)
    db.session.commit()
    return message, 200


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
    user_work = get_user_in_contest_work(user_id, contest_id)
    answer = db_get_or_raise(BaseAnswer, 'task_id', task_id)
    return answer, 200
