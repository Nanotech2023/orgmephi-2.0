from marshmallow import Schema, fields
from common import fields as common_fields
from contest.tasks.model_schemas.olympiad import ContestSchema


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


# Location
class VariantIdResponseTaskAdminSchema(Schema):
    variant_id = fields.Int(required=True)


class LocationResponseTaskAdminSchema(Schema):
    location_id = fields.Int(required=True)


class FontsResponseTasksAdminSchema(Schema):
    fonts = fields.List(fields.String)


class GetCertificateArgsTasksAdminSchema(Schema):
    user_id = fields.Int(required=True)
    contest_id = fields.Int(required=True)


class TestCertificateArgsTasksAdminSchema(Schema):
    first_name = common_fields.CommonName(required=False, load_default='Ivan')
    second_name = common_fields.CommonName(required=False, load_default='Ivanov')
    middle_name = common_fields.CommonName(required=False, load_default='Ivanovich')


# Contests with user count

class IncludeComplexQuerySchema(Schema):
    include_complex = fields.Boolean()


class ListContestsWithUserCountRequestSchema(Schema):
    contests = fields.List(fields.Nested(ContestSchema), required=True)
