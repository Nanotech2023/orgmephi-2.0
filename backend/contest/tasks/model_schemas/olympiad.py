from marshmallow_enum import EnumField
from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields

from common.fields import text_validator, common_name_validator
from contest.tasks.model_schemas.contest import StageSchema
from contest.tasks.model_schemas.location import OlympiadLocationSchema
from contest.tasks.models import *
from contest.tasks.models.reference import TargetClass
from user.models.auth import *

"""
Target class
"""


class TargetClassSchema(SQLAlchemySchema):
    class Meta:
        model = TargetClass
        load_instance = True
        sqla_session = db.session

    target_class_id = auto_field(column_name='target_class_id', dump_only=True)
    target_class = auto_field(column_name='target_class', validate=common_name_validator, required=True)


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

    winner_1_condition = auto_field(column_name='winner_1_condition', required=False)
    winner_2_condition = auto_field(column_name='winner_2_condition', required=False)
    winner_3_condition = auto_field(column_name='winner_3_condition', required=False)
    diploma_1_condition = auto_field(column_name='diploma_1_condition', required=False)
    diploma_2_condition = auto_field(column_name='diploma_2_condition', required=False)
    diploma_3_condition = auto_field(column_name='diploma_3_condition', required=False)

    olympiad_type_id = auto_field(column_name='olympiad_type_id', required=True)
    subject = EnumField(OlympiadSubjectEnum, data_key='subject', by_value=True, required=True)
    target_classes = fields.Nested(TargetClassSchema, many=True, required=True)


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
    holding_type = EnumField(ContestHoldingTypeEnum,
                             data_key='holding_type',
                             by_value=True, required=True)
    stages = fields.Nested(StageSchema, many=True, required=True, dump_only=True)
    base_contest = fields.Nested(BaseContestSchema, required=True, dump_only=True)


class SimpleContestSchema(SQLAlchemySchema):
    class Meta:
        model = SimpleContest
        load_instance = True
        sqla_session = db.session

    contest_id = auto_field(column_name='contest_id', dump_only=True)
    visibility = auto_field(column_name='visibility', required=True)
    start_date = auto_field(column_name='start_date', required=True)
    end_date = auto_field(column_name='end_date', required=True)
    contest_duration = auto_field(column_name='contest_duration', required=True)
    result_publication_date = auto_field(column_name='result_publication_date', required=True)
    end_of_enroll_date = auto_field(column_name='end_of_enroll_date', required=True)
    previous_contest_id = auto_field(column_name='previous_contest_id', allow_none=True)
    locations = fields.Nested(OlympiadLocationSchema, many=True, required=True)
    target_classes = fields.Nested(TargetClassSchema, many=True, required=False)
    previous_participation_condition = EnumField(UserStatusEnum,
                                                 data_key='previous_participation_condition',
                                                 by_value=True, required=True)
    holding_type = EnumField(ContestHoldingTypeEnum,
                             data_key='holding_type',
                             by_value=True, required=True)
    base_contest = fields.Nested(BaseContestSchema, required=True, dump_only=True)


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
