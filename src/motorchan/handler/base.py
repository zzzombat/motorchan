
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def prepare(self):
        if 'application/json' in self.request.headers.get('Content-type',""):
            self.request.json = json.loads(self.request.body)

    def get_current_user(self):
        username = self.get_secure_cookie("user")
        if not username:
            return None
        if username == options.demouser:
            return pwd.getpwnam('nobody')
        return pwd.getpwnam(username)
