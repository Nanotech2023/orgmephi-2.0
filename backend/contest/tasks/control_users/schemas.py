from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.model_schemas.auth import UserSchema
from user.models.auth import UserTypeEnum, UserRoleEnum
from user.model_schemas.university import StudentInfoSchema
from user.model_schemas.personal import UserInfoSchema


class UpdateUserInRequestCreatorSchema(Schema):
    users_id = fields.List(fields.Int(), required=True)


class UsersResponseSchema(Schema):
    users = fields.Nested(UserSchema, many=True, required=True)


class UserCertificateSchema(Schema):
    certificate = common_fields.BytesField(required=True)


