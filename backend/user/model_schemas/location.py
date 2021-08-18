import enum
from marshmallow import pre_load, post_dump, fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Related
from marshmallow_oneofschema import OneOfSchema
from user.models.location import *
from common import fields as common_fields

from common.errors import NotFound
from common.marshmallow import check_related_existence


native_country = app.config['ORGMEPHI_NATIVE_COUNTRY']


class LocationRussiaSchema(SQLAlchemySchema):
    class Meta:
        model = LocationRussia
        load_instance = True
        sqla_session = db.session

    rural = auto_field(column_name='rural')
    russian = fields.String(dump_only=True)
    country = fields.String(dump_only=True, required=True)
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

    # noinspection PyUnusedLocal
    @post_dump()
    def fill_country(self, data, many, **kwargs):
        data['country'] = native_country
        return data

    # noinspection PyUnusedLocal
    @pre_load()
    def pop_country(self, data, many, **kwargs):
        data.pop('country', None)
        return data


class LocationOtherSchema(SQLAlchemySchema):
    class Meta:
        model = LocationOther
        load_instance = True
        sqla_session = db.session

    rural = auto_field(column_name='rural')
    russian = fields.String(dump_only=True)
    country = Related(column=['name'], required=True)
    location = auto_field(column_name='location')

    # noinspection PyUnusedLocal
    @pre_load()
    def check_country(self, data, many, **kwargs):
        return check_related_existence(data, 'country', 'name', Country)


class LocationTypeEnum(enum.Enum):
    russian = 'Russian'
    foreign = 'Foreign'


class LocationSchema(OneOfSchema):
    type_schemas = {LocationTypeEnum.russian.value: LocationRussiaSchema,
                    LocationTypeEnum.foreign.value: LocationOtherSchema}
    type_field = "russian"
    type_field_remove = True

    class_types = {LocationRussia: LocationTypeEnum.russian.value,
                   LocationOther: LocationTypeEnum.foreign.value}

    def get_obj_type(self, obj):
        obj_type = self.class_types.get(type(obj), None)
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type

    def get_data_type(self, data):
        if data.get('country', native_country) == native_country:
            return LocationTypeEnum.russian.value
        else:
            return LocationTypeEnum.foreign.value


class LocationRussiaCompatibleSchema(Schema):
    rural = fields.Boolean(required=True)
    country = common_fields.CommonName(required=True, validate=validate.OneOf([native_country]))
    region = common_fields.CommonName(required=True)
    city = common_fields.CommonName(required=True)


class LocationOtherCompatibleSchema(Schema):
    rural = fields.Boolean(required=True)
    country = common_fields.CommonName(required=True, validate=validate.NoneOf([native_country]))
    location = common_fields.FreeDescription(required=True)


class LocationCompatibleSchema(OneOfSchema):
    type_schemas = {LocationTypeEnum.russian.value: LocationRussiaCompatibleSchema,
                    LocationTypeEnum.foreign.value: LocationOtherCompatibleSchema}
    type_field = "russian"
    type_field_remove = True

    def get_obj_type(self, obj):
        if getattr(obj, 'country', native_country) == native_country:
            return LocationTypeEnum.russian.value
        else:
            return LocationTypeEnum.foreign.value

    def get_data_type(self, data):
        if data.get('country', native_country) == native_country:
            return LocationTypeEnum.russian.value
        else:
            return LocationTypeEnum.foreign.value
