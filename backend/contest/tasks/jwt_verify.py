from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import abort


def jwt_required_role(roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['role'] not in roles:
                abort(403)
            return function(*args, **kwargs)
        return wrapper
    return decorator


def jwt_get_id():
    return get_jwt()['sub']


def jwt_get_role():
    return get_jwt()['role']


def jwt_get_username():
    return get_jwt()['name']