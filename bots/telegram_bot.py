import telepot

from bots.settings import telegram_token

CHAT_ID = '-155062201'


class TeleBot:

    def __init__(self, token, chat_id):
        self._bot = telepot.Bot(token)
        self._chat_id = chat_id

    def send_message(self, text):
        self._bot.sendMessage(chat_id=self._chat_id, text=text)

telebot_ffs_group = TeleBot(telegram_token, CHAT_ID)
