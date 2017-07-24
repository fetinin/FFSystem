import os
from collections import ChainMap

try:
    from local_config import CONFIG as LOCAL_CONF
except ImportError:
    LOCAL_CONF = {}

CONF = {
    "DEBUG": False,
    "SECRET_KEY": os.environ.get('SECRET_KEY'),
    "SQLALCHEMY_DATABASE_URI": os.environ.get('DATABASE_URL'),
}

CONF = ChainMap(LOCAL_CONF, CONF)
