from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField

from .models import *

from user.model_schemas.auth import UserSchema
from contest.tasks.model_schemas.schemas import ContestSchema
from contest.responses.model_schemas.schemas import ResponseSchema, AppealSchema


class ThreadCategorySchema(SQLAlchemySchema):
    class Meta:
        model = ThreadCategory
        load_instance = True
        sqla_session = db.session

    name = auto_field(column_name='name', allow_none=False)


class MessageSchema(SQLAlchemySchema):
    class Meta:
        model = Message
        load_instance = True
        sqla_session = db.session

    message_id = auto_field(column_name='id', dump_only=True, allow_none=False)
    post_time = auto_field(column_name='post_time', allow_none=False)
    from_mephi = auto_field(column_name='from_mephi', allow_none=False)
    message = auto_field(column_name='message', allow_none=False)


class ThreadSchema(SQLAlchemySchema):
    class Meta:
        model = Thread
        load_instance = True
        sqla_session = db.session

    id = auto_field(column_name='id', dump_only=True, allow_none=False)
    author = Nested(nested=UserSchema, many=False, allow_none=False)
    category_name = auto_field(column_name='category_name', allow_none=False)
    thread_type = EnumField(enum=ThreadType, by_value=True, allow_none=False)
    resolved = auto_field(column_name='resolved', allow_none=False)
    status = EnumField(enum=ThreadStatus, by_value=True, allow_none=False)
    post_time = auto_field(column_name='post_time', allow_none=False)
    resolve_time = auto_field(column_name='resolve_time', allow_none=True)
    topic = auto_field(column_name='topic', allow_none=False)
    messages = Nested(nested=MessageSchema, many=True, allow_none=False)
    related_contest = Nested(nested=ContestSchema, many=True, allow_none=True)
    related_work = Nested(nested=ResponseSchema, many=True, allow_none=True)
    related_appeal = Nested(nested=AppealSchema, many=True, allow_none=True)

