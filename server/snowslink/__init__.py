# coding=utf-8

from flask import Flask
from flask.ext.login import LoginManager
from mongoengine import connect
from flask_wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth
import os

# App
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
if os.environ.get('SNOWSLINK_PRODUCTION') is not None:
    app.config.from_pyfile('config.py')

# CSRF Protect
csrf = CsrfProtect()
csrf.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# MongoDB
connect(app.config['DB_NAME'])

# OAuth
oauth = OAuth(app)
github = oauth.remote_app(
    'github',
    consumer_key=app.config['GITHUB_CLIENT_ID'],
    consumer_secret=app.config['GITHUB_CLIENT_SECRET'],
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)
