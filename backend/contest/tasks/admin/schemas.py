from marshmallow import Schema, fields
from common import fields as common_fields


class CreateOlympiadTypeRequestTaskAdminSchema(Schema):
    olympiad_type = common_fields.CommonName(required=True)


class OlympiadTypeResponseTaskAdminSchema(Schema):
    olympiad_type_id = fields.Int(required=True)
