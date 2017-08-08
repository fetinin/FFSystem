from flask import request, jsonify, Blueprint

from ffsystem.database.models import User

token_bp = Blueprint('token', __name__, url_prefix='/api/token')


@token_bp.route('/', methods=['GET'])
def get_token():
    json_data = request.get_json(silent=True) or {}
    username = json_data.get('username')
    password = json_data.get('password')
    user = User.query.filter_by(username=username).first()

    if user.verify_password(password):
        return jsonify({'token': user.generate_auth_token()}), 200
    else:
        return jsonify({'error:': 'Invalid credentials'}), 404
