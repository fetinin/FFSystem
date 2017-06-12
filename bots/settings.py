try:
    from bots.tokens import telegram_token
except ImportError:
    telegram_token = 'non-exist'
