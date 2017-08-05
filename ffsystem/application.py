from flask import Flask

from ffsystem.config import CONF
from ffsystem.database import db
from ffsystem.routes import blueprints


def create_app(conf: dict) -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.update(conf)
    for bp in blueprints:
        flask_app.register_blueprint(bp)
    db.init_app(flask_app)

    return flask_app

app = create_app(CONF)
