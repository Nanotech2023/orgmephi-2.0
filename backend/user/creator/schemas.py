from marshmallow import Schema, fields
from user.model_schemas.auth import UserSchema, GroupSchema


class UserListResponseCreatorSchema(Schema):
    users = fields.Nested(nested=UserSchema, many=True, required=True)


class GroupListResponseCreatorSchema(Schema):
    groups = fields.Nested(nested=GroupSchema, many=True, required=True)
