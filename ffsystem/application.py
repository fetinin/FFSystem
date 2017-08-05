import logging

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from ffsystem.config import CONF
from ffsystem.database import db
from ffsystem.routes import blueprints

__all__ = ['create_app', 'make_json_app']

logger = logging.getLogger(__name__)


def create_app(conf: dict) -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.update(conf)
    for bp in blueprints:
        flask_app.register_blueprint(bp)
    db.init_app(flask_app)

    return flask_app


def make_json_app(config: dict) -> Flask:
    """
        Creates a JSON-oriented Flask app.

        All error responses that you don't specifically
        manage yourself will have application/json content
        type, and will contain JSON like this (just an example):

        { "message": "405: Method Not Allowed" }
    """

    def make_json_error(ex):
        logger.exception("Exception: ")
        if isinstance(ex, HTTPException):
            msg = ex.description
            err_type = ex.name
            err_code = ex.code
        else:
            msg = "Undexpected error occured"
            err_type = "Exception"
            err_code = 500
        response = jsonify(message=msg, code=err_code, type=err_type)
        response.status_code = err_code
        return response

    flask_app = create_app(config)
    flask_app.register_error_handler(Exception, make_json_error)
    flask_app.handle_http_exception = make_json_error

    return flask_app


app = create_app(CONF)
json_app = make_json_app(CONF)
