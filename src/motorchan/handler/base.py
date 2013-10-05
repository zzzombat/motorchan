import tornado

class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        if 'application/json' in self.request.headers.get('Content-type',""):
            self.request.json = json.loads(self.request.body)
        self.db = self.application.settings.get('db')

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get_user_locale(self):
        return tornado.locale.get('ru')
