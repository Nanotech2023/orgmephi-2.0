from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from user.models.reference import *


class UniversitySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = True
        sqla_session = db.session

    name = auto_field(column_name='name')


class CountrySchema(SQLAlchemySchema):
    class Meta:
        model = University
        load_instance = True
        sqla_session = db.session

    name = auto_field(column_name='name')
