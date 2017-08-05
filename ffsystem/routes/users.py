from flask import request, jsonify, Blueprint

from ffsystem.database.enums import Roles
from ffsystem.database.models import User
from ffsystem.helpers import token_auth, role_required
from werkzeug.exceptions import BadRequest, NotFound

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['POST'])
def create_user():
    json_data = request.get_json(silent=True) or {}
    username = json_data.get('username')
    password = json_data.get('password')
    credit_card = json_data.get('creditCard',)

    if username is None or password is None:
        raise BadRequest('Username and password are required.')
    if User.query.filter_by(username=username).first() is not None:
        raise BadRequest(f'User {username} already exist.')
    try:
        user = User(
            username=username,
            password=password,
            credit_card=credit_card,
        )
    except AttributeError as err:
        raise BadRequest(str(err))
    user.save()

    token = user.generate_auth_token()
    return jsonify({'username': user.username, 'token': token}), 201


@users_bp.route('/', methods=['GET'])
@token_auth
@role_required(Roles.admin.value)
def list_users(user):
    users = User.query.filter_by(deleted=False)
    users_as_dicts = [user.to_dict() for user in users]
    return jsonify(users_as_dicts), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@token_auth
@role_required(Roles.admin.value)
def get_user(user, user_id):
    user = User.qeury.filter_by(id=user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        raise NotFound('User not found.')
