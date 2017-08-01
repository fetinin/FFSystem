from uuid import uuid4

import docker as libdocker
import pytest

from application import create_app
from config import CONF
from database import db as database

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
    yield container
    container.stop()
    container.remove()


@pytest.fixture(scope='session', autouse=True)
def flask_app(db_postgres):
    return create_app(CONF)


@pytest.fixture(scope='session', autouse=True)
def create_db(flask_app):
    with flask_app.app_context():
        database.create_all()
