from marshmallow_oneofschema import OneOfSchema
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

    answer = auto_field(column_name='answer')


class MultipleChoiceAnswerSchema(SQLAlchemySchema):
    class Meta:
        model = MultipleChoiceAnswer
        load_instance = True
        sqla_session = db.session

    answers = auto_field(column_name='answers', many=True, required=True)


class PlainAnswerTextSchema(SQLAlchemySchema):
    class Meta:
        model = PlainAnswerText
        load_instance = True
        sqla_session = db.session

    answer_text = auto_field(column_name='answer_text')


class PlainAnswerFileSchema(SQLAlchemySchema):
    class Meta:
        model = PlainAnswerFile
        load_instance = True
        sqla_session = db.session

    filetype = EnumField(ResponseFiletypeEnum, data_key='filetype', by_value=True)


class AnswerSchema(OneOfSchema):
    type_schemas = {
        AnswerEnum.PlainAnswerText.value: PlainAnswerTextSchema,
        AnswerEnum.RangeAnswer.value: RangeAnswerSchema,
        AnswerEnum.MultipleChoiceAnswer.value: MultipleChoiceAnswerSchema,
        AnswerEnum.PlainAnswerFile.value: PlainAnswerFileSchema
    }

    type_field = "answer_type"
    type_field_remove = True

    class_types = {
        PlainAnswerTextSchema: AnswerEnum.PlainAnswerText.value,
        RangeAnswerSchema: AnswerEnum.RangeAnswer.value,
        MultipleChoiceAnswerSchema: AnswerEnum.MultipleChoiceAnswer.value,
        PlainAnswerFileSchema: AnswerEnum.PlainAnswerFile.value
    }

    def get_obj_type(self, obj):
        obj_type = obj.answer_type
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type.value


