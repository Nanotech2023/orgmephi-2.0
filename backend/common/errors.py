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
    """
    Base request error type, should not be raised on it's own, use child classes

    Request errors are raised when invalid or conflicting data is provided from client (normally 4xx http statuses)
    """
    def __init__(self, http_code: int = 400):
        """
        Create a request error
        :param http_code: http status code
        """
        self.http_code = http_code

    def get_msg(self) -> str:
        """
        Get error message
        :return: Error message
        """
        return ''

    def to_response(self) -> Response:
        """
        Convert error to flask response
        :return: Flask response
        """
        return make_response({"errors": [
            {
                "class": str(type(self)),
                "status": self.http_code,
                "title": self.get_msg()
            }
        ]}, self.http_code)


class AlreadyExists(RequestError):
    """
    Requested data can not be posted because a conflicting object is already posted (e.g. entity with the same value of
        a unique attribute)
    """
    def __init__(self, field: str, value: str):
        """
        Create error object
        :param field: name of the conflicting attribute
        :param value: value of the conflicting attribute
        """
        super(AlreadyExists, self).__init__(409)
        self.field = field
        self.value = value

    def get_msg(self) -> str:
        return '%s "%s" already exists' % (self.field, self.value)


class NotFound(RequestError):
    """
    Requested data is not found (e.g. id does not exist)
    """
    def __init__(self, field: str, value: str):
        """
        Create error object
        :param field: name of the searched attribute
        :param value: value of the searched attribute
        """
        super(NotFound, self).__init__(404)
        self.field = field
        self.value = value

    def get_msg(self) -> str:
        return '%s "%s" not found' % (self.field, self.value)


class WeakPassword(RequestError):
    """
    Provided password is too weak according to password policy
    """
    def __init__(self, errors):
        """
        Create error object
        :param errors: List of errors (see password_strength.PasswordPolicy)
        """
        super(WeakPassword, self).__init__(400)
        self.errors = errors

    def get_msg(self) -> str:
        return 'Password is too weak: %s' % str(self.errors)


class WrongCredentials(RequestError):
    """
    CAn not authenticate user because of non-matching credentials
    """
    def __init__(self):
        """
        Create error object
        """
        super(WrongCredentials, self).__init__(401)

    def get_msg(self) -> str:
        return 'Wrong credentials'


class InsufficientData(RequestError):
    """
    Required data was not found in the request body
    """
    def __init__(self, obj: str, data: str):
        """
        Create error object
        :param obj: what object is missing data
        :param data: what data is missing
        """
        super(InsufficientData, self).__init__(409)
        self.obj = obj
        self.data = data

    def get_msg(self) -> str:
        return '%s is missing %s' % (self.obj, self.data)


class PermissionDenied(RequestError):
    """
    User hos insufficient permissions to perform the operation
    """
    def __init__(self, roles: list[str]):
        """
        Create error object
        :param roles: List of roles that can perform the operation
        """
        super(PermissionDenied, self).__init__(403)
        self.roles = roles

    def get_msg(self) -> str:
        return 'Roles %s are required to perform this action' % str(self.roles)