from .errors import NotFound
from typing import Type
from flask_sqlalchemy import Model


def db_get_one_or_none(table: Type[Model], field: str, value: object):
    return table.query.filter_by(**{field: value}).one_or_none()


def db_get_or_raise(table: Type[Model], field: str, value: object):
    result = db_get_one_or_none(table, field, value)
    if result is None:
        raise NotFound(field, str(value))
    return result


def db_get_list(table: Type[Model], field: str, value: str):
    return table.query.filter_by(**{field: value}).all()


def db_get_all(table: Type[Model]):
    return table.query.all()
