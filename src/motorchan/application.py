
import os
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import handler

logger = logging.getLogger(__name__)

define("port", default=8888, help="run on the given port", type=int)
define("host", default='0.0.0.0', help="run on the given host", type=str)

class Application(tornado.web.Application):
    def __init__(self):
        logger.info("Starting application on %s:%s", options.host, options.port)
        handlers = [
            tornado.web.url(r"/", handler.MainApplicationHandler, name='main'),
        ]

        settings = dict(
            debug=True,
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="11zKXQAGgE||22mGeJJFuYasdh11237EQnp2XdTP1o/Vo=",
            login_url="/auth/login",
            autoescape=None,
        )
        super(Application,self).__init__(handlers, **settings)

def run():
    logging.basicConfig(level=logging.DEBUG)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
