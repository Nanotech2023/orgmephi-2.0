from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields

from messages.models import ThreadType
from messages.model_schemas import ThreadCategorySchema, ThreadInfoSchema


class ListCategoriesMessagesResponseSchema(Schema):
    categories = fields.Nested(nested=ThreadCategorySchema, many=True)


class ListThreadsMessagesResponseSchema(Schema):
    threads = fields.Nested(nested=ThreadInfoSchema, many=True)


class CreateThreadMessagesRequestSchema(Schema):
    category = common_fields.CommonName(required=True)
    thread_type = EnumField(enum=ThreadType, by_value=True, required=True)
    topic = common_fields.CommonName(required=True)
    message = common_fields.Message(required=True)

    related_contest = fields.Integer(required=False)
    related_work = fields.Integer(required=False)


class CreateMessageMessagesRequestSchema(Schema):
    message = common_fields.Message(required=True)
