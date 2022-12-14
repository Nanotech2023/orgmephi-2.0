from marshmallow import Schema, fields
from common import fields as common_fields
from contest.responses.model_schemas.schemas import BaseAnswerSchema, AnswerWithoutMarkSchema, RightAnswerSchema
from contest.responses.models import ResponseStatusEnum
from contest.tasks.models import TaskTypeEnum
from contest.tasks.models.user import UserStatusEnum
from marshmallow_enum import EnumField
from contest.tasks.model_schemas.olympiad import ContestInfoSchema


class AllUserAnswersResponseSchema(Schema):
    user_id = fields.Int(required=True)
    work_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    user_answers = fields.Nested(nested=AnswerWithoutMarkSchema, many=True, required=False)


class AllUserMarksResponseSchema(Schema):
    user_id = fields.Int(required=True)
    work_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    user_answers = fields.Nested(nested=BaseAnswerSchema, many=True, required=True)


class TaskForUserResponseResultsSchema(Schema):
    task_id = fields.Integer(required=True)
    task_type = EnumField(TaskTypeEnum, data_key='task_type', by_value=True)
    task_points = fields.Int(required=True)


class UserResultForContestResponseSchema(Schema):
    user_id = fields.Int(required=True)
    work_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)
    user_answers = fields.Nested(nested=BaseAnswerSchema, many=True, required=True)
    tasks_list = fields.Nested(TaskForUserResponseResultsSchema, many=True, required=True)


class PlainAnswerRequestSchema(Schema):
    answer_text = common_fields.Text(required=True)


class RangeAnswerRequestSchema(Schema):
    answer = fields.Float(required=True)


class MultipleUserAnswerRequestSchema(Schema):
    answer = common_fields.Text(required=True)


class MultipleAnswerRequestSchema(Schema):
    answers = fields.List(fields.Nested(MultipleUserAnswerRequestSchema), required=True)


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
    time = fields.TimeDelta(required=True, nullable=False)


class UserResultsForContestResponseSchema(Schema):
    mark = fields.Float(required=True)
    status = EnumField(ResponseStatusEnum, by_value=True, required=True)
    user_status = EnumField(UserStatusEnum, by_value=True, required=True)
    contest_info = fields.Nested(nested=ContestInfoSchema, required=True)


class AllUserResultsResponseSchema(Schema):
    results = fields.List(fields.Nested(UserResultsForContestResponseSchema), required=True)
