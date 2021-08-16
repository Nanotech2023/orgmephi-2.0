from marshmallow import fields, Schema
from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

from contest.tasks.models import *
from user.models.auth import *
from common.fields import text_validator, common_name_validator

"""
User
"""


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = UserInContest
        load_instance = False
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
        load_instance = False
        sqla_session = db.session

    variant_id = auto_field(column_name='variant_id', dump_only=True)
    variant_number = auto_field(column_name='variant_number', required=True)
    variant_description = auto_field(column_name='name', validate=text_validator, required=True)


"""
Task
"""

# TODO DELETE AFTER TEST, ALREADY EXIST IN MODELS


class TaskType(enum.Enum):
    plain = "PlainTask"
    range = "RangeTask"
    multiple = "MultipleChoiceTask"
    base = "BaseTask"


class TaskImageSchema(SQLAlchemySchema):
    class Meta:
        model = Task
        load_instance = False
        sqla_session = db.session

    task_id = auto_field(column_name='variant_id', dump_only=True)
    image_of_task = auto_field(column_name='image_of_task', required=True)


class TaskPlainSchema(SQLAlchemySchema):
    class Meta:
        model = PlainTask
        load_instance = False
        sqla_session = db.session

    task_id = auto_field(column_name='variant_id', dump_only=True)
    num_of_task = auto_field(column_name='variant_number', required=True)
    recommended_answer = auto_field(column_name='name', validate=text_validator, required=True)


class TaskRangeSchema(SQLAlchemySchema):
    class Meta:
        model = RangeTask
        load_instance = False
        sqla_session = db.session

    task_id = auto_field(column_name='variant_id', dump_only=True)
    num_of_task = auto_field(column_name='variant_number', required=True)
    start_value = auto_field(column_name='name', validate=text_validator, required=True)
    end_value = auto_field(column_name='name', validate=text_validator, required=True)


class Answers(Schema):
    answer = auto_field(column_name='name', validate=text_validator, required=True)
    is_right_answer = auto_field(column_name='name', validate=text_validator, required=True)


class TaskMultipleSchema(SQLAlchemySchema):
    class Meta:
        model = MultipleChoiceTask
        load_instance = False
        sqla_session = db.session

    task_id = auto_field(column_name='variant_id', dump_only=True)
    num_of_task = auto_field(column_name='variant_number', required=True)
    answers = fields.Nested(Answers, many=True, required=True)


class TaskSchema(OneOfSchema):
    type_schemas = {TaskType.plain.value: TaskPlainSchema,
                    TaskType.range.value: TaskRangeSchema,
                    TaskType.multiple.value: TaskMultipleSchema, }
    type_field = "task_type"
    type_field_remove = False

    class_types = {TaskPlainSchema: TaskType.plain.value,
                   TaskRangeSchema: TaskType.range.value,
                   TaskMultipleSchema: TaskType.multiple.value}

    def get_obj_type(self, obj):
        obj_type = self.class_types.get(type(obj), None)
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type


"""
Contest
"""


# TODO DELETE AFTER TEST, ALREADY EXIST IN MODELS
class ContestType(enum.Enum):
    contest = "Contest"
    simpleContest = "SimpleContest"
    compositeContest = "CompositeContest"


class CompositeContestSchema(SQLAlchemySchema):
    class Meta:
        model = CompositeContest
        load_instance = False
        sqla_session = db.session

    contest_id = auto_field(column_name='contest_id', dump_only=True)
    visibility = auto_field(column_name='visibility', required=True)
    composite_type = EnumField(ContestTypeEnum, data_key='composite_type', by_value=True, required=True)
    recommended_answer = auto_field(column_name='name', validate=text_validator, required=True)


class SimpleSchema(SQLAlchemySchema):
    class Meta:
        model = SimpleContest
        load_instance = False
        sqla_session = db.session

    contest_id = auto_field(column_name='contest_id', dump_only=True)
    visibility = auto_field(column_name='visibility', required=True)
    composite_type = EnumField(ContestTypeEnum, data_key='composite_type', by_value=True, required=True)
    recommended_answer = auto_field(column_name='name', validate=text_validator, required=True)
    location = auto_field(column_name='location', validate=text_validator, required=True)
    start_time = auto_field(column_name='start_time', required=True)
    end_time = auto_field(column_name='end_time', required=True)
    previous_contest_id = auto_field(column_name='previous_contest_id', allow_none=True)
    previous_participation_condition = auto_field(column_name='previous_participation_condition',
                                                  validate=text_validator, allow_none=True)


class ContestSchema(OneOfSchema):
    type_schemas = {ContestType.simpleContest.value: SimpleContest,
                    ContestType.compositeContest.value: CompositeContestSchema }
    type_field = "composite_type"
    type_field_remove = False

    class_types = {SimpleContest: ContestType.simpleContest.value,
                   CompositeContestSchema: ContestType.compositeContest.value}

    def get_obj_type(self, obj):
        obj_type = self.class_types.get(type(obj), None)
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type


"""
Olympiad types
"""


class OlympiadTypeSchema(SQLAlchemySchema):
    class Meta:
        model = OlympiadType
        load_instance = False
        sqla_session = db.session

    olympiad_type_id = auto_field(column_name='olympiad_type_id', dump_only=True)
    olympiad_type = auto_field(column_name='olympiad_type', validate=common_name_validator, required=True)


"""
Base olympiad 
"""


class TargetClassSchema(SQLAlchemySchema):
    typeTargetClass = EnumField(TargetClassEnum, data_key='typeTargetClass', by_value=True, required=True)


class BaseContestSchema(SQLAlchemySchema):
    class Meta:
        model = BaseContest
        load_instance = False
        sqla_session = db.session

    base_contest_id = auto_field(column_name='base_contest_id', dump_only=True)
    name = auto_field(column_name='name', required=True)
    description = auto_field(column_name='description', validate=text_validator, required=True)
    rules = auto_field(column_name='rules', validate=text_validator, required=True)

    winning_condition = auto_field(column_name='winning_condition', required=True)
    laureate_condition = auto_field(column_name='winning_condition', required=True)

    olympiad_type_id = auto_field(column_name='olympiad_type_id', required=True)

    subject = EnumField(OlympiadSubjectEnum, data_key='subject', by_value=True, required=True)

    target_classes = fields.Nested(TargetClassSchema, many=True, required=True)


class StageSchema(SQLAlchemySchema):
    class Meta:
        model = Stage
        load_instance = False
        sqla_session = db.session

    stage_id = auto_field(column_name='stage_id', dump_only=True)
    olympiad_id = auto_field(column_name='olympiad_id', required=True)
    stage_name = auto_field(column_name='stage_name', validate=common_name_validator, required=True)
    condition = auto_field(column_name='condition', validate=text_validator, required=True)
    this_stage_condition = auto_field(column_name='condition', validate=text_validator, required=True)
    stage_num = EnumField(StageConditionEnum, data_key='subject', by_value=True, required=True)

