from marshmallow import Schema, fields
from common import fields as common_fields


class CreateOlympiadTypeRequestAdminSchema(Schema):
    olympiad_type = common_fields.CommonName(required=True)


class CreateOlympiadTypeSchema(Schema):
    olympiad_type_id = fields.Int(required=True)
