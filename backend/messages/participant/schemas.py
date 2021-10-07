from marshmallow import Schema, fields, post_load, ValidationError
from marshmallow_enum import EnumField
from common import fields as common_fields

from messages.models import ThreadType
from messages.model_schemas import ThreadCategorySchema


class ListCategoriesMessagesResponseSchema(Schema):
    categories = fields.Nested(nested=ThreadCategorySchema, many=True)


class CreateThreadMessagesRequestSchema(Schema):
    category = common_fields.CommonName(required=True)
    thread_type = EnumField(enum=ThreadType, by_value=True, required=True)
    topic = common_fields.CommonName(required=True)
    message = common_fields.Message(required=True)

    related_contest = fields.Integer(required=False)

    # noinspection PyUnusedLocal
    @post_load()
    def check_type(self, data, many, **kwargs):
        thread_type = data['thread_type']
        if (thread_type == ThreadType.appeal or thread_type == ThreadType.work or thread_type == ThreadType.contest)\
                and 'related_contest' not in data:
            raise ValidationError('Related contest is required for this thread type')
        return data


class CreateMessageMessagesRequestSchema(Schema):
    message = common_fields.Message(required=True)
