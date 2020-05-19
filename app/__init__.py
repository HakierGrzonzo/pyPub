from flask import Flask
from flaskwebgui import FlaskUI

app = Flask(__name__)
ui = FlaskUI(app)

from app import routes
from .routes import config, args

