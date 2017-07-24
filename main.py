from flask import request, jsonify, url_for, abort
from database.models import User

from application import create_app
from config import CONF

app = create_app(CONF)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/users', methods=['POST'])
def new_user():
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

if __name__ == '__main__':
    app.run()
