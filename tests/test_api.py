# coding: utf-8
import json
from bson.objectid import ObjectId
from pymongo import MongoClient
from motor import MotorClient
import tornado.testing
from tornado_utils.http_test_client import TestClient, HTTPClientMixin

from motorchan.application import Application

import fixtures

TEST_DB_NAME = 'test_motorchan'


class BaseAsyncTestCase(tornado.testing.AsyncHTTPTestCase, tornado.testing.LogTrapTestCase):
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
       super(BaseHTTPTestCase, self).setUp()
       self.client = ExTestClient(self)


class BaseTestCase(BaseHTTPTestCase):

    def get_app(self):
        pymongo_client = MongoClient()
        pymongo_client.drop_database(TEST_DB_NAME)
        self.db = pymongo_client[TEST_DB_NAME]
        fixtures.setup(self.db)

        motor_client = MotorClient().open_sync()
        return Application(motor_client[TEST_DB_NAME], xsrf_cookies=False)

    def get_new_ioloop(self):
        return tornado.ioloop.IOLoop.instance()



class BoardAPITestCase(BaseTestCase):

    def test_board_list(self):
        response = self.client.get('/api/board/')
        self.assertTrue('application/json' in response.headers['content-type'])

        data = json.loads(response.body)['data']
        self.assertEqual(len(data), 3)
        self.assertEqual(response.code, 200)

    def test_board_create(self):
        data = {
            'slug': 't',
            'name': 'Test',
        }
        response = self.client.post_json('/api/board/', data)
        record = self.db.boards.find_one(data)
        self.assertEqual(response.code, 201)
        self.assertNotEqual(record, None)


class ThreadAPITestCase(BaseTestCase):

    def test_thread_create(self):
        board = self.db.boards.find_one()
        req_data = {
            'name': 'Ivan',
            'email': '',
            'board_id': unicode(board['_id']),
            'is_sage': False,
            'parent_id': '',
            'body': 'Test post body',
        }
        response = self.client.post_json('/api/thread/', req_data)
        self.assertEqual(response.code, 201)

        board_record = self.db.boards.find_one({'_id': board['_id']})
        self.assertEqual(board_record['post_max_id'], 1)

        new_thread_id = ObjectId(json.loads(response.body)['id'])
        thread_record = self.db.threads.find_one({'_id': new_thread_id})
        self.assertNotEqual(thread_record, None)
        self.assertEqual(thread_record['board_id'], board_record['_id'])

    def test_thread_get_list(self):
        response = self.client.get('/api/thread/')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body)['data']

