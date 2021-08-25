from marshmallow import Schema, fields

from contest.tasks.model_schemas.contest import StageSchema
from contest.tasks.model_schemas.location import OlympiadLocationSchema
from contest.tasks.model_schemas.olympiad import OlympiadTypeSchema, ContestSchema, BaseContestSchema, \
    SimpleContestSchema


class AllOlympiadTypesResponseTaskUnauthorizedSchema(Schema):
    olympiad_types = fields.Nested(OlympiadTypeSchema, many=True, required=True)


class AllLocationResponseTaskUnauthorizedSchema(Schema):
    locations = fields.Nested(OlympiadLocationSchema, many=True, required=True)


class LocationResponseTaskUnauthorizedSchema(Schema):
    location_id = fields.Int(required=False)
    url = fields.String(required=False)
    country_name = fields.String(required=False)
    location = fields.String(required=False)
    city_name = fields.String(required=False)
    address = fields.String(required=False)
    region_name = fields.String(required=False)


class AllOlympiadsResponseTaskUnauthorizedSchema(Schema):
    contest_list = fields.Nested(ContestSchema, many=True, required=True)


class AllBaseContestResponseTaskUnauthorizedSchema(Schema):
    olympiad_list = fields.Nested(BaseContestSchema, many=True, required=True)


class AllStagesResponseTaskUnauthorizedSchema(Schema):
    stages_list = fields.Nested(StageSchema, many=True, required=True)


class FilterSimpleContestResponseSchema(Schema):
    contest_list = fields.Nested(nested=SimpleContestSchema, many=True)
    count = fields.Integer()
