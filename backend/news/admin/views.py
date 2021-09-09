from flask import request

from common import get_current_app, get_current_module, get_current_db
from common.util import db_exists, db_get_or_raise
from common.errors import AlreadyExists

from .schemas import AddCategoryNewsRequestSchema
from news.models import NewsCategory, News
from news.model_schemas import NewsCategorySchema

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/add_category', input_schema=AddCategoryNewsRequestSchema, methods=['POST'],
              output_schema=NewsCategorySchema)
def add_category():
    """
    Add a news category
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: AddCategoryNewsRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: NewsCategorySchema
        '409':
          description: Category with this name already exists
    """
    values = request.marshmallow
    name = values['name']
    if db_exists(db.session, NewsCategory, 'name', name):
        raise AlreadyExists('NewsCategory.name', name)
    category = NewsCategory(name=name)
    db.session.add(category)
    db.session.commit()
    return category, 200


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
    category = db_get_or_raise(NewsCategory, 'name', category_name)
    db.session.delete(category)
    db.session.commit()
    return {}, 204


@module.route('/news/<int:news_id>/delete', methods=['POST'])
def delete_news(news_id):
    """
    Delete news
    ---
    post:
      parameters:
        - in: path
          description: ID of news
          name: news_id
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
          description: News not found
    """
    news = db_get_or_raise(News, 'id', news_id)
    db.session.delete(news)
    db.session.commit()
    return {}, 204
