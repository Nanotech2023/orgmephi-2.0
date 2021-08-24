from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_enum import EnumField

from contest.tasks.models import *
from user.models.auth import *

"""
User
"""


class UserInContestSchema(SQLAlchemySchema):
    class Meta:
        model = UserInContest
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    variant_id = auto_field(column_name='variant_id', dump_only=True)
    user_status = EnumField(UserStatusEnum, data_key='user_status', by_value=True, required=True)
    show_results_to_user = auto_field(column_name='show_results_to_user')
