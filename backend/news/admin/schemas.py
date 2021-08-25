from marshmallow import Schema
from common import fields as common_fields


class AddCategoryNewsRequestSchema(Schema):
    name = common_fields.CommonName(required=True)
