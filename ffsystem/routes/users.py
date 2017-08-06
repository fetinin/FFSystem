from flask import jsonify, Blueprint
from werkzeug.exceptions import BadRequest, NotFound

from ffsystem.database.enums import Roles
from ffsystem.database.models import User
from ffsystem.helpers import token_auth, role_required, extract_json

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['POST'])
@extract_json(allowed_keys={'username', 'password', 'credit_card'})
def create_user(json_data):
    username = json_data.get('username')
    password = json_data.get('password')
    if password is None or username is None:
        raise BadRequest('Username and password are required.')
    if User.query.filter_by(username=username).first() is not None:
        raise BadRequest(f'User {username} already exist.')
    try:
        user = User(**json_data)
    except AttributeError as err:
        raise BadRequest(str(err))
    user.save()

    token = user.generate_auth_token()
    return jsonify({'username': user.username, 'token': token}), 201


@users_bp.route('/', methods=['GET'])
@token_auth
@role_required(Roles.admin.value)
def list_users():
    users = User.query.filter_by(deleted=False).all()
    users_as_dicts = [user.to_dict() for user in users]
    return jsonify(users_as_dicts), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@token_auth
@role_required(Roles.admin.value)
def get_user(user_id):
    user = User.qeury.filter_by(id=user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        raise NotFound('User not found.')


@users_bp.route('/<int:user_id>', methods=['PUT'])
@token_auth
@extract_json(allowed_keys={'password', 'credit_card'})
@role_required(Roles.admin.value)
def update_user(json_data, user_id):
    user = User.qeury.filter_by(id=user_id)
    if user:
        user.update(**json_data)
        return jsonify(user.to_dict()), 200
    else:
        raise NotFound('User not found.')


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@token_auth
@role_required(Roles.admin.value)
def update_user(user_id):
    user = User.qeury.filter_by(id=user_id)
    if user:
        user.delete()
        return jsonify(message='Success.'), 200
    else:
        raise NotFound('User not found.')
