import telepot

from ffsystem.bots.settings import telegram_token, CHAT_ID


class TeleBot:
    def __init__(self, token, chat_id):
        self._bot = telepot.Bot(token)
        self._chat_id = chat_id

    def send_msg(self, text, parse_mode=None):
        self._bot.sendMessage(
            chat_id=self._chat_id, text=text, parse_mode=parse_mode)


telebot_ffs_group = TeleBot(telegram_token, CHAT_ID)
