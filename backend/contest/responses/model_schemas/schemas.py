from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

from contest.responses.models import *
from common.fields import message_validator
<<<<<<< HEAD
from common.fields import username_validator, group_name_validator
=======
>>>>>>> add: marshmallow for creator module


class ResponseSchema(SQLAlchemySchema):
    class Meta:
        model = Response
        load_instance = False
        sqla_session = db.session

    work_id = auto_field(column_name='work_id', dump_only=True)
    user_id = auto_field(column_name='user_id', dump_only=True)
    contest_id = auto_field(column_name='contest_id', dump_only=True)


class ResponseStatusSchema(SQLAlchemySchema):
    class Meta:
        model = ResponseStatus
        load_instance = False
        sqla_session = db.session

    status = EnumField(ResponseStatusEnum, data_key='status', by_value=True)
    mark = auto_field(column_name='mark', required=False)


class ResponseStatusHistorySchema(SQLAlchemySchema):
    class Meta:
        model = ResponseStatus
        load_instatnce = False
        sqla_session = db.session

    status = EnumField(ResponseStatusEnum, data_key='status', by_value=True)
    mark = auto_field(column_name='mark', required=False)
    appeal_id = auto_field(column_name='appeal_id', required=False)
    datetime = auto_field(column_name='datetime', dump_only=True)


class AppealSchema(SQLAlchemySchema):
    class Meta:
        model = Appeal
        load_instance = False
        sqla_session = db.session

    appeal_id = auto_field(column_name='appeal_id', dump_only=True)
    status_id = auto_field(column_name='status_id', dump_only=True)
    appeal_status = EnumField(AppealStatusEnum, data_key='appeal_status', by_value=True)
    appeal_message = auto_field(column_name='appeal_message', dump_only=True, validate=message_validator)
    appeal_response = auto_field(column_name='appeal_response', required=False, validate=message_validator)


class ResponseAnswerListSchema(SQLAlchemySchema):
    class Meta:
        model = ResponseAnswer
        load_instance = True
        sqla_session = db.session

    filetype = EnumField(ResponseFiletypeEnum, data_key='filetype', by_value=True)
    answer = auto_field(column_name='answer', dump_only=True)
    task_id = auto_field(column_name='task_id', dump_only=True)
    answer_id = auto_field(column_name='answer_id', dump_only=True)
    work_id = auto_field(column_name="work_id", dump_only=True)


class ResponseAnswerListSchema(ResponseAnswerSchema):
    class Meta:
        exclude = ["answer", "filetype", "work_id"]
