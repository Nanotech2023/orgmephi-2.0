from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, UserRoleEnum
from user.model_schemas.university import StudentInfoSchema, StudentUniversityCompatibleSchema
from user.model_schemas.personal import UserInfoSchema


class RegisterInternalRequestAdminSchema(Schema):
    username = common_fields.Username(required=True)
    password = common_fields.Password(required=True)


class PasswordRequestAdminSchema(Schema):
    new_password = common_fields.Password(required=True)


class RoleRequestAdminSchema(Schema):
    role = EnumField(UserRoleEnum, required=True, by_value=True)


class TypeRequestAdminSchema(Schema):
    type = EnumField(UserTypeEnum, required=True, by_value=True)


class GroupAddRequestAdminSchema(Schema):
    name = common_fields.CommonName(required=True)


class MembershipRequestAdminSchema(Schema):
    group_id = fields.Int(required=True)


class PreregisterResponseAdminSchema(Schema):
    registration_number = common_fields.Username(required=True)
    password = common_fields.Password(required=True)


class UserInfoAdminSchema(UserInfoSchema):
    pass


class StudentInfoAdminSchema(StudentInfoSchema):
    university = fields.Nested(nested=StudentUniversityCompatibleSchema, allow_none=True, many=False)
