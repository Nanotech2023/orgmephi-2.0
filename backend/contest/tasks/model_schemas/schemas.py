from marshmallow import fields
from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

from contest.tasks.models import *
from user.models.auth import *
from common.fields import text_validator, common_name_validator

"""
User
"""


class UserInContestSchema(SQLAlchemySchema):
    class Meta:
        model = UserInContest
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    variant_id = auto_field(column_name='variant_id', dump_only=True)
    user_status = EnumField(UserStatusEnum, data_key='user_status', by_value=True, required=True)


"""
Variant
"""


class VariantSchema(SQLAlchemySchema):
    class Meta:
        model = Variant
        load_instance = True
        sqla_session = db.session

    variant_id = auto_field(column_name='variant_id', dump_only=True)
    contest_id = auto_field(column_name='contest_id', required=False)
    variant_number = auto_field(column_name='variant_number', required=True)
    variant_description = auto_field(column_name='variant_description', validate=text_validator, required=True)


"""
Task
"""


class PlainTaskSchema(SQLAlchemySchema):
    class Meta:
        model = PlainTask
        load_instance = True
        sqla_session = db.session

    task_id = auto_field(column_name='task_id', dump_only=True)
    num_of_task = auto_field(column_name='num_of_task', required=True)
    recommended_answer = auto_field(column_name='recommended_answer', validate=text_validator, required=True)


class RangeTaskSchema(SQLAlchemySchema):
    class Meta:
        model = RangeTask
        load_instance = True
        sqla_session = db.session

    task_id = auto_field(column_name='task_id', dump_only=True)
    num_of_task = auto_field(column_name='num_of_task', required=True)
    start_value = auto_field(column_name='start_value', required=True)
    end_value = auto_field(column_name='end_value', required=True)


class MultipleChoiceTaskSchema(SQLAlchemySchema):
    class Meta:
        model = MultipleChoiceTask
        load_instance = True
        sqla_session = db.session

    task_id = auto_field(column_name='task_id', dump_only=True)
    num_of_task = auto_field(column_name='num_of_task', required=False)
    answers = auto_field(column_name='answers', many=True, required=False)


class TaskSchema(OneOfSchema):
    type_schemas = {TaskTypeEnum.PlainTask.value: PlainTaskSchema,
                    TaskTypeEnum.RangeTask.value: RangeTaskSchema,
                    TaskTypeEnum.MultipleChoiceTask.value: MultipleChoiceTaskSchema, }
    type_field = "task_type"
    type_field_remove = True

    class_types = {PlainTaskSchema: TaskTypeEnum.PlainTask.value,
                   RangeTaskSchema: TaskTypeEnum.RangeTask.value,
                   MultipleChoiceTaskSchema: TaskTypeEnum.MultipleChoiceTask.value}

    def get_obj_type(self, obj):
        obj_type = obj.task_type
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type.value


"""
Contest
"""


class CompositeContestSchema(SQLAlchemySchema):
    class Meta:
        model = CompositeContest
        load_instance = True
        sqla_session = db.session

    contest_id = auto_field(column_name='contest_id', dump_only=True)
    visibility = auto_field(column_name='visibility', required=True)


class SimpleContestSchema(SQLAlchemySchema):
    class Meta:
        model = SimpleContest
        load_instance = True
        sqla_session = db.session

    contest_id = auto_field(column_name='contest_id', dump_only=True)
    visibility = auto_field(column_name='visibility', required=True)
    location = auto_field(column_name='location', validate=text_validator, required=True)
    start_date = auto_field(column_name='start_date', required=True)
    end_date = auto_field(column_name='end_date', required=True)
    previous_contest_id = auto_field(column_name='previous_contest_id', allow_none=True)
    previous_participation_condition = EnumField(UserStatusEnum,
                                                 data_key='previous_participation_condition',
                                                 by_value=True, required=True)


class ContestSchema(OneOfSchema):
    type_schemas = {ContestTypeEnum.SimpleContest.value: SimpleContestSchema,
                    ContestTypeEnum.CompositeContest.value: CompositeContestSchema}
    type_field = "composite_type"
    type_field_remove = True

    class_types = {SimpleContestSchema: ContestTypeEnum.SimpleContest.value,
                   CompositeContestSchema: ContestTypeEnum.CompositeContest.value}

    def get_obj_type(self, obj):
        obj_type = obj.composite_type
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type.value

    def get_data_type(self, data):
        location = data.get('location', None)
        if location is not None:
            return ContestTypeEnum.SimpleContest.value
        return ContestTypeEnum.CompositeContest.value


"""
Olympiad types
"""


class OlympiadTypeSchema(SQLAlchemySchema):
    class Meta:
        model = OlympiadType
        load_instance = True
        sqla_session = db.session

    olympiad_type_id = auto_field(column_name='olympiad_type_id', dump_only=True)
    olympiad_type = auto_field(column_name='olympiad_type', validate=common_name_validator, required=True)


"""
Base olympiad 
"""


class BaseContestSchema(SQLAlchemySchema):
    class Meta:
        model = BaseContest
        load_instance = True
        sqla_session = db.session

    base_contest_id = auto_field(column_name='base_contest_id', dump_only=True)
    name = auto_field(column_name='name', required=True)
    description = auto_field(column_name='description', validate=text_validator, required=True)
    rules = auto_field(column_name='rules', validate=text_validator, required=True)

    winning_condition = auto_field(column_name='winning_condition', required=True)
    laureate_condition = auto_field(column_name='laureate_condition', required=True)

    olympiad_type_id = auto_field(column_name='olympiad_type_id', required=True)

    subject = EnumField(OlympiadSubjectEnum, data_key='subject', by_value=True, required=True)

    target_classes = fields.List(EnumField(TargetClassEnum, by_value=True, required=True), data_key='target_classes',
                                 required=True)


class StageSchema(SQLAlchemySchema):
    class Meta:
        model = Stage
        load_instance = True
        sqla_session = db.session

    stage_id = auto_field(column_name='stage_id', dump_only=True)
    olympiad_id = auto_field(column_name='olympiad_id', required=False)
    stage_name = auto_field(column_name='stage_name', validate=common_name_validator, required=True)
    condition = EnumField(StageConditionEnum, data_key='condition', required=True, by_value=True)
    this_stage_condition = auto_field(column_name='this_stage_condition', validate=text_validator, required=True)
    stage_num = auto_field(column_name='stage_num', required=True)
