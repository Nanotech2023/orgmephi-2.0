from marshmallow import Schema, fields
from common import fields as common_fields
from user.model_schemas.auth import GroupSchema


class PasswordRequestProfileSchema(Schema):
    new_password = common_fields.Password(required=True)
    old_password = common_fields.Password(required=True)


class GroupsResponseProfileSchema(Schema):
    groups = fields.Nested(GroupSchema, many=True, required=True)