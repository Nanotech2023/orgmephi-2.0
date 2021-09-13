from marshmallow import Schema, fields
from common import fields as common_fields
from user.model_schemas.auth import GroupSchema
from user.model_schemas.personal import UserInfoSchema


class SelfPasswordRequestUserSchema(Schema):
    new_password = common_fields.Password(required=True)
    old_password = common_fields.Password(required=True)


class SelfGroupsResponseUserSchema(Schema):
    groups = fields.Nested(GroupSchema, many=True, required=True)


class UserInfoRestrictedSchema(UserInfoSchema):
    class Meta(UserInfoSchema.Meta):
        exclude = ['email', 'first_name', 'middle_name', 'second_name', 'date_of_birth']
