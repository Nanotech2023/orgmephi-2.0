from marshmallow import pre_load
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested, Related

from common.marshmallow import check_related_existence

from .models import *


class NewsCategorySchema(SQLAlchemySchema):
    class Meta:
        model = NewsCategory
        load_instance = True
        sqla_session = db.session

    name = auto_field(column_name='name', allow_none=False)


class NewsSchema(SQLAlchemySchema):
    class Meta:
        model = News
        load_instance = True
        sqla_session = db.session

    id = auto_field(column_name='id', allow_none=False, dump_only=True)
    category = Related(column=['name'], allow_none=False)
    post_time = auto_field(column_name='post_time', allow_none=False)
    title = auto_field(column_name='title', allow_none=False)
    body = auto_field(column_name='body', allow_none=False)
    related_contest = Related(column=['contest_id'], many=False, allow_none=True)

    # noinspection PyUnusedLocal
    @pre_load()
    def check_contest(self, data, many, **kwargs):
        return check_related_existence(data, 'related_contest', 'contest_id', Contest)
