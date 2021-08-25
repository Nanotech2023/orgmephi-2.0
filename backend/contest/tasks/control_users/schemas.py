from marshmallow import Schema, fields
from common import fields as common_fields
from contest.tasks.model_schemas.user import UserInContestSchema


class UpdateUserInContestRequestTaskControlUsersSchema(Schema):
    users_id = fields.List(fields.Int(), required=True)
    location_id = fields.Int(required=False)
    show_results_to_user = fields.Boolean(required=True)


class ChangeUsersLocationInContestRequestTaskControlUsersSchema(Schema):
    users_id = fields.List(fields.Int(), required=True)
    location_id = fields.Int(required=False)


class UsersResponseTaskControlUsersSchema(Schema):
    user_list = fields.Nested(UserInContestSchema, many=True, required=True)


class UserCertificateResponseTaskControlUsersSchema(Schema):
    certificate = common_fields.Text(required=True)


