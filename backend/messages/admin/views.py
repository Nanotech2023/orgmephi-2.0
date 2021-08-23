from flask import request

from common.errors import AlreadyExists
from common import get_current_app, get_current_module, get_current_db
from common.util import db_exists, db_get_or_raise

from .schemas import AddCategoryMessagesRequestSchema, CleanupMessagesRequestSchema
from messages.models import ThreadCategory, Thread

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/add_category', input_schema=AddCategoryMessagesRequestSchema, methods=['POST'])
def add_category():
    """
    Add a message thread category
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: AddCategoryMessagesRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '409':
          description: Category with this name already exists
    """
    values = request.marshmallow
    name = values['name']
    if db_exists(db.session, ThreadCategory, 'name', name):
        raise AlreadyExists('ThreadCategory.name', name)
    category = ThreadCategory(name=name)
    db.session.add(category)
    db.session.commit()
    return {}, 204


@module.route('/delete_category/<string:category_name>', methods=['POST'])
def delete_category(category_name):
    """
    Delete a message thread category
    ---
    post:
      parameters:
        - in: path
          description: Name of the category
          name: category_name
          required: true
          schema:
            type: string
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '404':
          description: Category not found
    """
    category = db_get_or_raise(ThreadCategory, 'name', category_name)
    db.session.delete(category)
    db.session.commit()
    return {}, 204


@module.route('/delete_thread/<int:thread_id>', methods=['POST'])
def delete_thread(thread_id):
    """
    Delete a message thread
    ---
    post:
      parameters:
        - in: path
          description: ID of the thread
          name: thread_id
          required: true
          schema:
            type: integer
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
        '404':
          description: Category not found
    """
    thread = db_get_or_raise(Thread, 'id', thread_id)
    db.session.delete(thread)
    db.session.commit()
    return {}, 204


@module.route('/cleanup', input_schema=CleanupMessagesRequestSchema, methods=['POST'])
def cleanup_threads():
    """
    Cleanup old threads
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CleanupMessagesRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
    """
    values = request.marshmallow
    query = Thread.query
    amount = values['amount']
    if not values['delete_unresolved']:
        query = query.filter_by(resolved=True)
    query = query.order_by(Thread.post_time.asc()).limit(amount)
    # Can't .delete() after limit
    values = query.all()
    for val in values:
        db.session.delete(val)
    db.session.commit()
    return {}, 204
