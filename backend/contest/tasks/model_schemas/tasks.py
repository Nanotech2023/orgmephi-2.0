from marshmallow import validate, Schema, post_load
from marshmallow_enum import EnumField
from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields
from marshmallow import fields as m_f
from marshmallow_sqlalchemy.fields import Related

from common.errors import InsufficientData
from contest.tasks.models import *
from user.models.auth import *
from common.fields import text_validator, common_name_validator, sequential_number_validator, points_validator

"""
Task Pool
"""


class TaskPoolSchema(SQLAlchemySchema):
    class Meta:
        model = TaskPool
        load_instance = True
        sqla_session = db.session

    task_pool_id = auto_field(column_name='task_pool_id',
                              dump_only=True)
    name = auto_field(column_name='name',
                      validate=text_validator,
                      required=True)
    year = auto_field(column_name='year',
                      validate=validate.Range(min=2000),
                      required=True)
    orig_task_points = auto_field(column_name='orig_task_points',
                                  validate=points_validator,
                                  required=True)


"""
ContestTask
"""


class ContestTaskSchema(SQLAlchemySchema):
    class Meta:
        model = ContestTask
        load_instance = True
        sqla_session = db.session

    contest_task_id = auto_field(column_name='contest_task_id', dump_only=True)
    task_pools = fields.RelatedList(Related('task_pool_id'), attribute='task_pools', load_only=True)
    num = auto_field(column_name='num',
                     validate=sequential_number_validator,
                     required=True)
    task_points = auto_field(column_name='task_points',
                             validate=points_validator,
                             required=True)
    task_pools_values = fields.Nested(nested=TaskPoolSchema,
                                      many=True,
                                      dump_only=True,
                                      required=True,
                                      validate=validate.Length(min=1)
                                      )


"""
Task
"""


class PlainTaskSchema(SQLAlchemySchema):
    class Meta:
        model = PlainTask
        load_instance = True
        sqla_session = db.session

    task_id = auto_field(column_name='task_id', dump_only=True)
    name = auto_field(column_name='name',
                      validate=common_name_validator
                      )
    recommended_answer = auto_field(column_name='recommended_answer',
                                    validate=text_validator, required=True)
    answer_type = EnumField(TaskAnswerTypeEnum,
                            data_key='answer_type',
                            by_value=True,
                            required=False)


class RangeTaskSchema(SQLAlchemySchema):
    class Meta:
        model = RangeTask
        load_instance = True
        sqla_session = db.session

    task_id = auto_field(column_name='task_id', dump_only=True)
    name = auto_field(column_name='name',
                      validate=common_name_validator)
    start_value = auto_field(column_name='start_value',
                             required=True)
    end_value = auto_field(column_name='end_value',
                           required=True)


class AnswerSchema(Schema):
    answer = m_f.String(required=True)
    is_right_answer = m_f.Boolean(required=True)


class MultipleChoiceTaskSchema(SQLAlchemySchema):
    class Meta:
        model = MultipleChoiceTask
        load_instance = True
        sqla_session = db.session

    task_id = auto_field(column_name='task_id', dump_only=True)
    name = auto_field(column_name='name',
                      validate=common_name_validator)
    answers = m_f.Nested(AnswerSchema, many=True, required=False)
    # answers = auto_field(column_name='answers', many=True, required=False)


class TaskSchema(OneOfSchema):
    type_schemas = {
        TaskTypeEnum.PlainTask.value: PlainTaskSchema,
        TaskTypeEnum.RangeTask.value: RangeTaskSchema,
        TaskTypeEnum.MultipleChoiceTask.value: MultipleChoiceTaskSchema
    }

    type_field = "task_type"
    type_field_remove = True

    class_types = {
        PlainTaskSchema: TaskTypeEnum.PlainTask.value,
        RangeTaskSchema: TaskTypeEnum.RangeTask.value,
        MultipleChoiceTaskSchema: TaskTypeEnum.MultipleChoiceTask.value
    }

    def get_obj_type(self, obj):
        obj_type = obj.task_type
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type.value
