from flask import Flask
from config import CONF

app = Flask(__name__)
app.config.update(CONF)


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
