import os
import os.path
import logging

import motor
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import handler
from handler import auth

PROJECT_ROOT = os.path.dirname(__file__)
logger = logging.getLogger(__name__)

define("port", default=8888, help="run on the given port", type=int)
define("host", default='0.0.0.0', help="run on the given host", type=str)
define("dburl", default='mongodb://localhost:27017')
define("dbname", default='motorchan')
define("debug", default=True, help="server debug mode", type=bool)
define("static_url", default="/static/", help="Static url prefix", type=str)
define("static_root", default=os.path.join(PROJECT_ROOT, "static"), help="Static files root", type=str)


class Application(tornado.web.Application):
    def __init__(self):

        logger.info("Starting application on %s:%s", options.host, options.port)
        handlers = [
            tornado.web.url(r"/", handler.MainApplicationHandler, name='main'),
            tornado.web.url(r"/api/board", handler.api.BoardAPIHandler, name='api_board'),
            tornado.web.url(r"/login", auth.LoginHandler, name='login'),
        ]

        db_client = motor.MotorClient(options.dburl).open_sync()

        settings = dict(
            debug=options.debug,
            template_path=os.path.join(PROJECT_ROOT, "templates"),
            static_path=options.static_root,
            static_url_prefix=options.static_url,
            xsrf_cookies=True,
            cookie_secret="11zKXQAGgE||22mGeJJFuYasdh11237EQnp2XdTP1o/Vo=",
            autoescape=None,
            db=db_client[options.dbname],
        )
        super(Application, self).__init__(handlers, **settings)


def run():
    logging.basicConfig(level=logging.DEBUG)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
