
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
from handler import auth, test

PROJECT_ROOT = os.path.dirname(__file__)
logger = logging.getLogger(__name__)

define("port", default=8888, help="run on the given port", type=int)
define("host", default='0.0.0.0', help="run on the given host", type=str)
define("dburl", default='mongodb://localhost:27017')
define("dbname", default='motorchan')
define("debug", default=True, help="server debug mode", type=bool)
define("static_url", default="/static/", help="Static url prefix", type=str)
define("static_root", default=os.path.join(PROJECT_ROOT, "static"),
       help="Static files root", type=str)


class Application(tornado.web.Application):

    def setup_database(self, sync_db):
        sync_db.boards.ensure_index('slug', unique=True)

    def __init__(self, db=None, xsrf_cookies=True):
        logger.info("Starting application on %s:%s", options.host, options.port)

        handlers = [
            tornado.web.url(r"/", handler.MainApplicationHandler, name='main'),
            tornado.web.url(r"/api/board[/]?", handler.api.BoardAPIHandler, name='api_board'),
            tornado.web.url(r"/api/thread[/]?", handler.api.ThreadAPIHandler, name='api_thread'),
            tornado.web.url(r"/api/thread/([\da-f]+)[/]?$", handler.api.ThreadItemAPIHandler, name='api_thread_item'),
            tornado.web.url(r"/login[/]?", auth.LoginHandler, name='login'),
            tornado.web.url(r"/logout[/]?", auth.LogoutHandler, name='logout'),
            tornado.web.url(r"/test[/]?", test.TestHandler, name='test'),
        ]

        if not db:
            db = motor.MotorClient(options.dburl).open_sync()[options.dbname]

        self.setup_database(db.connection.sync_client()[db.name])

        settings = dict(
            debug=options.debug,
            template_path=os.path.join(PROJECT_ROOT, "templates"),
            static_path=options.static_root,
            static_url_prefix=options.static_url,
            xsrf_cookies=xsrf_cookies,
            cookie_secret="11zKXQAGgE||22mGeJJFuYasdh11237EQnp2XdTP1o/Vo=",
            login_url='/login',
            autoescape=None,
            db=db,
        )
        super(Application, self).__init__(handlers, **settings)


def run():
    logging.basicConfig(level=logging.DEBUG)
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
