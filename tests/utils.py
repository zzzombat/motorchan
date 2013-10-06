
import json
from pymongo import MongoClient
from motor import MotorClient
import tornado.testing
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from tornado_utils.http_test_client import TestClient, HTTPClientMixin
from motorchan.application import Application
import fixtures

TEST_DB_NAME = 'test_motorchan'


class BaseAsyncTestCase(AsyncHTTPTestCase, LogTrapTestCase):
    pass


class ExTestClient(TestClient):

    def post_json(self, url, data=None, headers=None):
        if data:
            data = json.dumps(data)
        if headers is None:
            headers = {}
        headers['Content-Type'] = 'application/json'
        return self.post(url, data, headers)


class BaseHTTPTestCase(BaseAsyncTestCase, HTTPClientMixin):

    def setUp(self):
        reload(fixtures)
        super(BaseHTTPTestCase, self).setUp()
        self.client = ExTestClient(self)


class BaseTestCase(BaseHTTPTestCase):

    fixtures = None

    def setUp(self):
        pymongo_client = MongoClient()
        pymongo_client.drop_database(TEST_DB_NAME)
        self.db = pymongo_client[TEST_DB_NAME]

        if callable(self.fixtures):
            self.fixtures = self.fixtures()

        if self.fixtures:
            for collection_name, data in self.fixtures.items():
                self.db[collection_name].insert(data)
        super(BaseTestCase, self).setUp()

    def get_app(self):
        motor_client = MotorClient().open_sync()
        return Application(motor_client[TEST_DB_NAME], xsrf_cookies=False)

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()
