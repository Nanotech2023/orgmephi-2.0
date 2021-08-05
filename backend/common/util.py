from .errors import NotFound
from typing import Type
from flask_sqlalchemy import Model


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


def db_get_list(table: Type[Model], field: str, value: str):
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
