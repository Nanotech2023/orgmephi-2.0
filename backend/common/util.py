import io

import pdfkit
from flask import render_template, send_file

from .errors import NotFound, AlreadyExists
from typing import Type, Optional
from flask_sqlalchemy import Model
from sqlalchemy.orm import Session


def db_get_one_or_none(table: Type[Model], field: str, value: object):
    """
    Retrieve an object from the database, or None if object does not exist
    :param table: table class
    :param field: attribute to filter by
    :param value: value to filter by
    :return: First found instance of table, or None if nothing was found
    """
    return table.query.filter_by(**{field: value}).one_or_none()


def db_get_or_raise(table: Type[Model], field: str, value: object):
    """
    Retrieve an object from the database, or raises NotFound (returning 404 to user) if object does not exist
    :param table: table class
    :param field: attribute to filter by
    :param value: value to filter by
    :return: First found instance of table
    """
    result = db_get_one_or_none(table, field, value)
    if result is None:
        raise NotFound(field, str(value))
    return result


def db_get_list(table: Type[Model], field: str, value):
    """

    Retrieve a list of objects from the database
    :param table: table class
    :param field: attribute to filter by
    :param value: value to filter by
    :return: List of table instances that match the provided filter
    """
    return table.query.filter_by(**{field: value}).all()


def db_get_filter_all(table: Type[Model], field: str, value: str):
    """

    Retrieve objects from the database
    :param table: table class
    :param field: attribute to filter by
    :param value: value to filter by
    :return: Table instances that match the provided filter
    """
    return table.query.filter_by(**{field: value})


def db_get_all(table: Type[Model]):
    """
    Retrieve all objects from the same table of the database
    :param table: table class
    :return: List of table instances
    """
    return table.query.all()


def db_exists(db_session: Session, table: Type[Model], field: Optional[str] = None, value: Optional[object] = None,
              filters: dict[str, object] = None) -> bool:
    """
    Check if object with specified value exists
    :param db_session: database session
    :param table: table class
    :param field: attribute to filter by
    :param value: value to filter by
    :param filters: attribute_name-value dictionary
    :return: True if at least one object found, false otherwise
    """
    if filters is None:
        filters = {field: value}
    q = db_session.query(table).filter_by(**filters)
    return db_session.query(q.exists()).scalar()


def db_add_if_not_exists(db_session: Session, table: Type[Model], value, keys: Optional[list[str]]):
    def _get_filter(obj, key_list: list[str]) -> dict[str, object]:
        return {k: getattr(obj, k) for k in key_list if getattr(obj, k) is not None}

    value_filter = _get_filter(value, keys)

    if db_exists(db_session, table, filters=value_filter):
        raise AlreadyExists(f'{table.__tablename__}({value_filter.keys()})', f'({value_filter.values()})')
    db_session.add(value)


def db_populate(db_session: Session, table: Type[Model], values: list, key: Optional[str] = None,
                keys: Optional[list[str]] = None) -> None:
    """
    Populate table
    :param db_session: database session
    :param table: table class
    :param values: list of values to insert
    :param key: name of the PK field
    :param keys: list of PK field names
    """

    def _get_filter(obj, key_list: list[str]) -> dict[str, object]:
        return {k: getattr(obj, k) for k in key_list if getattr(obj, k) is not None}

    if keys is None:
        keys = [key]
    new_values = [v for v in values if not db_exists(db_session, table, filters=_get_filter(v, keys))]
    db_session.add_all(new_values)


def send_pdf(template_name_or_list, **context):
    from . import get_current_app
    template = render_template(template_name_or_list, **context)
    if get_current_app().app.testing:
        pdf = b''
    else:
        pdf = pdfkit.from_string(template, False, options={'orientation': 'landscape', 'quiet': ''})
    return send_file(io.BytesIO(pdf), 'application/pdf')
