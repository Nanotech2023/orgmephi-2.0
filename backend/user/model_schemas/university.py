from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import pre_load, post_dump
from user.models.university import *
from common.fields import *


class StudentInfoSchema(SQLAlchemySchema):
    class Meta:
        model = StudentInfo
        load_instance = True

    user_id = auto_field(column_name='user_id', dump_only=True)
    phone = auto_field(column_name='phone', validate=phone_validator, nullable=True)

    university = auto_field(column_name='custom_university', validate=common_name_validator, nullable=True)
    university_id = auto_field(column_name='university', nullable=True,
                               description="Framework-specific, ignored on request and never set on on response")

    admission_year = auto_field(column_name='admission_year', nullable=True)

    university_country = fields.Str(validate=common_name_validator, nullable=True)
    university_country_id = auto_field(column_name='university_country_id', nullable=True,
                                       description="Framework-specific, "
                                                   "ignored on request and never set on on response")

    citizenship = fields.Str(validate=common_name_validator, nullable=True)
    citizenship_country_id = auto_field(column_name='citizenship_country_id', nullable=True,
                                        description="Framework-specific, "
                                                    "ignored on request and never set on on response")

    region = auto_field(column_name='region', validate=common_name_validator, nullable=True)
    city = auto_field(column_name='city', validate=common_name_validator, nullable=True)

    @pre_load()
    def get_university(self, data, many, **kwargs):
        from common.util import db_get_one_or_none
        uni_name = data.get('university', None)
        if uni_name is not None:
            uni_known = db_get_one_or_none(University, 'name', uni_name)
            if uni_known is not None:
                data['university_id'] = uni_known.id
                data['university'] = None
            else:
                data['university_id'] = None
                data['university'] = uni_name
        elif 'university' in data:
            data['university_id'] = None
            data['university'] = None
        return data

    @post_dump()
    def put_university(self, data, many, **kwargs):
        from common.util import db_get_one_or_none
        uni_known = data.pop('university_id', None)
        if uni_known is not None:
            uni = db_get_one_or_none(University, 'id', uni_known.id)
            data['university'] = uni.name
        else:
            data['university'] = None
        return data

    @pre_load()
    def get_university_country(self, data, many, **kwargs):
        from common.util import db_get_or_raise
        if 'university_country' in data:
            country_name = data.pop('university_country')
            if country_name is not None:
                country = db_get_or_raise(Country, 'name', country_name)
                data['university_country_id'] = country.id
            else:
                data['university_country_id'] = None
        return data

    @post_dump()
    def put_university_country(self, data, many, **kwargs):
        from common.util import db_get_one_or_none
        country_id = data.pop('university_country_id', None)
        if country_id is not None:
            country = db_get_one_or_none(Country, 'id', country_id)
            data['university_country'] = country.name
        else:
            data['university_country'] = None
        return data

    @pre_load()
    def get_citizenship(self, data, many, **kwargs):
        from common.util import db_get_or_raise
        country_name = data.pop('citizenship', None)
        if country_name is not None:
            country = db_get_or_raise(Country, 'name', country_name)
            data['citizenship_country_id'] = country.id
        return data

    @post_dump()
    def put_citizenship(self, data, many, **kwargs):
        from common.util import db_get_or_raise
        if 'citizenship' in data:
            country_name = data.pop('citizenship')
            if country_name is not None:
                country = db_get_or_raise(Country, 'name', country_name)
                data['citizenship_country_id'] = country.id
            else:
                data['citizenship_country_id'] = None
        return data
