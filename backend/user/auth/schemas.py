from marshmallow import Schema, fields
from common import fields as common_fields


class LoginRequestUserSchema(Schema):
    username = common_fields.Username(required=True)
    password = common_fields.Password(required=True)
    remember_me = fields.Bool(required=True)


class CSRFPairUserSchema(Schema):
    csrf_access_token = fields.String(required=True)
    csrf_refresh_token = fields.String(required=True)
    confirmed = fields.Bool(required=True)
