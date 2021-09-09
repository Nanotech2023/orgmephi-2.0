from marshmallow import Schema, fields

from common import fields as common_fields

from news.models import News
from news.model_schemas import NewsInfoSchema


class FilterNewsRequestSchema(Schema):
    offset = fields.Integer()
    limit = fields.Integer()
    posted = fields.Boolean()
    category_name = common_fields.CommonName()
    grade = fields.Integer()
    title = common_fields.CommonName()
    contest_id = fields.Integer(attribute='related_contest_id')
    only_count = fields.Boolean()


class FilterNewsResponseSchema(Schema):
    news = fields.Nested(nested=NewsInfoSchema, many=True)
    count = fields.Integer()


_filter_fields = ['posted', 'category_name', 'grade', 'related_contest_id']


# noinspection DuplicatedCode
def filter_news_query(args, only_posted):
    marshmallow = FilterNewsRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in _filter_fields if v in marshmallow}

    query = News.query.filter_by(**filters)

    title = marshmallow.get('title', None)
    if title is not None:
        query = query.filter(News.title.like(f'%{title}%'))
    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)
    if only_posted:
        query = query.filter_by(posted=True)
    query = query.order_by(News.post_time)
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    if marshmallow.get('only_count', False):
        return {'count': query.count()}, 200
    else:
        return {'news': query.all(), 'count': query.count()}, 200
