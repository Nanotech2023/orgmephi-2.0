from marshmallow import Schema, fields
from user.model_schemas.auth import UserSchema, GroupSchema, UserFullSchema


class UserListResponseUserSchema(Schema):
    users = fields.Nested(nested=UserSchema, many=True, required=True)


class UserFullListResponseUserSchema(Schema):
    users = fields.Nested(nested=UserFullSchema, many=True, required=True)


class GroupListResponseUserSchema(Schema):
    groups = fields.Nested(nested=GroupSchema, many=True, required=True)
