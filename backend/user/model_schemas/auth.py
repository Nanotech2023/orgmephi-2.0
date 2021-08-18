from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

from user.models.auth import *


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
