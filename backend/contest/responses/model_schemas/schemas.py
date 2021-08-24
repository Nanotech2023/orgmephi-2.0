from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields
from marshmallow_enum import EnumField
from marshmallow_sqlalchemy.fields import Related

from contest.responses.models import *


class ResponseSchema(SQLAlchemySchema):
    class Meta:
        model = Response
        load_instance = True
        sqla_session = db.session

    work_id = auto_field(column_name='work_id', dump_only=True)
    user_id = auto_field(column_name='user_id', dump_only=True)
    contest_id = auto_field(column_name='contest_id', dump_only=True)
    start_time = auto_field(column_name='start_time', dump_only=True)
    status = EnumField(ResponseStatusEnum, data_key='status', by_value=True)


class AppealSchema(SQLAlchemySchema):
    class Meta:
        model = Appeal
        load_instance = True
        sqla_session = db.session

    appeal_id = auto_field(column_name='appeal_id', dump_only=True)
    status_id = auto_field(column_name='work_status', dump_only=True)
    appeal_status = EnumField(AppealStatusEnum, data_key='appeal_status', by_value=True)


class BaseAnswerSchema(SQLAlchemySchema):
    class Meta:
        model = BaseAnswer
        load_instance = True
        sqla_session = db.session

    answer_id = auto_field(column_name='answer_id', dump_only=True)
    answer_type = EnumField(AnswerEnum, data_key='answer_type', by_value=True)


class RangeAnswerSchema(SQLAlchemySchema):
    class Meta:
        model = RangeAnswer
        load_instance = True
        sqla_session = db.session

    answer = auto_field(column_name='answer', dump_only=True)


class MultipleChoiceAnswerSchema(SQLAlchemySchema):
    class Meta:
        model = MultipleChoiceAnswer
        load_instance = True
        sqla_session = db.session

    answers = Related(column=['answer'], data_key='answers', required=True)


class PlainAnswerSchema(SQLAlchemySchema):
    class Meta:
        model = PlainAnswer
        load_instance = True
        sqla_session = db.session

    answer_text = auto_field(column_name='answer_text', dump_only=True)
