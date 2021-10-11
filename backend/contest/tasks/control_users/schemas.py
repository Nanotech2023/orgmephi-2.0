from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from contest.tasks.model_schemas.user import UserInContestSchema
from contest.tasks.models.olympiad import UserStatusEnum


class UpdateUserInContestRequestTaskControlUsersSchema(Schema):
    users_id = fields.List(fields.Int(), required=True)
    location_id = fields.Int(required=False)
    show_results_to_user = fields.Boolean(required=False)
    check_condition = fields.Boolean(required=False)
    user_status = EnumField(UserStatusEnum, by_value=True, required=False)


class ChangeUsersLocationInContestRequestTaskControlUsersSchema(Schema):
    users_id = fields.List(fields.Int(), required=True)
    location_id = fields.Int(required=False)


class UsersResponseTaskControlUsersSchema(Schema):
    user_list = fields.Nested(UserInContestSchema, many=True, required=True)
