from flask import request

from common.errors import DataConflict
from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise
from common.jwt_verify import jwt_get_id

from .schemas import CreateMessageCreatorMessagesRequestSchema, ThreadStatusMessagesRequestSchema, \
    FilterThreadsMessagesResponseSchema, FilterThreadsMessagesRequestSchema
from messages.model_schemas import ThreadSchema, MessageSchema
from messages.models import ThreadType, ThreadStatus, Thread, Message

from user.models import User

db = get_current_db()
module = get_current_module()
app = get_current_app()


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
    return db_get_or_raise(Thread, 'id', thread_id), 200


@module.route('/message/<int:thread_id>', methods=['POST'], input_schema=CreateMessageCreatorMessagesRequestSchema,
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
            schema: CreateMessageCreatorMessagesRequestSchema
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
    """
    values = request.marshmallow
    author = db_get_or_raise(User, 'id', jwt_get_id())
    thread = db_get_or_raise(Thread, 'id', thread_id)

    msg = Message(message=values['message'])
    msg.employee = author
    thread.messages.append(msg)
    db.session.commit()
    return msg, 200


@module.route('/thread_status/<int:thread_id>', methods=['POST'], input_schema=ThreadStatusMessagesRequestSchema,
              output_schema=ThreadSchema)
def update_thread_status(thread_id):
    """
    Change thread status
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
            schema: ThreadStatusMessagesRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ThreadSchema
        '404':
          description: Thread not found
    """
    thread = db_get_or_raise(Thread, 'id', thread_id)
    status = request.marshmallow['status']
    if thread.thread_type == ThreadType.appeal and status == ThreadStatus.closed:
        raise DataConflict('Appeal must be either rejected or accepted')
    thread.status = status
    thread.resolved = status != ThreadStatus.open
    db.session.commit()
    return thread, 200


@module.route('/filter_threads', methods=['GET'], output_schema=FilterThreadsMessagesResponseSchema)
def filter_threads():
    """
    Get threads based on a filter
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
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ThreadSchema
    """
    marshmallow = FilterThreadsMessagesRequestSchema().load(request.args)

    filters = {v: marshmallow[v] for v in ['resolved', 'answered', 'thread_type', 'category_name'] if v in marshmallow}

    query = Thread.query.filter_by(**filters)

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)
    if offset is not None:
        query = query.order_by(Thread.update_time)
    if limit is not None:
        query = query.offset(offset).limit(limit)
    if marshmallow.get('only_count', False):
        return {'count': query.count()}, 200
    else:
        return {'threads': query.all(), 'count': query.count()}, 200
