from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Related
from common import fields as common_fields

from user.models.reference import *


class UniversitySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = False
        sqla_session = db.session

    name = common_fields.CommonName()
    country = Related(column=['name'], required=True)


class CountrySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = False
        sqla_session = db.session

    name = common_fields.CommonName(required=True)


class RegionSchema(SQLAlchemySchema):
    class Meta:
        model = Region
        load_instance = False
        sqla_session = db.session

    name = common_fields.CommonName(required=True)


class CitySchema(SQLAlchemySchema):
    class Meta:
        model = City
        load_instance = False
        sqla_session = db.session

    name = common_fields.CommonName(required=True)
    region = Related(column=['name'], required=True)
