from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required
from typing import Callable
from .errors import PermissionDenied


def jwt_required_role(roles: list[str], refresh: bool = False) -> Callable:
    """
    Decorator factory to set permissions on some operations

    Normally this decorator is automatically applied by OrgMephiModule

    Set access_level argument of OrgMephiModule to None and use this decorator to apply permissions per view rather than
        per module

    :param roles: List of accepted roles
    :param refresh: if True checks refresh
    :return: decorator
    """
    def decorator(function: Callable) -> Callable:
        """
        Decorator factory to set permissions on some operations
        :param function: function to wrap
        :return: wrapped function
        """
        @wraps(function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request(refresh=refresh)
            claims = get_jwt()
            if claims['role'] not in roles:
                raise PermissionDenied(roles)
            return function(*args, **kwargs)
        return wrapper
    return decorator


def jwt_get_id() -> int:
    """
    Get id of the authenticated user
    :return: ID of the current user
    """
    return get_jwt().get('sub', None)


def jwt_get_role() -> str:
    """
    Get role of the authenticated user
    :return: Role of the current user
    """
    return get_jwt().get('role', None)


def jwt_get_username() -> str:
    """
    Get username of the authenticated user
    :return: Username of the current user
    """
    return get_jwt().get('name', None)
