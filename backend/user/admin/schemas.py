from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, UserRoleEnum


class RegisterInternalRequestUserSchema(Schema):
    username = common_fields.Username(required=True)
    password = common_fields.Password(required=True)


class PasswordRequestUserSchema(Schema):
    new_password = common_fields.Password(required=True)


class RoleRequestUserSchema(Schema):
    role = EnumField(UserRoleEnum, required=True, by_value=True)


class TypeRequestUserSchema(Schema):
    type = EnumField(UserTypeEnum, required=True, by_value=True)


class GroupAddRequestUserSchema(Schema):
    name = common_fields.CommonName(required=True)


class MembershipRequestUserSchema(Schema):
    group_id = fields.Int(required=True)


class PreregisterResponseUserSchema(Schema):
    registration_number = common_fields.Username(required=True)
    password = common_fields.Password(required=True)
