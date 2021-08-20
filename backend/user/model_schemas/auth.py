from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField

from user.models.auth import *

from .personal import UserInfoSchema
from .university import StudentInfoSchema
from .school import SchoolInfoSchema


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    id = auto_field(column_name='id', dump_only=True)
    username = auto_field(column_name='username')
    role = EnumField(UserRoleEnum, data_key='role', by_value=True)
    type = EnumField(UserTypeEnum, data_key='type', by_value=True)


class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True
        sqla_session = db.session

    id = auto_field(column_name='id', dump_only=True)
    name = auto_field(column_name='name')


class UserFullSchema(UserSchema):
    user_info = Nested(nested=UserInfoSchema, many=False)
    student_info = Nested(nested=StudentInfoSchema, many=False)
    school_info = Nested(nested=SchoolInfoSchema, many=False)
    groups = Nested(nested=GroupSchema, many=True)
