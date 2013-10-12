
import json
import inspect
import tornado
import jsonschema
from bson.objectid import ObjectId
from docutils.core import publish_string


def json_serialize_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return unicode(obj)
    else:
        raise TypeError(
            'Object of type {0} with value of {1} '
            'is not JSON serializable'.format(type(obj), repr(obj)))


class BaseHandler(tornado.web.RequestHandler):

    allow_options = False

    def prepare(self):
        if 'application/json' in self.request.headers.get('Content-type', ""):
            self.request.json = json.loads(self.request.body)
        self.db = self.settings.get('db')

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def write(self, chunk):
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk, default=json_serialize_handler)
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        super(BaseHandler, self).write(chunk)

    def get_user_locale(self):
        return tornado.locale.get('ru')

    def options(self, *args, **kwargs):
        if not self.allow_options:
            raise tornado.web.HTTPError(405)

        html = publish_string(inspect.getdoc(self), writer_name='html')
        self.write(html)

    def _handle_request_exception(self, exc):
        if isinstance(exc, jsonschema.ValidationError):
            self.set_status(400)
            self.write({
                'error': unicode(exc),
            })
            return self.finish()
        return super(BaseHandler, self)._handle_request_exception(exc)
