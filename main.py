# -*- coding: utf-8 -*-

"""

Author: Y.Han Lee

"""

import os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from app import create_app
from app.config import config


cfg = config[os.getenv("SERVER_TYPE", "default")]
flask_app = create_app(cfg)
http_server = HTTPServer(WSGIContainer(flask_app))
http_server.listen(int(os.getenv("SERVER_PORT", 5000)))
IOLoop.instance().start()
