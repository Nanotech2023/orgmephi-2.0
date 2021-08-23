from marshmallow import Schema, fields
from common import fields as common_fields


class AddCategoryMessagesRequestSchema(Schema):
    name = common_fields.CommonName(required=True)


class CleanupMessagesRequestSchema(Schema):
    amount = fields.Integer(required=True)
    delete_unresolved = fields.Boolean(default=False)
