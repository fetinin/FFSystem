import os

try:
    from ffsystem.bots import telegram_token
except ImportError:
    telegram_token = os.environ.get('TELEGRAM_TOKEN', 'non-exist')
