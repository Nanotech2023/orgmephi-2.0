from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from common.fields import text_validator
from contest.tasks.models import *
from user.models.auth import *

"""
Variant
"""


class VariantSchema(SQLAlchemySchema):
    class Meta:
        model = Variant
        load_instance = True
        sqla_session = db.session

    variant_id = auto_field(column_name='variant_id', dump_only=True)
    contest_id = auto_field(column_name='contest_id', required=False)
    variant_number = auto_field(column_name='variant_number', required=True)
    variant_description = auto_field(column_name='variant_description', validate=text_validator, required=True)
