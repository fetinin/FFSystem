import functools

from flask import request, g
from werkzeug.exceptions import Unauthorized, Forbidden, BadRequest

from ffsystem.database.models import User
import re


def token_auth(func):
    """
    Decorator that adds token verification and
    puts user into route function. Adds user to g object.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token', '')
        user = User.get_by_auth_token(token)
        if not user:
            raise Unauthorized("Invalid token.")
        g.user = user
        return func(*args, **kwargs)

    return wrapper


def role_required(*allowed_roles):
    """Decorator for user role validation"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not getattr(g, 'user', None):
                token = request.headers.get('token', '')
                user = User.get_by_auth_token(token)
            else:
                user = g.user
            if user.role.value not in allowed_roles:
                raise Forbidden("You don't have proper role.")
            return func(*args, **kwargs)

        return wrapper

    return decorator


def extract_json(allowed_keys=None):
    """
    Decorator that extracts json from request and checks that it
    contains only allowed keys. Pass parsed json into function kwargs.
    """

    if not allowed_keys:
        allowed_keys = set()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal allowed_keys
            json = request.get_json(silent=True) or {}
            if not json:
                raise BadRequest("Request must contain valid JSON.")
            if not isinstance(json, dict):
                raise BadRequest("JSON map expected.")
            json = convert_keys_to_snake(json)
            check_for_not_allowed_keys(json, allowed_keys)

            kwargs['json_data'] = json
            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_for_not_allowed_keys(json_data: dict, allowed_keys: set) -> None:
    for v in json_data.items():
        if isinstance(v, dict):
            check_for_not_allowed_keys(v, allowed_keys)
    forbidden_keys = json_data.keys() - allowed_keys
    if forbidden_keys:
        raise BadRequest("The following items are not allowed: "
                         + ", ".join(forbidden_keys))


def camel2snake(word: str) -> str:
    subbed = _underscorer1.sub(r'\1_\2', word)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def snake2camel(word: str) -> str:
    parts = word.split('_')
    return parts[0] + ''.join(l.title() for l in parts[1:])


def convert_keys_to_snake(d: dict) -> dict:
    return {camel2snake(k): v for k, v in d.items()}

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')


def format_dict_diff(old_dict: dict, updated_values: dict) -> dict(tuple()):
    """
    Represent value diff between two dicts.

    Example output: ["key1: oldValue -> newValue", "name: John -> Kenny"]
    """
    return [
        f"{str(key).title()}: {old_dict[key]} -> {updated_values[key]}"
        for key in updated_values.keys()
    ]
