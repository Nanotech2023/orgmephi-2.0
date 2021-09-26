from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField
from marshmallow import fields

from user.models.auth import *
from common import fields as common_fields

from .personal import UserInfoSchema
from .university import StudentInfoSchema
from .school import SchoolInfoSchema


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    username = common_fields.CommonName(required=True)
    role = EnumField(UserRoleEnum, by_value=True, required=True)
    type = EnumField(UserTypeEnum, by_value=True, required=True)


class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    name = common_fields.CommonName(required=True)


class UserFullSchema(UserSchema):
    user_info = Nested(nested=UserInfoSchema, many=False)
    student_info = Nested(nested=StudentInfoSchema, many=False)
    school_info = Nested(nested=SchoolInfoSchema, many=False)
    groups = Nested(nested=GroupSchema, many=True)
