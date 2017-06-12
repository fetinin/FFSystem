from flask import Flask, request
from bots.telegram_bot import telebot_ffs_group

app = Flask(__name__)


@app.route('/')
def hello_world():
    user_ip, host_ip = request.remote_addr, request.host
    telebot_ffs_group.send_msg(f"New connection from {user_ip} to {host_ip}")
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
