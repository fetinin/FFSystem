import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
os.environ['DATABASE_URL'] = 'postgres://xfdqzanolatrgu:3a3a901ec1c8055ae364e36537bab04b116c2d05f8e29697eeceda9355fc2ed6@ec2-107-21-99-176.compute-1.amazonaws.com:5432/d71i38071drdpm'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
