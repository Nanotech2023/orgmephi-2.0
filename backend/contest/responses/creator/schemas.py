from marshmallow import Schema, fields
from common import fields as common_fields
from contest.responses.model_schemas.schemas import ResponseAnswerListSchema, ResponseStatusSchema
from contest.responses.models import ResponseStatusEnum
from marshmallow_enum import EnumField


class AllUserAnswersResponseSchema(Schema):
    user_id = fields.Int(required=True)
    work_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    user_answers = fields.Nested(nested=ResponseAnswerListSchema, many=True, required=False)


class UserResponseStatusMarkResponseSchema(Schema):
    status = EnumField(ResponseStatusEnum, by_value=True, required=True)
    mark = fields.Float(required=False)


class UserResponseStatusHistoryResponseSchema(Schema):
    user_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    history = fields.Nested(nested=ResponseStatusSchema, many=True, required=True)


class UserResponseListSchema(Schema):
    user_id = fields.Int(required=True)
    mark = fields.Float(required=False, allow_none=True)


class ContestResultSheetResponseSchema(Schema):
    contest_id = fields.Int(required=True)
    user_row = fields.Nested(nested=UserResponseListSchema, many=True, required=True)


class AppealMessageRequestSchema(Schema):
    message = common_fields.Message(required=True)


class AppealReplyRequestSchema(Schema):
    message = common_fields.Message(required=True)
    accepted = fields.Bool(required=True)
    mark = fields.Float(required=False)


class AppealCreateInfoResponseSchema(Schema):
    appeal_id = fields.Int(required=True)


class PostUserAnswerSchema(Schema):
    user_answer = fields.Raw(required=True)
