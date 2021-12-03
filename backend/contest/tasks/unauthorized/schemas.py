from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from contest.tasks.model_schemas.location import OlympiadLocationSchema
from contest.tasks.model_schemas.olympiad import OlympiadTypeSchema, ContestSchema, BaseContestSchema, \
    SimpleContestSchema, TargetClassSchema, StageSchema


# Olympiad type
from contest.tasks.models import ContestTypeEnum


class AllOlympiadTypesResponseTaskUnauthorizedSchema(Schema):
    olympiad_types = fields.Nested(OlympiadTypeSchema, many=True, required=True)


# Location


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


# Olympiads


class AllOlympiadsResponseTaskUnauthorizedSchema(Schema):
    contest_list = fields.Nested(ContestSchema, many=True, required=True)


# Base contest


class AllBaseContestResponseTaskUnauthorizedSchema(Schema):
    olympiad_list = fields.Nested(BaseContestSchema, many=True, required=True)


# Stage


class AllStagesResponseTaskUnauthorizedSchema(Schema):
    stages_list = fields.Nested(StageSchema, many=True, required=True)


# Target classes


class AllTargetClassesRequestTaskUnauthorizedSchema(Schema):
    target_classes = fields.Nested(TargetClassSchema, many=True, required=True)


# For filter query


class FilterSimpleContestResponseSchema(Schema):
    contest_list = fields.Nested(nested=ContestSchema, many=True)
    count = fields.Integer()


class FilterOlympiadAllRequestSchema(Schema):
    base_contest_id = fields.Integer()
    location_id = fields.Integer()
    target_classes = fields.Nested(TargetClassSchema, many=True, required=False)
    end_date = fields.DateTime()
    academic_year = fields.Integer()
    only_count = fields.Boolean()
    offset = fields.Integer()
    limit = fields.Integer()
    composite_type = EnumField(ContestTypeEnum, data_key='composite_type', by_value=True, required=False)
