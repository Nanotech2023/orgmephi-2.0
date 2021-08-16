from marshmallow import pre_load
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from user.models.personal import *
from common.fields import Email, common_name_validator
from common.util import db_get_one_or_none
from common.errors import AlreadyExists


class UserInfoSchema(SQLAlchemySchema):
    class Meta:
        model = UserInfo
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    email = Email(attribute='email', allow_none=True)
    first_name = auto_field(column_name='first_name', allow_none=True, validate=common_name_validator)
    middle_name = auto_field(column_name='middle_name', allow_none=True, validate=common_name_validator)
    second_name = auto_field(column_name='second_name', allow_none=True, validate=common_name_validator)
    date_of_birth = auto_field(column_name='date_of_birth', allow_none=True)

    @pre_load()
    def check_email(self, data, **kwargs):
        email = data.get('email', None)
        if isinstance(email, str):
            info = db_get_one_or_none(UserInfo, 'email', email)
            if info is not None:
                current_email = getattr(getattr(self, 'instance', None), 'email', None)
                if current_email != email:
                    raise AlreadyExists('user.email', email)
        return data
