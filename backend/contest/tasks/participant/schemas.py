from marshmallow import Schema, fields
from contest.tasks.model_schemas.schemas import TaskSchema


class AllTaskSchema(Schema):
    tasks_list = fields.Nested(TaskSchema, many=True, required=True)


