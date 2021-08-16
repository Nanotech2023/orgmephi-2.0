from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, UserRoleEnum
from user.model_schemas.university import StudentInfoSchema
from user.model_schemas.personal import UserInfoSchema


class CreateOlympiadTypeRequestAdminSchema(Schema):
    olympiad_type = common_fields.CommonName(required=True)


class OlympiadTypeSchema(Schema):
    olympiad_type_id = fields.Int(required=True)
