from marshmallow import Schema, fields
from common import fields as common_fields


class CreateOlympiadTypeRequestTaskAdminSchema(Schema):
    olympiad_type = common_fields.CommonName(required=True)


class OlympiadTypeResponseTaskAdminSchema(Schema):
    olympiad_type_id = fields.Int(required=True)


class CreateOtherLocationRequestTaskAdminSchema(Schema):
    country_name = common_fields.CommonName(required=True)
    location = common_fields.FreeDescription(required=True)


class CreateOnlineLocationRequestTaskAdminSchema(Schema):
    url = common_fields.URL(required=True)


class CreateRussiaLocationRequestTaskAdminSchema(Schema):
    city_name = common_fields.CommonName(required=True)
    region_name = common_fields.CommonName(required=True)
    address = common_fields.FreeDescription(required=True)


class LocationResponseTaskAdminSchema(Schema):
    location_id = fields.Int(required=True)
