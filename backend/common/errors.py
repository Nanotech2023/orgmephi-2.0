from flask import make_response, Response
from functools import wraps
from typing import Callable


def _catch_request_error(function: Callable) -> Callable:
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except RequestError as err:
            return err.to_response()
    return wrapper


class RequestError(Exception):
    def __init__(self, http_code: int = 400):
        self.http_code = http_code

    def get_msg(self) -> str:
        return ''

    def to_response(self) -> Response:
        return make_response({"errors": [
            {
                "class": str(type(self)),
                "status": self.http_code,
                "title": self.get_msg()
            }
        ]}, self.http_code)


class AlreadyExists(RequestError):
    def __init__(self, field: str, value: str):
        super(AlreadyExists, self).__init__(409)
        self.field = field
        self.value = value

    def get_msg(self) -> str:
        return '%s "%s" already exists' % (self.field, self.value)


class NotFound(RequestError):
    def __init__(self, field: str, value: str):
        super(NotFound, self).__init__(404)
        self.field = field
        self.value = value

    def get_msg(self) -> str:
        return '%s "%s" not found' % (self.field, self.value)


class WeakPassword(RequestError):
    def __init__(self, errors):
        super(WeakPassword, self).__init__(400)
        self.errors = errors

    def get_msg(self) -> str:
        return 'Password is too weak: %s' % str(self.errors)


class WrongCredentials(RequestError):
    def __init__(self):
        super(WrongCredentials, self).__init__(401)

    def get_msg(self) -> str:
        return 'Wrong credentials'


class InsufficientData(RequestError):
    def __init__(self, obj: str, data: str):
        super(InsufficientData, self).__init__(409)
        self.obj = obj
        self.data = data

    def get_msg(self) -> str:
        return '%s is missing %s' % (self.obj, self.data)


class PermissionDenied(RequestError):
    def __init__(self, roles: list[str]):
        super(PermissionDenied, self).__init__(403)
        self.roles = roles

    def get_msg(self) -> str:
        return 'Roles %s are required to perform this action' % str(self.roles)
