import api
from base import BaseHandler


class MainApplicationHandler(BaseHandler):
    def get(self):
        self.render("application.html")
