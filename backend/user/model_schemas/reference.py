from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from user.models.reference import *
from common.fields import common_name_validator


class UniversitySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = False

    name = auto_field(column_name='name', validate=common_name_validator)


class CountrySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = False

    name = auto_field(column_name='name', validate=common_name_validator)
