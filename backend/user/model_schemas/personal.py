import enum
from marshmallow import pre_load, post_dump, fields, Schema, validate
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Related, Nested
from marshmallow_oneofschema import OneOfSchema
from user.models.personal import *
from common import fields as common_fields

from common.util import db_get_one_or_none
from common.errors import AlreadyExists, NotFound
from common.marshmallow import check_related_existence

native_country = app.config['ORGMEPHI_NATIVE_COUNTRY']


class DwellingRussiaSchema(SQLAlchemySchema):
    class Meta:
        model = DwellingRussia
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


class DwellingOtherSchema(SQLAlchemySchema):
    class Meta:
        model = DwellingOther
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


class DwellingTypeEnum(enum.Enum):
    russian = 'Russian'
    foreign = 'Foreign'


class DwellingSchema(OneOfSchema):
    type_schemas = {DwellingTypeEnum.russian.value: DwellingRussiaSchema,
                    DwellingTypeEnum.foreign.value: DwellingOtherSchema}
    type_field = "russian"
    type_field_remove = True

    class_types = {DwellingRussia: DwellingTypeEnum.russian.value,
                   DwellingOther: DwellingTypeEnum.foreign.value}

    def get_obj_type(self, obj):
        obj_type = self.class_types.get(type(obj), None)
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type

    def get_data_type(self, data):
        if data.get('country', native_country) == native_country:
            return DwellingTypeEnum.russian.value
        else:
            return DwellingTypeEnum.foreign.value


class DwellingRussiaCompatibleSchema(Schema):
    rural = fields.Boolean(required=True)
    country = common_fields.CommonName(required=True, validate=validate.OneOf([native_country]))
    region = common_fields.CommonName(required=True)
    city = common_fields.CommonName(required=True)


class DwellingOtherCompatibleSchema(Schema):
    rural = fields.Boolean(required=True)
    country = common_fields.CommonName(required=True, validate=validate.NoneOf([native_country]))
    location = common_fields.FreeDescription(required=True)


class DwellingCompatibleSchema(OneOfSchema):
    type_schemas = {DwellingTypeEnum.russian.value: DwellingRussiaCompatibleSchema,
                    DwellingTypeEnum.foreign.value: DwellingOtherCompatibleSchema}
    type_field = "russian"
    type_field_remove = True

    def get_obj_type(self, obj):
        if getattr(obj, 'country', native_country) == native_country:
            return DwellingTypeEnum.russian.value
        else:
            return DwellingTypeEnum.foreign.value

    def get_data_type(self, data):
        if data.get('country', native_country) == native_country:
            return DwellingTypeEnum.russian.value
        else:
            return DwellingTypeEnum.foreign.value


class UserInfoSchema(SQLAlchemySchema):
    class Meta:
        model = UserInfo
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    email = auto_field(attribute='email', allow_none=True)
    first_name = auto_field(column_name='first_name', allow_none=True)
    middle_name = auto_field(column_name='middle_name', allow_none=True)
    second_name = auto_field(column_name='second_name', allow_none=True)
    date_of_birth = auto_field(column_name='date_of_birth', allow_none=True)
    dwelling = Nested(nested=DwellingSchema, allow_none=False, many=False)

    # noinspection PyUnusedLocal
    @pre_load()
    def check_email(self, data, **kwargs):
        email = data.get('email', None)
        if isinstance(email, str):
            info = db_get_one_or_none(UserInfo, 'email', email)
            if info is not None:
                current_email = getattr(getattr(self, 'instance', None), 'email', None)
                if current_email != email:
                    raise AlreadyExists('user.email', email)
        return data
