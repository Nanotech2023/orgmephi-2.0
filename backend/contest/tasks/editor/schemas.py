from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import fields as common_fields
from contest.tasks.models import OlympiadSubjectEnum, StageConditionEnum, ContestHoldingTypeEnum, \
    UserStatusEnum


# Base contest

class UpdateBaseOlympiadRequestTaskEditorSchema(Schema):
    name = common_fields.CommonName(required=False)
    description = common_fields.Text(required=False)
    rules = common_fields.Text(required=False)
    winner_1_condition = common_fields.FloatCondition(required=False)
    winner_2_condition = common_fields.FloatCondition(required=False)
    winner_3_condition = common_fields.FloatCondition(required=False)
    diploma_1_condition = common_fields.FloatCondition(required=False)
    diploma_2_condition = common_fields.FloatCondition(required=False)
    diploma_3_condition = common_fields.FloatCondition(required=False)
    olympiad_type_id = fields.Int(required=False)
    subject = EnumField(OlympiadSubjectEnum, required=False, by_value=True)


# Contest

class UpdateContestRequestTaskEditorSchema(Schema):
    start_date = fields.DateTime(required=False)
    end_date = fields.DateTime(required=False)
    result_publication_date = fields.DateTime(required=False)
    end_of_enroll_date = fields.DateTime(required=False)
    visibility = fields.Boolean(required=False)
    contest_duration = fields.TimeDelta(required=False)
    previous_contest_id = fields.Int(required=False)
    previous_participation_condition = EnumField(UserStatusEnum, required=False, by_value=True)
    holding_type = EnumField(ContestHoldingTypeEnum, required=False, by_value=False)


class UpdatePreviousContestRequestTaskEditorSchema(Schema):
    previous_contest_id = fields.Int(required=True)
    previous_participation_condition = EnumField(UserStatusEnum, required=True, by_value=True)


# Stage

class UpdateStageRequestTaskEditorSchema(Schema):
    stage_name = common_fields.CommonName(required=False)
    stage_num = fields.Int(required=False)
    this_stage_condition = common_fields.Text(required=False)
    condition = EnumField(StageConditionEnum, required=False, by_value=True)


# Variant

class VariantResponseTaskEditorSchema(Schema):
    variant_id = fields.Int(required=True)
    variant_number = fields.Int(required=True)
    variant_description = common_fields.Text(required=True)


class UpdateVariantRequestTaskEditorSchema(Schema):
    variant_number = fields.Int(required=False)
    variant_description = common_fields.Text(required=False)


# Tasks

class AnswersInTaskRequestTaskEditorSchema(Schema):
    answer = common_fields.Text(required=True)
    is_right_answer = fields.Boolean(required=True)


class UpdatePlainRequestTaskEditorSchema(Schema):
    num_of_task = fields.Int(required=False)
    recommended_answer = common_fields.Text(required=False)
    show_answer_after_contest = fields.Boolean(required=False)
    task_points = fields.Integer(required=False)


class UpdateRangeRequestTaskEditorSchema(Schema):
    num_of_task = fields.Int(required=False)
    start_value = fields.Float(required=False)
    end_value = fields.Float(required=False)
    show_answer_after_contest = fields.Boolean(required=False)
    task_points = fields.Integer(required=False)


class UpdateMultipleRequestTaskEditorSchema(Schema):
    num_of_task = fields.Int(required=False)
    answers = fields.List(fields.Nested(AnswersInTaskRequestTaskEditorSchema), required=False)
    show_answer_after_contest = fields.Boolean(required=False)
    task_points = fields.Integer(required=False)


# Location

class UpdateLocationOfContestRequestTaskEditorSchema(Schema):
    locations = fields.List(fields.Int(), required=True)


# Target classes


class UpdateTargetClassesOfContestRequestTaskEditorSchema(Schema):
    target_classes_ids = fields.List(fields.Int(), required=True)
