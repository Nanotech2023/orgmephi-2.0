from marshmallow import pre_load, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField

from common import fields as common_fields
from common.util import db_get_one_or_none
from common.errors import AlreadyExists

from user.models.personal import *

from .location import LocationSchema
from .document import DocumentSchema


class UserLimitationsSchema(SQLAlchemySchema):
    class Meta:
        model = UserLimitations
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    hearing = auto_field(column_name='hearing', allow_none=True)
    sight = auto_field(column_name='sight', allow_none=True)
    movement = auto_field(column_name='movement', allow_none=True)


class UserInfoSchema(SQLAlchemySchema):
    class Meta:
        model = UserInfo
        load_instance = True
        sqla_session = db.session

    user_id = fields.Integer(dump_only=True)
    email = common_fields.Email()
    phone = common_fields.Phone()
    first_name = common_fields.CommonName()
    middle_name = common_fields.CommonName()
    second_name = common_fields.CommonName()
    date_of_birth = fields.Date()
    place_of_birth = common_fields.FreeDescription()
    gender = EnumField(enum=GenderEnum, by_value=True)
    dwelling = Nested(nested=LocationSchema, many=False)
    document = Nested(nested=DocumentSchema, many=False)
    limitations = Nested(nested=UserLimitationsSchema, many=False)

    # noinspection PyUnusedLocal
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


class UserPhoneSchema(SQLAlchemySchema):
    phone = common_fields.Phone()


class UserInfoSchemaPersonal(UserInfoSchema):
    class Meta(UserInfoSchema.Meta):
        exclude = ['user_id', 'email', 'phone', 'dwelling', 'limitations']
