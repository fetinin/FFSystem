import functools

from flask import request, jsonify

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
            return jsonify({'error': 'Invalid token.'}), 404
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
                return jsonify({"error": "You don't have proper role."}), 403
            return func(*args, **kwargs)

        return wrapper
    return decorator
