import io
from flask import request, send_file

from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_or_raise
from common.errors import NotFound, DataConflict

from news.util import FilterNewsResponseSchema, filter_news_query
from news.model_schemas import NewsSchema
from news.models import News

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/news', methods=['GET'], output_schema=FilterNewsResponseSchema)
def filter_news():
    """
    List news
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
          name: category_name
          required: false
          schema:
            type: string
        - in: query
          name: grade
          required: false
          schema:
            type: integer
        - in: query
          name: title
          required: false
          schema:
            type: string
        - in: query
          name: contest_id
          required: false
          schema:
            type: integer
        - in: query
          name: only_count
          required: false
          schema:
            type: boolean
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FilterNewsResponseSchema
    """
    return filter_news_query(request.args, True)


@module.route('/news/<int:news_id>', methods=['GET'], output_schema=NewsSchema)
def get_news(news_id):
    """
    Get news
    ---
    get:
      parameters:
        - in: path
          description: ID of news
          name: news_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: NewsSchema
        '404':
          description: News not found
    """
    news = db_get_or_raise(News, 'id', news_id)
    if not news.posted:
        raise NotFound('id', news_id)
    return news, 200


@module.route('/news/<int:news_id>/image', methods=['GET'])
def get_image(news_id):
    """
    Get news
    ---
    get:
      parameters:
        - in: path
          description: ID of news
          name: news_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: OK
          content:
            image/*:
              schema:
                type: string
                format: binary
        '404':
          description: News not found
    """
    news = db_get_or_raise(News, 'id', news_id)
    if not news.posted:
        raise NotFound('id', news_id)
    if news.image is None:
        raise DataConflict('Image not present')
    return send_file(io.BytesIO(news.image), mimetype='image/*')
