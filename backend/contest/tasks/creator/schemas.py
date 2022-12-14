from datetime import timedelta

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import fields as common_fields
from contest.tasks.model_schemas.contest import VariantSchema
from contest.tasks.model_schemas.olympiad import ContestSchema, BaseContestSchema, StageSchema, \
    ContestGroupRestrictionEnum
from contest.tasks.model_schemas.tasks import TaskSchema, TaskPoolSchema, ContestTaskSchema
from contest.tasks.models import StageConditionEnum, ContestHoldingTypeEnum, \
    UserStatusEnum


# Base contest

class BaseOlympiadResponseTaskCreatorSchema(BaseContestSchema):
    class Meta(BaseContestSchema.Meta):
        exclude = []


class BaseOlympiadIdResponseTaskCreatorSchema(Schema):
    base_contest_id = fields.Int(required=True)


class UserProctoringDataRequestTaskCreatorSchema(Schema):
    proctoring_login = common_fields.Text(required=True)
    proctoring_password = common_fields.Text(required=True)

# Task pool


class TaskPoolIdResponseTaskCreatorSchema(Schema):
    task_pool_id = fields.Int(required=True)


class FilterTaskPoolAllRequestSchema(Schema):
    base_contest_id = fields.Integer()


class AllTaskPoolsResponseTaskCreatorSchema(Schema):
    task_pools_list = fields.Nested(TaskPoolSchema, many=True, required=True)


# Contest Task


class ContestTaskResponseTaskCreatorSchema(Schema):
    contest_task_id = fields.Int(required=True)


class AllContestTaskResponseTaskCreatorSchema(Schema):
    contest_task_list = fields.Nested(ContestTaskSchema, many=True, required=True)

# Contest


class CreateSimpleContestRequestTaskCreatorSchema(Schema):
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    end_of_enroll_date = fields.DateTime(required=False)
    deadline_for_appeal = fields.DateTime(required=False)
    show_result_after_finish = fields.Boolean(required=False)
    contest_duration = fields.TimeDelta(required=False, default=timedelta(seconds=0))
    result_publication_date = fields.DateTime(required=False)
    visibility = fields.Boolean(required=True)
    show_answer_after_contest = fields.Boolean(required=True)
    stage_id = fields.Int(required=False)
    previous_contest_id = fields.Int(required=False)
    previous_participation_condition = EnumField(UserStatusEnum, required=False, by_value=True)
    holding_type = EnumField(ContestHoldingTypeEnum, required=True, by_value=True)
    regulations = common_fields.Text(required=False)


class CreateCompositeContestRequestTaskCreatorSchema(Schema):
    visibility = fields.Boolean(required=True)
    holding_type = EnumField(ContestHoldingTypeEnum, required=True, by_value=True)


class ContestResponseTaskCreatorSchema(Schema):
    contest_id = fields.Int(required=True)
    holding_type = EnumField(ContestHoldingTypeEnum, required=False, by_value=True)
    location = common_fields.Location(required=False)
    start_date = fields.DateTime(required=False)
    end_of_enroll_date = fields.DateTime(required=False)
    end_date = fields.DateTime(required=False)
    deadline_for_appeal = fields.DateTime(required=False)
    show_result_after_finish = fields.Boolean(required=False)
    result_publication_date = fields.DateTime(required=False)
    contest_duration = fields.TimeDelta(required=False)
    visibility = fields.Boolean(required=True)
    previous_contest_id = fields.Int(required=False)
    previous_participation_condition = EnumField(UserStatusEnum, required=False, by_value=True)


class ContestIdResponseTaskCreatorSchema(Schema):
    contest_id = fields.Int(required=True)


# Stage


class CreateStageRequestTaskCreatorSchema(Schema):
    stage_name = common_fields.CommonName(required=True)
    stage_num = fields.Int(required=True)
    this_stage_condition = common_fields.Text(required=True)
    condition = EnumField(StageConditionEnum, required=True, by_value=True)


class StageResponseTaskCreatorSchema(StageSchema):
    class Meta(StageSchema.Meta):
        exclude = ['olympiad_id']


class StageIdResponseTaskCreatorSchema(Schema):
    stage_id = fields.Int(required=True)


# All

class AllOlympiadsResponseTaskCreatorSchema(Schema):
    olympiad_list = fields.Nested(ContestSchema, many=True, required=True)


class AllBaseContestResponseTaskCreatorSchema(Schema):
    olympiad_list = fields.Nested(BaseContestSchema, many=True, required=True)


class AllStagesResponseTaskCreatorSchema(Schema):
    stages_list = fields.Nested(StageSchema, many=True, required=True)


class AllVariantsResponseTaskCreatorSchema(Schema):
    variants_list = fields.Nested(VariantSchema, many=True, required=True)


# Variant


class VariantResponseTaskCreatorSchema(VariantSchema):
    class Meta(VariantSchema.Meta):
        exclude = ['contest_id']


class VariantIdResponseTaskCreatorSchema(Schema):
    variant_id = fields.Int(required=True)


class AllTasksResponseTaskCreatorSchema(Schema):
    tasks_list = fields.Nested(TaskSchema, many=True, required=True)


# Tasks

class AnswersInTaskRequestTaskCreatorSchema(Schema):
    answer = common_fields.Text(required=True)
    is_right_answer = fields.Boolean(required=True)


class TaskResponseTaskCreatorSchema(Schema):
    task_id = fields.Int(required=True)
    name = common_fields.CommonName(required=True)
    num_of_task = fields.Int(required=True)
    recommended_answer = common_fields.Text(required=False)
    start_value = fields.Float(required=False)
    end_value = fields.Float(required=False)
    task_points = fields.Integer(required=False)
    answers = fields.List(fields.Nested(AnswersInTaskRequestTaskCreatorSchema), required=False)


class TaskIdResponseTaskCreatorSchema(Schema):
    task_id = fields.Int(required=True)


# Restrictions


class ListElemContestGroupRestrictionAdminSchema(Schema):
    group_name = common_fields.CommonName(required=True)
    restriction = EnumField(ContestGroupRestrictionEnum, by_value=True, required=True)


class ContestGroupRestrictionListAdminSchema(Schema):
    restrictions = fields.Nested(ListElemContestGroupRestrictionAdminSchema, many=True, required=True)
