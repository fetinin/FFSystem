import os

try:
    from bots.tokens import telegram_token
except ImportError:
    telegram_token = os.environ.get('TELEGRAM_TOKEN', 'non-exist')
