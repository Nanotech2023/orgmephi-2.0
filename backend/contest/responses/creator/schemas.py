from marshmallow import Schema, fields
from common import fields as common_fields
from contest.responses.model_schemas.schemas import ResponseAnswerListSchema, ResponseStatusHistorySchema
from contest.responses.models import ResponseStatusEnum
from marshmallow_enum import EnumField


class UserResponseAnswersListSchema(Schema):
    user_id = fields.Int(required=True)
    work_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    user_answers = fields.Nested(nested=ResponseAnswerListSchema, many=True, required=False)


class ResponseStatusPostSchema(Schema):
    status = EnumField(ResponseStatusEnum, by_value=True, required=True)
    mark = fields.Float(required=False)


class UserResponseHistorySchema(Schema):
    user_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    history = fields.Nested(nested=ResponseStatusHistorySchema, many=True, required=True)


class UserResponseListSchema(Schema):
    user_id = fields.Int(required=True)
    mark = fields.Float(required=False)


class ContestResultSheetSchema(Schema):
    contest_id = fields.Int(required=True)
    user_row = fields.Nested(nested=UserResponseListSchema, many=True, required=True)


class AppealMessageSchema(Schema):
    message = common_fields.Message(required=True)


class AppealCreateInfoSchema(Schema):
    appeal_id = fields.Int(required=True)
