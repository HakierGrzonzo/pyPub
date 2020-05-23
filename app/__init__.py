from flask import Flask
from flaskwebgui import FlaskUI

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource

app = Flask(__name__)

from app import routes
from .routes import config, args

resource = WSGIResource(reactor, reactor.getThreadPool(), app)
site = Site(resource)

class dummyRun():
    def __init__(self, reactor):
        self.app = reactor
    def run(self, host = "", port = 5000):
        self.app.listenTCP(port, site)
        self.app.run()



ui = FlaskUI(dummyRun(reactor))