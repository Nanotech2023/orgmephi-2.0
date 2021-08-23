from marshmallow import Schema, fields
from common import fields as common_fields


class AnswersInTaskRequestTaskParticipantSchema(Schema):
    answer = common_fields.Text(required=True)


class TaskForUserResponseTaskParticipantSchema(Schema):
    task_id = fields.Integer(required=True)
    answers = fields.List(fields.Nested(AnswersInTaskRequestTaskParticipantSchema), required=False)


class AllTaskResponseTaskParticipantSchema(Schema):
    tasks_list = fields.Nested(TaskForUserResponseTaskParticipantSchema, many=True, required=True)


