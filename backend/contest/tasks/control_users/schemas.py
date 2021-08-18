from marshmallow import Schema, fields
from common import fields as common_fields
from contest.tasks.model_schemas.schemas import UserInContestSchema


class UpdateUserInRequestCreatorSchema(Schema):
    users_id = fields.List(fields.Int(), required=True)


class UsersResponseSchema(Schema):
    user_list = fields.Nested(UserInContestSchema, many=True, required=True)


class UserCertificateSchema(Schema):
    certificate = common_fields.BytesField(required=True)


