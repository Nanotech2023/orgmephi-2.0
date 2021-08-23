from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import fields as common_fields

from .models import ThreadType, Thread
from .model_schemas import ThreadInfoSchema


class FilterThreadsMessagesRequestSchema(Schema):
    offset = fields.Integer()
    limit = fields.Integer()
    resolved = fields.Boolean()
    answered = fields.Boolean()
    thread_type = EnumField(enum=ThreadType, by_value=True)
    category_name = common_fields.CommonName()
    only_count = fields.Boolean()


class FilterThreadsMessagesResponseSchema(Schema):
    threads = fields.Nested(nested=ThreadInfoSchema, many=True)
    count = fields.Integer()


def filter_threads_query(args, user_id):
    marshmallow = FilterThreadsMessagesRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in ['resolved', 'answered', 'thread_type', 'category_name'] if v in marshmallow}

    query = Thread.query.filter_by(**filters)

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)
    if user_id is not None:
        query = query.filter(Thread.author_id == user_id)
    if offset is not None:
        query = query.order_by(Thread.update_time)
    if limit is not None:
        query = query.offset(offset).limit(limit)
    if marshmallow.get('only_count', False):
        return {'count': query.count()}, 200
    else:
        return {'threads': query.all(), 'count': query.count()}, 200
