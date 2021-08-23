from marshmallow import Schema, fields
from common import fields as common_fields


class AddCategoryMessagesSchema(Schema):
    name = common_fields.CommonName(required=True)


class CleanupMessagesSchema(Schema):
    amount = fields.Integer(required=True)
    delete_unresolved = fields.Boolean(default=False)
