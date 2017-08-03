from uuid import uuid4
from time import sleep
import logging

import docker as libdocker
import pytest
from ffsystem.application import create_app

from ffsystem.config import CONF
from ffsystem.database import db as database

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
    # TODO: Wait container to become alive in other way.
    logger.info("Created docker container.")
    sleep(5)
    yield container
    logger.info("Shutting down container.")
    container.stop()
    container.remove()


@pytest.fixture(scope='session', autouse=True)
def flask_app(db_postgres):
    return create_app(CONF)


@pytest.fixture(scope='session', autouse=True)
def create_db(flask_app):
    with flask_app.app_context():
        database.create_all()
