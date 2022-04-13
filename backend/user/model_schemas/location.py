import enum
from marshmallow import pre_load, fields, validate
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy.fields import Related
from marshmallow_oneofschema import OneOfSchema
from marshmallow_enum import EnumField

from common import fields as common_fields
from common.errors import NotFound
from common.marshmallow import check_related_existence

from user.models.location import *


native_country = app.config['ORGMEPHI_NATIVE_COUNTRY']


class LocationTypeEnum(enum.Enum):
    russian = 'Russian'
    foreign = 'Foreign'


class LocationRussiaSchema(SQLAlchemySchema):
    class Meta:
        model = LocationRussia
        load_instance = True
        sqla_session = db.session

    rural = fields.Boolean(column_name='rural')
    location_type = EnumField(LocationTypeEnum, by_value=True, validate=validate.OneOf([LocationTypeEnum.russian]))
    country = common_fields.CommonName(required=True, validate=validate.OneOf([native_country]))
    city = Related(column=['name', 'region_name'])

    # noinspection PyUnusedLocal
    @pre_load()
    def check_city(self, data, many, **kwargs):
        city = data.get('city', None)
        if isinstance(city, dict):
            city_name = city.get('name', None)
            region_name = city.get('region_name', None)
        elif city is None:
            return data
        else:
            city_name = city
            region_name = data.pop('region', None)
            data['city'] = {'name': city_name, 'region_name': region_name}
        city_obj = City.query.filter_by(name=city_name, region_name=region_name).one_or_none()
        if city_obj is None:
            raise NotFound('city(name, region_name)', f'({city_name}, {region_name})')
        return data


class LocationOtherSchema(SQLAlchemySchema):
    class Meta:
        model = LocationOther
        load_instance = True
        sqla_session = db.session

    rural = fields.Boolean(column_name='rural')
    location_type = EnumField(LocationTypeEnum, by_value=True, validate=validate.OneOf([LocationTypeEnum.foreign]))
    country = Related(column=['name'], required=True)
    location = common_fields.FreeDescription(column_name='location')

    # noinspection PyUnusedLocal
    @pre_load()
    def check_country(self, data, many, **kwargs):
        return check_related_existence(data, 'country', 'name', Country)


class LocationSchema(OneOfSchema):
    type_schemas = {LocationTypeEnum.russian.value: LocationRussiaSchema,
                    LocationTypeEnum.foreign.value: LocationOtherSchema}
    type_field = "location_type"
    type_field_remove = True

    class_types = {LocationRussia: LocationTypeEnum.russian.value,
                   LocationOther: LocationTypeEnum.foreign.value}

    def get_obj_type(self, obj):
        obj_type = self.class_types.get(type(obj), None)
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type

    def get_data_type(self, data):
        if self.type_field_remove:
            type_field = data.pop(self.type_field, None)
        else:
            type_field = data.get(self.type_field, None)
        if type_field is None:
            country_name = data.get('country')
            if country_name == native_country:
                return LocationTypeEnum.russian.value
            else:
                return LocationTypeEnum.foreign.value
        else:
            return type_field
