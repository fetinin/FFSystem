from flask import request, jsonify, Blueprint

from ffsystem.database.enums import Roles
from ffsystem.database.models import User
from ffsystem.helpers import token_auth, role_required


users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['POST'])
def create_user():
    json_data = request.get_json(silent=True) or {}
    username = json_data.get('username')
    password = json_data.get('password')
    credit_card = json_data.get('credit_card')

    if username is None or password is None:
        return jsonify({'error': 'Username and password are required.'}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': f'User {username} already exist.'}), 400
    try:
        user = User(
            username=username,
            password=password,
            credit_card=credit_card,
        )
    except AttributeError as err:
        return jsonify({'error': str(err)}), 400
    user.save()

    token = user.generate_auth_token().decode('utf-8')

    return jsonify({'username': user.username, 'token': token}), 201


@users_bp.route('/', methods=['GET'])
@token_auth
@role_required(Roles.admin.value)
def show_user(user):
    users = User.query.filter_by(deleted=False)
    users_as_dicts = [user.to_dict() for user in users]
    return jsonify(users_as_dicts), 200