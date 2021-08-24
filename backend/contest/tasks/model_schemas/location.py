from marshmallow_oneofschema import OneOfSchema
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from common.fields import location_validator
from contest.tasks.models import *
from user.models.auth import *

"""
Location
"""


class OnlineOlympiadLocationSchema(SQLAlchemySchema):
    class Meta:
        model = OnlineOlympiadLocation
        load_instance = True
        sqla_session = db.session

    location_id = auto_field(column_name='location_id', dump_only=True)
    url = auto_field(column_name='url', required=True)


class RussiaOlympiadLocationSchema(SQLAlchemySchema):
    class Meta:
        model = RussiaOlympiadLocation
        load_instance = True
        sqla_session = db.session

    location_id = auto_field(column_name='location_id', dump_only=True)
    city_name = auto_field(column_name='city_name', required=True)
    region_name = auto_field(column_name='region_name', required=True)
    address = auto_field(column_name='address', required=True)


class OtherOlympiadLocationSchema(SQLAlchemySchema):
    class Meta:
        model = OtherOlympiadLocation
        load_instance = True
        sqla_session = db.session

    location_id = auto_field(column_name='location_id', dump_only=True)
    country_name = auto_field(column_name='country_name', required=True)
    location = auto_field(column_name='location', required=True)


class OlympiadLocationSchema(OneOfSchema):
    type_schemas = {
        LocationEnum.OnlineOlympiadLocation.value: OnlineOlympiadLocationSchema,
        LocationEnum.RussiaOlympiadLocation.value: RussiaOlympiadLocationSchema,
        LocationEnum.OtherOlympiadLocation.value: OtherOlympiadLocationSchema
    }
    type_field = "location_type"
    type_field_remove = True

    class_types = {
        OnlineOlympiadLocationSchema: LocationEnum.OnlineOlympiadLocation.value,
        OtherOlympiadLocationSchema: LocationEnum.RussiaOlympiadLocation.value,
        RussiaOlympiadLocationSchema: LocationEnum.OtherOlympiadLocation.value,
    }

    def get_obj_type(self, obj):
        obj_type = obj.location_type
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type.value
