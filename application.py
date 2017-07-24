from flask import Flask
from database import db


def create_app(conf: dict) -> Flask:
    app = Flask(__name__)
    app.config.update(conf)

    db.init_app(app)

    return app
