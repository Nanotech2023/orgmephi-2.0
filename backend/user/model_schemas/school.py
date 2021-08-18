from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField
from marshmallow import fields
from user.models.school import *
from .location import LocationSchema


class SchoolInfoSchema(SQLAlchemySchema):
    class Meta:
        model = SchoolInfo
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    school_type = EnumField(enum=SchoolType, attribute='school_type', allow_none=True, by_value=True)
    number = auto_field(column_name='number', allow_none=True)
    name = auto_field(column_name='name', allow_none=True)
    grade = fields.Integer(allow_none=True)
    location = Nested(nested=LocationSchema, allow_none=False, many=False)
