from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

from user.models.auth import *
from common.fields import username_validator, group_name_validator


class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field(column_name='id', dump_only=True)
    username = auto_field(column_name='username', validate=username_validator)
    role = EnumField(UserRoleEnum, data_key='role', by_value=True)
    type = EnumField(UserTypeEnum, data_key='type', by_value=True)


class GroupSchema(SQLAlchemySchema):
    class Meta:
        model = Group
        load_instance = True

    id = auto_field(column_name='id', dump_only=True)
    name = auto_field(column_name='name', validate=group_name_validator)
