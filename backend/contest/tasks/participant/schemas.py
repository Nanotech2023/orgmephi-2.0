from datetime import timedelta

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import fields as common_fields
from contest.tasks.model_schemas.location import OlympiadLocationSchema
from contest.tasks.model_schemas.olympiad import TargetClassSchema, BaseContestSchema, SimpleContestSchema
from contest.tasks.models import ContestHoldingTypeEnum, UserStatusEnum


class AnswersInTaskRequestTaskParticipantSchema(Schema):
    answer = common_fields.Text(required=True)


class TaskForUserResponseTaskParticipantSchema(Schema):
    task_id = fields.Integer(required=True)
    answers = fields.List(fields.Nested(AnswersInTaskRequestTaskParticipantSchema), required=False)


class AllTaskResponseTaskParticipantSchema(Schema):
    tasks_list = fields.Nested(TaskForUserResponseTaskParticipantSchema, many=True, required=True)


class EnrollRequestTaskParticipantSchema(Schema):
    location_id = fields.Int(required=False)


class SimpleContestWithFlagResponseTaskParticipantSchema(Schema):
    contest = fields.Nested(SimpleContestSchema, required=False, dump_only=True)
    enrolled = fields.Boolean(required=True)


# For filter query


class FilterSimpleContestResponseTaskParticipantSchema(Schema):
    contest_list = fields.Nested(nested=SimpleContestWithFlagResponseTaskParticipantSchema, many=True)
    count = fields.Integer()
