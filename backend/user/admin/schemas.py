from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, UserRoleEnum
from user.model_schemas.university import StudentInfoSchema, StudentUniversityCompatibleSchema
from user.model_schemas.personal import UserInfoSchema


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


class UserInfoRequestUserSchema(UserInfoSchema):
    pass


class StudentInfoRequestUserSchema(StudentInfoSchema):
    university = fields.Nested(nested=StudentUniversityCompatibleSchema, allow_none=True, many=False)
