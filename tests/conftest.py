import logging
from time import sleep
from uuid import uuid4

import docker as libdocker
import pytest
from flask import request as flask_request
from flask.testing import FlaskClient
from flask.wrappers import Response
from werkzeug.utils import cached_property
import json

from ffsystem.application import json_app as app
from ffsystem.config import CONF
from ffsystem.database import db as database
from ffsystem.database.enums import Roles
from ffsystem.database.models import User

LOG_FORMAT = "\n[%(levelname)s]%(asctime)s %(funcName)s: %(message)s"
TIME_FORMAT = "%H:%M:%S"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=TIME_FORMAT)

logger = logging.getLogger(__name__)

db_settings = {
    'POSTGRES_USER': 'docker',
    'POSTGRES_PASSWORD': 'docker',
    'POSTGRES_DB': 'docker',
    'port': 32794,
    'address': 'localhost',
}

CONF['SQLALCHEMY_DATABASE_URI'] = "postgresql://{POSTGRES_USER}:" \
                                  "{POSTGRES_PASSWORD}@{address}:{port}" \
                                  "/{POSTGRES_DB}".format(**db_settings)


class JsonResponse(Response):

    @cached_property
    def json(self):
        return json.loads(self.data)


class JsonTestClient(FlaskClient):
    def open(self, *args, **kwargs):
        if 'json' in kwargs:
            kwargs['data'] = json.dumps(kwargs.pop('json'))
            kwargs['content_type'] = 'application/json'
        return super().open(*args, **kwargs)


@pytest.yield_fixture(scope='session', autouse=True)
def db_postgres():
    docker_client = libdocker.DockerClient()
    postgres_image = docker_client.images.pull('postgres', tag='9')
    container = docker_client.containers.run(
        image=postgres_image,
        name='test-postgres-%s' % uuid4(),
        ports={'5432/tcp': db_settings['port']},
        detach=True,
        environment=db_settings,
    )
    logger.info("Created docker container.")
    # TODO: Wait for container to become alive in other way.
    sleep(5)
    yield container
    logger.info("Shutting down container.")
    container.stop()
    container.remove()


@pytest.yield_fixture(scope='session', autouse=True)
def flask_app(db_postgres):
    app.config.update(CONF)
    app.testing = True
    app.response_class = JsonResponse
    app.test_client_class = JsonTestClient
    with app.app_context():
        database.create_all()
        yield app


@pytest.fixture(scope='function')
def request():
    return flask_request


@pytest.yield_fixture
def client(flask_app):
    """
    A Flask test client.
    An instance of :class:`flask.testing.TestClient` by default.
    (Thx to pytest-flask)
    """
    with flask_app.test_client() as client:
        yield client


@pytest.yield_fixture
def user_lancer(flask_app):
    with flask_app.app_context():
        user = User(
            username='test_user',
            password='password',
            credit_card='4532954356226826'
        )
        user.save()
        user.token = user.generate_auth_token()
        user.raw_password = 'password'
        yield user
        user.delete()


@pytest.yield_fixture
def user_admin(flask_app):
    with flask_app.app_context():
        user = User(
            username='test_admin',
            password='password',
            credit_card='4532954356226826',
            role=Roles.admin.value,
        )
        user.save()
        user.token = user.generate_auth_token()
        user.raw_password = 'password'
        yield user
        user.delete()


@pytest.yield_fixture
def user_employer(flask_app):
    with flask_app.app_context():
        user = User(
            username='test_employer',
            password='password',
            credit_card='4532954356226826',
            role=Roles.employer.value,
        )
        user.save()
        user.token = user.generate_auth_token()
        user.raw_password = 'password'
        yield user
        user.delete()
