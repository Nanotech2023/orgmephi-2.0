from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

from contest.tasks.models import *
from contest.tasks.models import Stage
from user.models.auth import *
from common.fields import text_validator, common_name_validator


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
