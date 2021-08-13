from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from user.models.personal import *
from common.fields import email_validator, common_name_validator


class UserInfoSchema(SQLAlchemySchema):
    class Meta:
        model = UserInfo
        load_instance = True

    user_id = auto_field(column_name='user_id', dump_only=True)
    email = auto_field(column_name='email', allow_none=True, validate=email_validator)
    first_name = auto_field(column_name='first_name', allow_none=True, validate=common_name_validator)
    middle_name = auto_field(column_name='middle_name', allow_none=True, validate=common_name_validator)
    second_name = auto_field(column_name='second_name', allow_none=True, validate=common_name_validator)
    date_of_birth = auto_field(column_name='date_of_birth', allow_none=True)
