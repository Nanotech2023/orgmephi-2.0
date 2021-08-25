from marshmallow import pre_load, fields, Schema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField

from common import fields as common_fields
from common.util import db_get_one_or_none
from common.errors import AlreadyExists

from user.models.personal import *

from .location import LocationSchema, LocationInputSchema
from .document import DocumentSchema, DocumentInputSchema


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

    user_id = auto_field(column_name='user_id', dump_only=True)
    email = auto_field(column_name='email', allow_none=True)
    first_name = auto_field(column_name='first_name', allow_none=True)
    middle_name = auto_field(column_name='middle_name', allow_none=True)
    second_name = auto_field(column_name='second_name', allow_none=True)
    date_of_birth = auto_field(column_name='date_of_birth', allow_none=True)
    place_of_birth = auto_field(column_name='place_of_birth', allow_none=True)
    gender = EnumField(enum=GenderEnum, allow_none=True, by_value=True)
    dwelling = Nested(nested=LocationSchema, allow_none=True, many=False)
    document = Nested(nested=DocumentSchema, allow_none=True, many=False)
    limitations = Nested(nested=UserLimitationsSchema, allow_none=True, many=False)

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


class UserLimitationsInputSchema(Schema):
    hearing = fields.Boolean()
    sight = fields.Boolean()
    movement = fields.Boolean()


class UserInfoInputSchema(Schema):
    email = common_fields.Email()
    first_name = common_fields.CommonName()
    middle_name = common_fields.CommonName()
    second_name = common_fields.CommonName()
    date_of_birth = fields.Date()
    place_of_birth = common_fields.FreeDescription()
    gender = EnumField(enum=GenderEnum, by_value=True)
    dwelling = fields.Nested(nested=LocationInputSchema, many=False)
    document = fields.Nested(nested=DocumentInputSchema, many=False)
    limitations = fields.Nested(nested=UserLimitationsInputSchema, many=False)
