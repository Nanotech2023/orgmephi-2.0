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
    contest_id = fields.Integer(attribute='related_contest_id')
    work_id = fields.Integer(attribute='related_work_id')


class FilterThreadsMessagesResponseSchema(Schema):
    threads = fields.Nested(nested=ThreadInfoSchema, many=True)
    count = fields.Integer()


_filter_fields = ['resolved', 'answered', 'thread_type', 'category_name', 'related_contest_id', 'related_work_id']


def filter_threads_query(args, user_id):
    marshmallow = FilterThreadsMessagesRequestSchema().load(args)

    filters = {v: marshmallow[v] for v in _filter_fields if v in marshmallow}

    query = Thread.query.filter_by(**filters)

    offset = marshmallow.get('offset', None)
    limit = marshmallow.get('limit', None)
    if user_id is not None:
        query = query.filter(Thread.author_id == user_id)
    query = query.order_by(Thread.update_time)
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)
    if marshmallow.get('only_count', False):
        return {'count': query.count()}, 200
    else:
        return {'threads': query.all(), 'count': query.count()}, 200
