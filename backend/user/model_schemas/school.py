from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField
from marshmallow import fields

from user.models.school import *
from common import fields as common_fields

from .location import LocationSchema


class SchoolInfoSchema(SQLAlchemySchema):
    class Meta:
        model = SchoolInfo
        load_instance = True
        sqla_session = db.session

    user_id = fields.Integer(dump_only=True)
    school_type = EnumField(enum=SchoolType, by_value=True)
    number = fields.Integer()
    name = common_fields.SchoolName()
    grade = fields.Integer()
    location = Nested(nested=LocationSchema, many=False)
