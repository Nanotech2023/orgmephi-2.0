from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, UserRoleEnum
from user.model_schemas.university import StudentUniversityCompatibleSchema


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


class UserInfoRequestUserSchema(Schema):
    email = common_fields.Email()
    first_name = common_fields.CommonName()
    middle_name = common_fields.CommonName()
    second_name = common_fields.CommonName()
    date_of_birth = fields.Date()


class StudentInfoRequestUserSchema(Schema):
    phone = common_fields.Phone()
    university = fields.Nested(nested=StudentUniversityCompatibleSchema, many=False)
    grade = common_fields.Grade()
    citizenship = common_fields.CommonName()
    region = common_fields.CommonName()
    city = common_fields.CommonName()
