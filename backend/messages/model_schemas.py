from marshmallow import pre_load, fields
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, Related
from marshmallow_enum import EnumField

from .models import *

from common.marshmallow import check_related_existence


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
    employee = Related(column=['id'], allow_none=False, description='null if sent by the participant')
    message = auto_field(column_name='message', allow_none=False)


class ThreadSchema(SQLAlchemySchema):
    class Meta:
        model = Thread
        load_instance = True
        sqla_session = db.session

    id = auto_field(column_name='id', allow_none=False, dump_only=True)
    author = Related(column=['id'], many=False, allow_none=False)
    category = Related(column=['name'], allow_none=False)
    thread_type = EnumField(enum=ThreadType, by_value=True, allow_none=False)
    resolved = auto_field(column_name='resolved', allow_none=False)
    status = EnumField(enum=ThreadStatus, by_value=True, allow_none=False)
    post_time = auto_field(column_name='post_time', allow_none=False)
    resolve_time = auto_field(column_name='resolve_time', allow_none=True)
    topic = auto_field(column_name='topic', allow_none=False)
    messages = Nested(nested=MessageSchema, many=True, allow_none=False, dump_only=True)
    related_contest = Related(column=['contest_id'], many=False, allow_none=True)
    author_username = fields.String(allow_none=True, dump_only=True)
    author_first_name = fields.String(allow_none=True, dump_only=True)
    author_second_name = fields.String(allow_none=True, dump_only=True)
    author_middle_name = fields.String(allow_none=True, dump_only=True)

    # noinspection PyUnusedLocal
    @pre_load()
    def check_author(self, data, many, **kwargs):
        return check_related_existence(data, 'author', 'id', User)

    # noinspection PyUnusedLocal
    @pre_load()
    def check_category(self, data, many, **kwargs):
        return check_related_existence(data, 'category', 'name', ThreadCategory)

    # noinspection PyUnusedLocal
    @pre_load()
    def check_contest(self, data, many, **kwargs):
        return check_related_existence(data, 'related_contest', 'contest_id', Contest)


class ThreadInfoSchema(ThreadSchema):
    class Meta(ThreadSchema.Meta):
        exclude = ['messages']
