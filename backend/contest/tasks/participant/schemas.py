from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import fields as common_fields
from contest.tasks.model_schemas.contest import VariantSchema
from contest.tasks.model_schemas.olympiad import ContestSchema
from contest.tasks.models.tasks import TaskTypeEnum


class AnswersInTaskRequestTaskParticipantSchema(Schema):
    answer = common_fields.Text(required=True)


class UserProctoringDataResponseTaskParticipantSchema(Schema):
    proctoring_login = common_fields.Text(required=True)
    proctoring_password = common_fields.Text(required=True)


class UserExternalSingleDataResponseTaskParticipantSchema(Schema):
    num_of_task = fields.Int(required=True)
    task_points = fields.Int(required=True)


class UserExternalDataResponseTaskParticipantSchema(Schema):
    tasks = fields.List(fields.Nested(UserExternalSingleDataResponseTaskParticipantSchema), required=False)
    num_of_tasks = fields.Int(required=True)


class TaskForUserResponseTaskParticipantSchema(Schema):
    task_id = fields.Integer(required=True)
    answers = fields.List(fields.Nested(AnswersInTaskRequestTaskParticipantSchema), required=False)
    task_type = EnumField(TaskTypeEnum, data_key='task_type', by_value=True)


class AllTaskResponseTaskParticipantSchema(Schema):
    tasks_list = fields.Nested(TaskForUserResponseTaskParticipantSchema, many=True, required=True)


class EnrollRequestTaskParticipantSchema(Schema):
    location_id = fields.Int(required=False)


class ChangeSupervisorRequestTaskParticipantSchema(Schema):
    supervisor = common_fields.CommonName(required=False)


class SimpleContestWithFlagResponseTaskParticipantSchema(Schema):
    contest = fields.Nested(ContestSchema, required=False, dump_only=True)
    enrolled = fields.Boolean(required=True)


class VariantWithCompletedTasksCountTaskParticipantSchema(Schema):
    variant = fields.Nested(VariantSchema, required=False)
    completed_task_count = fields.Int(required=True)


# For filter query


class FilterSimpleContestResponseTaskParticipantSchema(Schema):
    contest_list = fields.Nested(nested=SimpleContestWithFlagResponseTaskParticipantSchema, many=True)
    count = fields.Integer()
