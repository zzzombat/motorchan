# -*- coding: utf-8 -*-
import tornado
import motor

from base import BaseHandler

class LoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render('login.html', errors=None)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        user_doc = yield motor.Op(self.db.users.find_one,
                                  {'username': self.get_argument('username'),
                                   'password': self.get_argument('password')})

        if user_doc is None:
            self.render('login.html', errors='Неверный логин или пароль.')

        else:
            self.set_secure_cookie("user", self.get_argument("username"))
            self.redirect("/")


class LogoutHandler(BaseHandler):
    def get(self):
        if self.current_user is not None:
            self.clear_cookie('user')

        self.redirect("/")