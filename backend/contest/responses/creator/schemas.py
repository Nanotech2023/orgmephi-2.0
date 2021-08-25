from marshmallow import Schema, fields
from common import fields as common_fields
from contest.responses.model_schemas.schemas import BaseAnswerSchema
from contest.responses.models import ResponseStatusEnum
from marshmallow_enum import EnumField


class AllUserAnswersResponseSchema(Schema):
    user_id = fields.Int(required=True)
    work_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    user_answers = fields.Nested(nested=BaseAnswerSchema, many=True, required=False)


class PlainAnswerRequestSchema(Schema):
    answer_text = common_fields.UserAnswer(required=True)


class RangeAnswerRequestSchema(Schema):
    answer = fields.Float(required=True)


class MultipleUserAnswerRequestSchema(Schema):
    answer = common_fields.UserAnswer(required=True)


class MultipleAnswerRequestSchema(Schema):
    answers = fields.Nested(nested=MultipleUserAnswerRequestSchema, many=True, required=True)


class UserResponseListSchema(Schema):
    user_id = fields.Int(required=True)
    mark = fields.Float(required=False, allow_none=True)


class ContestResultSheetResponseSchema(Schema):
    contest_id = fields.Int(required=True)
    user_row = fields.Nested(nested=UserResponseListSchema, many=True, required=True)


class UserResponseStatusResponseSchema(Schema):
    status = EnumField(ResponseStatusEnum, by_value=True, required=True)


class UserAnswerMarkResponseSchema(Schema):
    mark = fields.Float(required=True)


class UserTimeResponseRequestSchema(Schema):
    time = fields.TimeDelta(required=True)
