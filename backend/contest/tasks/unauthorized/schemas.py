from marshmallow import Schema, fields

from contest.tasks.model_schemas.contest import StageSchema
from contest.tasks.model_schemas.olympiad import OlympiadTypeSchema, OlympiadLocationSchema, ContestSchema, BaseContestSchema


class AllOlympiadTypesResponseTaskUnauthorizedSchema(Schema):
    olympiad_types = fields.Nested(OlympiadTypeSchema, many=True, required=True)


class AllLocationResponseTaskUnauthorizedSchema(Schema):
    locations = fields.Nested(OlympiadLocationSchema, many=True, required=True)


class AllOlympiadsResponseTaskUnauthorizedSchema(Schema):
    contest_list = fields.Nested(ContestSchema, many=True, required=True)


class AllBaseContestResponseTaskUnauthorizedSchema(Schema):
    olympiad_list = fields.Nested(BaseContestSchema, many=True, required=True)


class AllStagesResponseTaskUnauthorizedSchema(Schema):
    stages_list = fields.Nested(StageSchema, many=True, required=True)
