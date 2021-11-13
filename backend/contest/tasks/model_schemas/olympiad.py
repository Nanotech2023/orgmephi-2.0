from marshmallow import fields, validate, post_dump, pre_load
from marshmallow import fields as m_f
from marshmallow_enum import EnumField
from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Related

from common.fields import text_validator, common_name_validator
from common.marshmallow import check_related_existence
from contest.tasks.model_schemas.location import OlympiadLocationSchema
from contest.tasks.models import *
from contest.tasks.models.certificate import CertificateType
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

    winner_1_condition = auto_field(column_name='winner_1_condition', required=True)
    winner_2_condition = auto_field(column_name='winner_2_condition', required=True)
    winner_3_condition = auto_field(column_name='winner_3_condition', required=True)
    diploma_1_condition = auto_field(column_name='diploma_1_condition', required=True)
    diploma_2_condition = auto_field(column_name='diploma_2_condition', required=True)
    diploma_3_condition = auto_field(column_name='diploma_3_condition', required=True)

    olympiad_type_id = auto_field(column_name='olympiad_type_id', required=True)
    subject = EnumField(OlympiadSubjectEnum, data_key='subject', by_value=True, required=True)
    level = EnumField(OlympiadLevelEnum, data_key='level', by_value=True, required=True)
    target_classes = fields.Nested(TargetClassSchema, many=True, dump_only=True, required=False)
    certificate_type = Related(['certificate_type_id'], required=False)

    @pre_load()
    def check_certificate(self, data, many, **kwargs):
        return check_related_existence(data, 'certificate_type', 'certificate_type_id',
                                       CertificateType, 'certificate_type_id')

"""
Contest
"""

"""
Stage
"""


class ContestGroupRestrictionSchema(SQLAlchemySchema):
    class Meta:
        model = ContestGroupRestriction
        load_instance = True
        sqla_session = db.session

    contest_id = auto_field(column_name='contest_id', dump_only=True, required=True)
    group_id = auto_field(column_name='group_id', dump_only=True, required=True)
    restriction = EnumField(ContestGroupRestrictionEnum, data_key='restriction', by_value=True, required=True)
    group_name = auto_field(column_name='group_name', dump_only=True, required=True)


class SimpleContestSchema(SQLAlchemySchema):
    class Meta:
        model = SimpleContest
        load_instance = True
        sqla_session = db.session

    contest_id = auto_field(column_name='contest_id', dump_only=True)
    visibility = auto_field(column_name='visibility', required=True)
    start_date = auto_field(column_name='start_date', required=True)
    end_date = auto_field(column_name='end_date', required=True)
    regulations = auto_field(column_name='regulations', validate=text_validator, required=False)
    status = EnumField(OlympiadStatusEnum, data_key='status', by_value=True)
    academic_year = fields.Integer()
    total_points = fields.Integer()
    tasks_number = fields.Integer()
    enrolled = fields.Boolean(required=False, dump_only=True)
    show_answer_after_contest = fields.Boolean(required=False, dump_only=True)
    deadline_for_appeal = auto_field(column_name='deadline_for_appeal', required=True)
    contest_duration = auto_field(column_name='contest_duration', required=False)
    result_publication_date = auto_field(column_name='result_publication_date', required=False)
    end_of_enroll_date = auto_field(column_name='end_of_enroll_date', required=False)
    previous_contest_id = auto_field(column_name='previous_contest_id', allow_none=True)
    locations = fields.Nested(OlympiadLocationSchema, many=True, required=True)
    target_classes = fields.Nested(TargetClassSchema, many=True, required=False)
    previous_participation_condition = EnumField(UserStatusEnum,
                                                 data_key='previous_participation_condition',
                                                 by_value=True, required=True)
    composite_type = EnumField(ContestTypeEnum,
                               data_key='composite_type',
                               by_value=True, required=True,
                               validate=validate.OneOf([ContestTypeEnum.SimpleContest]))
    holding_type = EnumField(ContestHoldingTypeEnum,
                             data_key='holding_type',
                             by_value=True, required=True)
    base_contest = fields.Nested(BaseContestSchema, required=True, dump_only=True)

    @post_dump(pass_original=True)
    def add_enrolled(self, data, original, many, **kwargs):
        from common.jwt_verify import jwt_get_id
        from contest.tasks.util import is_user_in_contest
        user_id = jwt_get_id()
        if user_id is not None:
            data['enrolled'] = is_user_in_contest(user_id, original)
        return data


class ContestInfoSchema(SQLAlchemySchema):
    class Meta:
        model = SimpleContest
        load_instance = True
        sqla_session = db.session

    name = auto_field(column_name='name', dump_only=True, required=True)
    subject = EnumField(OlympiadSubjectEnum, data_key='subject', by_value=True)
    contest_id = auto_field(column_name='contest_id', dump_only=True)
    academic_year = m_f.Int(required=True)
    composite_type = EnumField(ContestTypeEnum,
                               data_key='composite_type',
                               by_value=True, required=True,
                               validate=validate.OneOf([ContestTypeEnum.SimpleContest]))


class StageSchema(SQLAlchemySchema):
    class Meta:
        model = Stage
        load_instance = True
        sqla_session = db.session

    stage_id = auto_field(column_name='stage_id', dump_only=True)
    olympiad_id = auto_field(column_name='olympiad_id')
    stage_name = auto_field(column_name='stage_name', validate=common_name_validator)
    condition = EnumField(StageConditionEnum, data_key='condition', by_value=True)
    this_stage_condition = auto_field(column_name='this_stage_condition', validate=text_validator)
    stage_num = auto_field(column_name='stage_num')

    contests = fields.Nested(SimpleContestSchema, many=True)


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
    status = EnumField(OlympiadStatusEnum, data_key='status', by_value=True)
    academic_year = fields.Integer()
    composite_type = EnumField(ContestTypeEnum,
                               data_key='composite_type',
                               by_value=True, required=True,
                               validate=validate.OneOf([ContestTypeEnum.CompositeContest]))


class ContestSchema(OneOfSchema):
    type_schemas = {ContestTypeEnum.SimpleContest.value: SimpleContestSchema,
                    ContestTypeEnum.CompositeContest.value: CompositeContestSchema}
    type_field = "composite_type"
    type_field_remove = False

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
