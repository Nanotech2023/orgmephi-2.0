from marshmallow import Schema
from marshmallow_enum import EnumField
from common import fields as common_fields

from messages.models import ThreadStatus


class CreateMessageCreatorMessagesRequestSchema(Schema):
    message = common_fields.Message(required=True)


class ThreadStatusMessagesRequestSchema(Schema):
    status = EnumField(enum=ThreadStatus, required=True, by_value=True)
