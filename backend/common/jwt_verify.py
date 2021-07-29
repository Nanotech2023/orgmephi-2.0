from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required
from typing import Callable
from .errors import PermissionDenied


def jwt_required_role(roles: list[str]) -> Callable:
    def decorator(function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['role'] not in roles:
                raise PermissionDenied(roles)
            return function(*args, **kwargs)
        return wrapper
    return decorator


def jwt_get_id() -> int:
    return get_jwt()['sub']


def jwt_get_role() -> str:
    return get_jwt()['role']


def jwt_get_username() -> str:
    return get_jwt()['name']