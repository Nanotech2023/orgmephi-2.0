from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from common import fields as common_fields
from contest.tasks.model_schemas.schemas import TaskSchema, ContestSchema, BaseContestSchema, StageSchema, VariantSchema
from contest.tasks.models import OlympiadSubjectEnum, TargetClassEnum, StageConditionEnum


# Base contest


class CreateBaseOlympiadSchema(Schema):
    name = common_fields.CommonName(required=True)
    description = common_fields.Text(required=True)
    rules = common_fields.Text(required=True)
    winning_condition = fields.Float(required=True)
    laureate_condition = fields.Float(required=True)
    olympiad_type_id = fields.Int(required=True)
    subject = EnumField(OlympiadSubjectEnum, required=True, by_value=True)
    target_classes = EnumField(TargetClassEnum, required=True, by_value=True)


class UpdateBaseOlympiadSchema(Schema):
    name = common_fields.CommonName(required=False)
    description = common_fields.Text(required=False)
    rules = common_fields.Text(required=False)
    winning_condition = fields.Float(required=False)
    laureate_condition = fields.Float(required=False)
    olympiad_type_id = fields.Int(required=False)
    subject = EnumField(OlympiadSubjectEnum, required=False, by_value=True)
    target_classes = EnumField(TargetClassEnum, required=False, by_value=True)


class GetBaseOlympiadSchema(Schema):
    base_contest_id = fields.Int(required=True)
    name = common_fields.CommonName(required=True)
    description = common_fields.Text(required=True)
    rules = common_fields.Text(required=True)
    winning_condition = fields.Float(required=True)
    laureate_condition = fields.Float(required=True)
    olympiad_type_id = fields.Int(required=True)
    subject = EnumField(OlympiadSubjectEnum, required=True, by_value=True)
    target_classes = EnumField(TargetClassEnum, required=True, by_value=True)


class BaseOlympiadIdSchema(Schema):
    base_contest_id = fields.Int(required=True)


class BaseCertificateSchema(Schema):
    certificate_template = common_fields.BytesField(required=True)


# Contest


class CreateSimpleContestSchema(Schema):
    location = common_fields.Location(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    visibility = fields.Boolean(required=True)
    previous_contest_id = fields.Int(required=False)
    previous_participation_condition = common_fields.Text(required=False)


class CreateCompositeContestSchema(Schema):
    visibility = fields.Boolean(required=True)


class GetCompositeContestSchema(Schema):
    contest_id = fields.Int(required=True)
    location = common_fields.Location(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    visibility = fields.Boolean(required=True)
    previous_contest_id = fields.Int(required=False)
    previous_participation_condition = common_fields.Text(required=False)


class ContestIdSchema(Schema):
    contest_id = fields.Int(required=True)


class UpdateContestSchema(Schema):
    contest_id = fields.Int(required=False)
    location = common_fields.Location(required=False)
    start_time = fields.DateTime(required=False)
    end_time = fields.DateTime(required=False)
    visibility = fields.Boolean(required=False)
    previous_contest_id = fields.Int(required=False)
    previous_participation_condition = common_fields.Text(required=False)


class UpdatePreviousContestSchema(Schema):
    previous_contest_id = fields.Int(required=True)
    previous_participation_condition = common_fields.Text(required=True)


# Stage


class CreateStageSchema(Schema):
    stage_name = common_fields.CommonName(required=True)
    stage_num = fields.Int(required=True)
    this_stage_condition = common_fields.Text(required=True)
    condition = EnumField(StageConditionEnum, required=True, by_value=True)


class GetStageSchema(Schema):
    stage_id = fields.Int(required=True)
    stage_name = common_fields.CommonName(required=True)
    stage_num = fields.Int(required=True)
    this_stage_condition = common_fields.Text(required=True)
    condition = EnumField(StageConditionEnum, required=True, by_value=True)


class StageIdSchema(Schema):
    stage_id = fields.Int(required=True)


class UpdateStageSchema(Schema):
    stage_name = common_fields.CommonName(required=False)
    stage_num = fields.Int(required=False)
    this_stage_condition = common_fields.Text(required=False)
    condition = EnumField(StageConditionEnum, required=False, by_value=True)


# All

class AllOlympiadsSchema(Schema):
    olympiad_list = fields.Nested(ContestSchema, many=True, required=True)


class AllBaseContestSchema(Schema):
    olympiad_list = fields.Nested(BaseContestSchema, many=True, required=True)


class AllStagesSchema(Schema):
    stages_list = fields.Nested(StageSchema, many=True, required=True)


class AllStagesSchema(Schema):
    stages_list = fields.Nested(StageSchema, many=True, required=True)


class AllVariantsSchema(Schema):
    stages_list = fields.Nested(VariantSchema, many=True, required=True)


# Variant


class CreateVariantSchema(Schema):
    variant_number = fields.Int(required=True)
    variant_description = common_fields.Text(required=True)


class GetVariantSchema(Schema):
    variant_id = fields.Int(required=True)
    variant_number = fields.Int(required=True)
    variant_description = common_fields.Text(required=True)


class VariantIdSchema(Schema):
    variant_id = fields.Int(required=True)


class UpdateVariantSchema(Schema):
    variant_number = fields.Int(required=False)
    variant_description = common_fields.Text(required=False)


class AllTasksSchema(Schema):
    stages_list = fields.Nested(TaskSchema, many=True, required=True)

# Tasks

"""
              task_id:
                $ref: '#/components/schemas/typeIdentifier'
              num_of_task:
                $ref: '#/components/schemas/typePartNum'
              recommended_answer:
                $ref: '#/components/schemas/typeOlympiadText'
              start_value:
                 $ref: '#/components/schemas/typeRangeAnswer'
              end_value:
                $ref: '#/components/schemas/typeRangeAnswer'
              answers:
                type: array
                items:
                  type: object
                  properties:
                    answer:
                      $ref: '#/components/schemas/typeMultipleAnswer'
                    is_right_answer:
                      $ref: '#/components/schemas/typeCorrectness'"""


class AnswersInTask(Schema):
    answer = common_fields.Text(required=True)
    is_right_answer = fields.Boolean(required=True)


class CreatePlainSchema(Schema):
    num_of_task = fields.Int(required=True)
    image_of_task = common_fields.BytesField(required=True)
    recommended_answer = common_fields.Text(required=True)


class CreateRangeSchema(Schema):
    num_of_task = fields.Int(required=True)
    image_of_task = common_fields.BytesField(required=True)
    start_value = fields.Float(required=True)
    end_value = fields.Float(required=True)


class CreateMultipleSchema(Schema):
    num_of_task = fields.Int(required=True)
    image_of_task = common_fields.BytesField(required=True)
    answer = fields.Nested(AnswersInTask, many=True, required=True)


class GetTaskSchema(Schema):
    task_id = fields.Int(required=True)
    num_of_task = fields.Int(required=True)
    image_of_task = common_fields.BytesField(required=True)
    recommended_answer = common_fields.Text(required=False)
    start_value = fields.Float(required=False)
    end_value = fields.Float(required=False)
    answer = fields.Nested(AnswersInTask, many=True, required=False)


class GetTaskImageSchema(Schema):
    task_id = fields.Int(required=True)
    image_of_task = common_fields.BytesField(required=True)


class TaskIdSchema(Schema):
    task_id = fields.Int(required=True)


class UpdatePlainSchema(Schema):
    num_of_task = fields.Int(required=False)
    image_of_task = common_fields.BytesField(required=False)
    recommended_answer = common_fields.Text(required=False)


class UpdateRangeSchema(Schema):
    num_of_task = fields.Int(required=False)
    image_of_task = common_fields.BytesField(required=False)
    start_value = fields.Float(required=False)
    end_value = fields.Float(required=False)


class UpdateMultipleSchema(Schema):
    num_of_task = fields.Int(required=False)
    image_of_task = common_fields.BytesField(required=False)
    answer = fields.Nested(AnswersInTask, many=True, required=False)
