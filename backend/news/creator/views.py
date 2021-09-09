import datetime
import io
from flask import request, send_file
from marshmallow import EXCLUDE

from common import get_current_app, get_current_module, get_current_db
from common.util import db_get_all, db_get_or_raise
from common.errors import InsufficientData, QuotaExceeded, DataConflict

from news.models import NewsCategory, News
from news.util import filter_news_query, FilterNewsResponseSchema
from news.model_schemas import NewsSchema

from .schemas import ListCategoriesNewsResponseSchema, CreateNewsRequestSchema, EditNewsRequestSchema

db = get_current_db()
module = get_current_module()
app = get_current_app()


@module.route('/categories', methods=['GET'], output_schema=ListCategoriesNewsResponseSchema)
def list_categories():
    """
    List available news categories
    ---
    get:
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: ListCategoriesNewsResponseSchema
    """
    return {'categories': db_get_all(NewsCategory)}, 200


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
          name: posted
          required: false
          schema:
            type: boolean
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

      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: FilterNewsResponseSchema
    """
    return filter_news_query(request.args, False)


@module.route('/news', methods=['POST'], input_schema=CreateNewsRequestSchema,
              output_schema=NewsSchema)
def create_news():
    """
    Create news
    ---
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema: CreateNewsRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: NewsSchema
    """
    news = NewsSchema(load_instance=True).load(request.json, unknown=EXCLUDE)
    db.session.add(news)
    db.session.commit()
    return news, 200


@module.route('/news/<int:news_id>', methods=['PATCH'], input_schema=EditNewsRequestSchema,
              output_schema=NewsSchema)
def edit_news(news_id):
    """
    Edit news
    ---
    patch:
      parameters:
        - in: path
          description: ID of news
          name: news_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: EditNewsRequestSchema
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: NewsSchema
    """
    news = db_get_or_raise(News, 'id', news_id)
    NewsSchema(load_instance=True).load(request.json, unknown=EXCLUDE, instance=news, partial=True)
    db.session.commit()
    return news, 200


@module.route('/news/<int:news_id>/image', methods=['POST'])
def post_news_image(news_id):
    """
    Edit news
    ---
    post:
      parameters:
        - in: path
          description: ID of news
          name: news_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          image/*:
            schema:
              type: string
              format: binary
      security:
        - JWTAccessToken: [ ]
        - CSRFAccessToken: [ ]
      responses:
        '204':
          description: OK
    """
    file = request.data
    if file == b'':
        raise InsufficientData('request', 'image')
    if len(file) > 4 * 1024 * 1024:
        raise QuotaExceeded('Image is too large', 4 * 1024 * 1024)
    news = db_get_or_raise(News, 'id', news_id)
    news.image = file
    db.session.commit()
    return {}, 204


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
      security:
        - JWTAccessToken: [ ]
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: NewsSchema
        '404':
          description: News not found
    """
    return db_get_or_raise(News, 'id', news_id), 200


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
      security:
        - JWTAccessToken: [ ]
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
    if news.image is None:
        raise DataConflict('Image not present')
    return send_file(io.BytesIO(news.image), mimetype='image/*')


@module.route('/news/<int:news_id>/post', methods=['POST'])
def post_news(news_id):
    """
    Post news
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
    news.posted = True
    news.post_time = datetime.datetime.utcnow()
    db.session.commit()
    return {}, 204


@module.route('/news/<int:news_id>/hide', methods=['POST'])
def hide_news(news_id):
    """
    Hide news
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
    news.posted = False
    news.post_time = datetime.datetime.utcnow()
    db.session.commit()
    return {}, 204
