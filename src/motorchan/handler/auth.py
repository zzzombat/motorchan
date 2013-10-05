from base import BaseHandler


class LoginHandler(BaseHandler):
    def get(self):
        # self.write('<html><body><form action="/login" method="post">'
        #            'Name: <input type="text" name="username">'
        #            '<input type="submit" value="Sign in">'
        #            '</form></body></html>')
        self.render('login.html')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("username"))
        self.redirect("/")
