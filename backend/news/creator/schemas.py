from marshmallow import Schema, fields
from common import fields as common_fields

from news.model_schemas import NewsCategorySchema


class ListCategoriesNewsResponseSchema(Schema):
    categories = fields.Nested(nested=NewsCategorySchema, many=True)


class CreateNewsRequestSchema(Schema):
    category = common_fields.CommonName(required=True)
    title = common_fields.CommonName(required=True)


class EditNewsRequestSchema(Schema):
    category = common_fields.CommonName()
    title = common_fields.CommonName()
    body = common_fields.News()
    related_contest = fields.Integer()
