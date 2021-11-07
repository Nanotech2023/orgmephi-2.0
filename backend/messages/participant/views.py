from datetime import date, datetime

from flask import request
from marshmallow import EXCLUDE

from common.errors import QuotaExceeded, NotFound, DataConflict
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise, db_get_all
from common.jwt_verify import jwt_get_id

from .schemas import ListCategoriesMessagesResponseSchema, CreateThreadMessagesRequestSchema, \
    CreateMessageMessagesRequestSchema
from messages.model_schemas import ThreadSchema, MessageSchema
from messages.models import ThreadCategory, Thread, Message
from messages.util import filter_threads_query, FilterThreadsMessagesResponseSchema

from user.models import User

db = get_current_db()
module = get_current_module()
app = get_current_app()


thread_limit = app.config['ORGMEPHI_DAILY_THREAD_LIMIT']
message_limit = app.config['ORGMEPHI_DAILY_MESSAGE_LIMIT']


@module.route('/categories', methods=['GET'], output_schema=ListCategoriesMessagesResponseSchema)
def list_categories():
    """
    List available thread categories
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ListCategoriesMessagesResponseSchema
    """
    return {'categories': db_get_all(ThreadCategory)}, 200


@module.route('/threads', methods=['GET'], output_schema=FilterThreadsMessagesResponseSchema)
def filter_threads():
    """
    List threads that belong to the user
    ---
    get:
      parameters:
        - in: query
          name: offset
          required: false
          schema:
            type: integer
        - in: query
          name: limit
          required: false
          schema:
            type: integer
        - in: query
          name: resolved
          required: false
          schema:
            type: boolean
        - in: query
          name: answered
          required: false
          schema:
            type: boolean
        - in: query
          name: thread_type
          required: false
          schema:
            type: string
            enum: ['Appeal', 'Work', 'Contest', 'General']
        - in: query
          name: category_name
          required: false
          schema:
            type: string
        - in: query
          name: only_count
          required: false
          schema:
            type: boolean
        - in: query
          name: contest_id
          required: false
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FilterThreadsMessagesResponseSchema
    """
    return filter_threads_query(request.args, jwt_get_id())


@module.route('/thread', methods=['POST'], input_schema=CreateThreadMessagesRequestSchema,
              output_schema=ThreadSchema)
def create_thread():
    """
    List threads that belong to the user
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateThreadMessagesRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ThreadSchema
        '409':
          description: Exceeded daily thread threshold
    """
    values = request.marshmallow
    author = db_get_or_raise(User, 'id', jwt_get_id())
    if thread_limit is not None:
        cnt = Thread.query.filter(Thread.author_id == author.id, Thread.post_time >= datetime.utcnow().date()).count()
        if cnt >= thread_limit:
            raise QuotaExceeded('New threads per day', thread_limit)

    thread = ThreadSchema(load_instance=True).load(request.json, unknown=EXCLUDE)

    thread.author = author
    thread.messages.append(Message(message=values['message']))

    db.session.add(thread)
    db.session.commit()
    return thread, 200


@module.route('/thread/<int:thread_id>', methods=['GET'], output_schema=ThreadSchema)
def get_thread(thread_id):
    """
    Get a message thread
    ---
    get:
      parameters:
        - in: path
          description: ID of the thread
          name: thread_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ThreadSchema
        '404':
          description: Thread not found
    """
    author = db_get_or_raise(User, 'id', jwt_get_id())
    thread = db_get_or_raise(Thread, 'id', thread_id)
    if thread.author != author:
        raise NotFound('id', str(thread_id))
    return thread, 200


@module.route('/message/<int:thread_id>', methods=['POST'], input_schema=CreateMessageMessagesRequestSchema,
              output_schema=MessageSchema)
def add_message(thread_id):
    """
    Add a message to a thread
    ---
    post:
      parameters:
        - in: path
          description: ID of the thread
          name: thread_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateMessageMessagesRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: MessageSchema
        '404':
          description: Thread not found
        '409':
          description: Exceeded daily message threshold
    """
    values = request.marshmallow
    author = db_get_or_raise(User, 'id', jwt_get_id())
    thread = db_get_or_raise(Thread, 'id', thread_id)
    if thread.author != author:
        raise NotFound('id', str(thread_id))

    if thread.resolved:
        raise DataConflict('Cant post to resolved thread')

    if message_limit is not None:
        # noinspection PyComparisonWithNone
        cnt = Message.query.filter(Message.thread_id == thread_id, Message.post_time >= datetime.utcnow().date(),
                                   Message.employee_id == None).count()
        if cnt >= message_limit:
            raise QuotaExceeded('New messages per day per thread', message_limit)

    msg = Message(message=values['message'])
    thread.messages.append(msg)
    db.session.commit()
    return msg, 200
