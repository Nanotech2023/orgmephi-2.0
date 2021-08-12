from marshmallow import Schema, fields
from common import fields as common_fields


class LoginRequestSchema(Schema):
    username = common_fields.Username(required=True)
    password = common_fields.Password(required=True)
    remember_me = fields.Bool(required=True)


class CSRFPairSchema(Schema):
    csrf_access_token = fields.String(required=True)
    csrf_refresh_token = fields.String(required=True)
