from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, UserRoleEnum
from user.model_schemas.personal import GenderEnum
from user.model_schemas.university import StudentUniversityCompatibleSchema
from user.model_schemas.school import SchoolType
from user.model_schemas.location import LocationCompatibleSchema
from user.model_schemas.document import DocumentCompatibleSchema


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


class UserLimitationsRequestUserSchema(Schema):
    hearing = fields.Boolean()
    sight = fields.Boolean()
    movement = fields.Boolean()


class UserInfoRequestUserSchema(Schema):
    email = common_fields.Email()
    first_name = common_fields.CommonName()
    middle_name = common_fields.CommonName()
    second_name = common_fields.CommonName()
    date_of_birth = fields.Date()
    gender = EnumField(enum=GenderEnum, by_value=True)
    dwelling = fields.Nested(nested=LocationCompatibleSchema, many=False)
    document = fields.Nested(nested=DocumentCompatibleSchema, many=False)
    limitations = fields.Nested(nested=UserLimitationsRequestUserSchema, many=False)


class StudentInfoRequestUserSchema(Schema):
    phone = common_fields.Phone()
    university = fields.Nested(nested=StudentUniversityCompatibleSchema, many=False)
    grade = common_fields.Grade()
    citizenship = common_fields.CommonName()
    region = common_fields.CommonName()
    city = common_fields.CommonName()


class SchoolInfoRequestUserSchema(Schema):
    school_type = EnumField(enum=SchoolType, by_value=True)
    number = fields.Integer()
    name = fields.String()
    grade = fields.Integer()
    location = fields.Nested(nested=LocationCompatibleSchema, many=False)
