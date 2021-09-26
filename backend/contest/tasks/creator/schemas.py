from datetime import timedelta

from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import fields as common_fields
from contest.tasks.model_schemas.contest import VariantSchema
from contest.tasks.model_schemas.olympiad import ContestSchema, BaseContestSchema, StageSchema
from contest.tasks.model_schemas.tasks import TaskSchema
from contest.tasks.models import OlympiadSubjectEnum, StageConditionEnum, ContestHoldingTypeEnum, \
    UserStatusEnum, OlympiadLevelEnum


# Base contest

class CreateBaseOlympiadRequestTaskCreatorSchema(Schema):
    name = common_fields.CommonName(required=True)
    description = common_fields.Text(required=True)
    rules = common_fields.Text(required=True)
    winner_1_condition = common_fields.FloatCondition(required=True)
    winner_2_condition = common_fields.FloatCondition(required=True)
    winner_3_condition = common_fields.FloatCondition(required=True)
    diploma_1_condition = common_fields.FloatCondition(required=True)
    diploma_2_condition = common_fields.FloatCondition(required=True)
    diploma_3_condition = common_fields.FloatCondition(required=True)
    olympiad_type_id = fields.Int(required=True)
    subject = EnumField(OlympiadSubjectEnum, required=True, by_value=True)
    level = EnumField(OlympiadLevelEnum, required=True, by_value=True)


class BaseOlympiadResponseTaskCreatorSchema(BaseContestSchema):
    class Meta(BaseContestSchema.Meta):
        exclude = []


class BaseOlympiadIdResponseTaskCreatorSchema(Schema):
    base_contest_id = fields.Int(required=True)


# Contest


class CreateSimpleContestRequestTaskCreatorSchema(Schema):
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    end_of_enroll_date = fields.DateTime(required=False)
    contest_duration = fields.TimeDelta(required=False, default=timedelta(seconds=0))
    result_publication_date = fields.DateTime(required=False)
    visibility = fields.Boolean(required=True)
    stage_id = fields.Int(required=False)
    previous_contest_id = fields.Int(required=False)
    previous_participation_condition = EnumField(UserStatusEnum, required=False, by_value=True)
    holding_type = EnumField(ContestHoldingTypeEnum, required=True, by_value=True)


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


class CreateVariantRequestTaskCreatorSchema(Schema):
    variant_description = common_fields.Text(required=True)


class VariantResponseTaskCreatorSchema(VariantSchema):
    class Meta(VariantSchema.Meta):
        exclude = ['contest_id']


class VariantIdResponseTaskCreatorSchema(Schema):
    variant_id = fields.Int(required=True)


class AllTasksResponseTaskCreatorSchema(Schema):
    tasks_list = fields.Nested(TaskSchema, many=True, required=True)


# Tasks

class CreatePlainRequestTaskCreatorSchema(Schema):
    num_of_task = fields.Int(required=True)
    recommended_answer = common_fields.Text(required=True)
    show_answer_after_contest = fields.Boolean(required=False)
    task_points = fields.Integer(required=False)


class CreateRangeRequestTaskCreatorSchema(Schema):
    num_of_task = fields.Int(required=True)
    start_value = fields.Float(required=True)
    end_value = fields.Float(required=True)
    show_answer_after_contest = fields.Boolean(required=False)
    task_points = fields.Integer(required=False)


class AnswersInTaskRequestTaskCreatorSchema(Schema):
    answer = common_fields.Text(required=True)
    is_right_answer = fields.Boolean(required=True)


class CreateMultipleRequestTaskCreatorSchema(Schema):
    num_of_task = fields.Int(required=True)
    show_answer_after_contest = fields.Boolean(required=False)
    task_points = fields.Integer(required=False)
    answers = fields.List(fields.Nested(AnswersInTaskRequestTaskCreatorSchema), required=True)


class TaskResponseTaskCreatorSchema(Schema):
    task_id = fields.Int(required=True)
    num_of_task = fields.Int(required=True)
    recommended_answer = common_fields.Text(required=False)
    start_value = fields.Float(required=False)
    end_value = fields.Float(required=False)
    show_answer_after_contest = fields.Boolean(required=False)
    task_points = fields.Integer(required=False)
    answers = fields.List(fields.Nested(AnswersInTaskRequestTaskCreatorSchema), required=False)


class TaskIdResponseTaskCreatorSchema(Schema):
    task_id = fields.Int(required=True)
