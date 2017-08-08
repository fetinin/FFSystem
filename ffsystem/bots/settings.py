import os

try:
    from ffsystem.local_config import telegram_token, CHAT_ID
except ImportError:
    telegram_token = os.environ.get('TELEGRAM_TOKEN', 'emptiness')
    CHAT_ID = os.environ.get('CHAT_ID', None)
