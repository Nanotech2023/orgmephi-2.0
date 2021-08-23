from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields

from messages.models import ThreadStatus, ThreadType
from messages.model_schemas import ThreadInfoSchema


class CreateMessageCreatorMessagesRequestSchema(Schema):
    message = common_fields.Message(required=True)


class ThreadStatusMessagesRequestSchema(Schema):
    status = EnumField(enum=ThreadStatus, required=True, by_value=True)


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
