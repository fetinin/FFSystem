import functools

from flask import request
from werkzeug.exceptions import Unauthorized, Forbidden

from ffsystem.database.models import User


def token_auth(func):
    """
    Decorator that adds token verification and
    puts user into route function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token', '')
        user = User.get_by_auth_token(token)
        if not user:
            raise Unauthorized("Invalid token.")
        return func(user, *args, **kwargs)

    return wrapper


def role_required(*allowed_roles):
    """Decorator for user role validation"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('token', '')
            user = User.get_by_auth_token(token)
            if user.role.value not in allowed_roles:
                raise Forbidden("You don't have proper role.")
            return func(*args, **kwargs)

        return wrapper

    return decorator
