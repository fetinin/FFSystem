from flask import request, jsonify

from database.enums import Roles
from database.models import User

from application import create_app
from config import CONF
from helpers import token_auth, role_required

app = create_app(CONF)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/users', methods=['POST'])
def create_user():
    from database import db
    db.create_all()
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


@app.route('/api/users', methods=['GET'])
@token_auth
@role_required(Roles.admin.value)
def show_user(user):
    users = User.query.filter_by(deleted=False)
    users_as_dicts = [user.to_dict() for user in users]
    return jsonify(users_as_dicts), 200


if __name__ == '__main__':
    app.run()
