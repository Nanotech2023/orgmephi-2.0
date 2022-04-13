from marshmallow import Schema, fields
from common import fields as common_fields
from user.model_schemas.auth import GroupSchema


class SelfPasswordRequestUserSchema(Schema):
    new_password = common_fields.Password(required=True)
    old_password = common_fields.Password(required=True)


class UserPhoneSchema(Schema):
    phone = common_fields.Phone()


class SelfGroupsResponseUserSchema(Schema):
    groups = fields.Nested(GroupSchema, many=True, required=True)


class SelfUnfilledResponseSchema(Schema):
    unfilled = fields.List(fields.Dict())
