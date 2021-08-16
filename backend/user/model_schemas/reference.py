from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields

from user.models.reference import *


class UniversitySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = False
        sqla_session = db.session

    name = auto_field(column_name='name')
    country = fields.Related(column=['name'], required=True)


class CountrySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = False
        sqla_session = db.session

    name = auto_field(column_name='name')


class RegionSchema(SQLAlchemySchema):
    class Meta:
        model = Region
        load_instance = False
        sqla_session = db.session

    name = auto_field(column_name='name', required=True)


class CitySchema(SQLAlchemySchema):
    class Meta:
        model = City
        load_instance = False
        sqla_session = db.session

    name = auto_field(column_name='name', required=True)
    region = fields.Related(column=['name'], required=True)
