from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, UserRoleEnum


class RegisterInternalRequestSchema(Schema):
    username = common_fields.Username(required=True)
    password = common_fields.Password(required=True)


class PasswordAdminRequestSchema(Schema):
    new_password = common_fields.Password(required=True)


class RoleRequestSchema(Schema):
    role = EnumField(UserRoleEnum, required=True, by_value=True)


class TypeRequestSchema(Schema):
    type = EnumField(UserTypeEnum, required=True, by_value=True)


class GroupAddRequestSchema(Schema):
    name = common_fields.CommonName(required=True)


class MembershipRequestSchema(Schema):
    group_id = fields.Int(required=True)


class PreregisterResponseSchema(Schema):
    registration_number = common_fields.Username(required=True)
    password = common_fields.Password(required=True)
