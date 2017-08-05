from ffsystem.routes.users import users_bp
from ffsystem.routes.index import index_bp
from ffsystem.routes.token import token_bp


blueprints = [
    users_bp,
    index_bp,
    token_bp,
]
