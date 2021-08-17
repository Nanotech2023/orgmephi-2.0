from marshmallow import Schema, fields
from contest.tasks.model_schemas.schemas import OlympiadTypeSchema, BaseContestSchema, StageSchema, ContestSchema


class AllOlympiadTypesSchema(Schema):
    olympiad_types = fields.Nested(OlympiadTypeSchema, many=True, required=True)


class AllOlympiadsSchema(Schema):
    olympiad_list = fields.Nested(ContestSchema, many=True, required=True)


class AllBaseContestSchema(Schema):
    olympiad_list = fields.Nested(BaseContestSchema, many=True, required=True)


class AllStagesSchema(Schema):
    stages_list = fields.Nested(StageSchema, many=True, required=True)
