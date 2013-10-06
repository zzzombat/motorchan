# coding: utf-8
import json
import datetime

from bson.objectid import ObjectId

import fixtures
from utils import BaseTestCase


class BoardAPITestCase(BaseTestCase):

    fixtures = {
        'boards': [
            fixtures.get_random_board(slug='b'),
            fixtures.get_random_board(slug='c'),
            fixtures.get_random_board(slug='d'),
        ],
    }

    def test_board_list(self):
        response = self.client.get('/api/board/')
        self.assertTrue('application/json' in response.headers['content-type'])

        data = json.loads(response.body)['data']
        self.assertEqual(len(data), 3)
        self.assertEqual(response.code, 200)
        board_data = data[0]
        self.assertIn('_id', board_data)
        self.assertIn('name', board_data)
        self.assertIn('slug', board_data)

    def test_board_create(self):
        data = {
            'slug': 't',
            'name': 'Test',
        }
        response = self.client.post_json('/api/board/', data)
        record = self.db.boards.find_one(data)
        self.assertEqual(response.code, 201)
        self.assertNotEqual(record, None)
        self.assertEqual(self.db.boards.count(), 4)

    def test_board_slug_unique(self):
        data = {
            'slug': 'b',
            'name': 'BBB',
        }

        response = self.client.post_json('/api/board/', data)
        self.assertEqual(response.code, 400)


class ThreadAPITestCase(BaseTestCase):

    def fixtures(self):
        board = fixtures.get_random_board(post_max_id=2)
        board_2 = fixtures.get_random_board()
        return {
            'boards': [board, board_2],
            'threads': [
                fixtures.get_random_thread(board_id=board['_id'], replies_count=24),
                fixtures.get_random_thread(board_id=board['_id'], replies_count=2),
                fixtures.get_random_thread(board_id=board_2['_id'], replies_count=12),
                fixtures.get_random_thread(board_id=board_2['_id'], replies_count=0),
                fixtures.get_random_thread(board_id=board_2['_id'], replies_count=3),
            ]
        }

    def test_thread_create_fail(self):
        response = self.client.post_json('/api/thread/', {'hello': 'world'})
        self.assertEqual(response.code, 400)
        data = json.loads(response.body)
        self.assertIn('error', data)

    def test_thread_create_bad_board(self):
        req_data = {
            'name': 'Ivan',
            'email': '',
            'board_id': unicode(ObjectId()),
            'is_sage': False,
            'body': 'Test post body',
        }
        response = self.client.post_json('/api/thread/', req_data)
        self.assertEqual(response.code, 400)

    def test_thread_create_no_body(self):
        board = self.fixtures['boards'][0]
        req_data = {
            'board_id': unicode(board['_id']),
        }
        response = self.client.post_json('/api/thread/', req_data)
        self.assertEqual(response.code, 400)

    def test_thread_create_blank_body(self):
        board = self.fixtures['boards'][0]
        req_data = {
            'body': '',
            'board_id': unicode(board['_id']),
        }
        response = self.client.post_json('/api/thread/', req_data)
        self.assertEqual(response.code, 201)

    def test_thread_create(self):
        board = self.fixtures['boards'][0]
        req_data = {
            'name': 'Ivan',
            'email': '',
            'board_id': unicode(board['_id']),
            'is_sage': False,
            'body': 'Test post body',
        }

        response = self.client.post_json('/api/thread/', req_data)
        self.assertEqual(response.code, 201, response.body)

        board_record = self.db.boards.find_one({'_id': board['_id']})
        self.assertEqual(board_record['post_max_id'], 3)

        new_thread_id = ObjectId(json.loads(response.body)['_id'])
        thread_record = self.db.threads.find_one({'_id': new_thread_id})
        self.assertNotEqual(thread_record, None)
        self.assertEqual(thread_record['board_id'], board_record['_id'])
        self.assertIn('replies', thread_record)
        self.assertIn('date_created', thread_record['op'])
        self.assertIsInstance(thread_record['op']['date_created'], datetime.datetime)
        # import ipdb;ipdb.set_trace()

    def test_thread_get_list_all(self):
        response = self.client.get('/api/thread/')
        self.assertEqual(response.code, 200, response.body)
        data = json.loads(response.body)['data']
        self.assertEqual(len(data), 5)
        self.assertIn('_id', data[0])
        self.assertIn('no', data[0])
        self.assertIn('op', data[0])
        self.assertIn('replies', data[0])
        self.assertNotIn('replies_count', data[0])
        self.assertIn('date_created', data[0]['op'])
        self.assertIn('date_created', data[0]['replies'][0])

    def test_thread_get_list_limit_offset(self):
        response = self.client.get('/api/thread/?limit=2&offset=1')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body)['data']
        self.assertEqual(len(data), 2)

    def test_thread_get_list_filter_board(self):
        board = self.fixtures['boards'][0]
        response = self.client.get('/api/thread/?board_id={0}'.format(board['_id']))
        self.assertEqual(response.code, 200)
        data = json.loads(response.body)['data']
        self.assertEqual(len(data), 2)

    def test_thread_get_one(self):
        test_board_fixture = self.fixtures['boards'][0]
        test_thread_fixture = fixtures.get_random_thread(
            board_id=test_board_fixture['_id'],
            replies_count=20)
        self.db.threads.insert(test_thread_fixture)
        response = self.client.get('/api/thread/{0}/'.format(test_thread_fixture['_id']))
        self.assertEqual(response.code, 200)
        data = json.loads(response.body)['data']
        self.assertIsInstance(data, dict)
        self.assertIn('no', data)
        self.assertIn('board_id', data)
        self.assertIn('op', data)
        self.assertIn('replies', data)
        self.assertEqual(len(data['replies']), 20)

    def test_thread_get_404(self):
        response = self.client.get('/api/thread/{0}/'.format(ObjectId()))
        self.assertEqual(response.code, 404)

    # def test_thread_create_reply(self):
    #     test_thread_fixture = self.fixtures['threads'][0]
    #     reply_request_data = {
    #         'name': '',
    #         'email': '',
    #         'is_sage': False,
    #         'body': 'Hello guys',
    #     }
    #     url = '/api/thread/{0}/reply/'.format(test_thread_fixture['_id'])
    #     response = self.client.post(url, reply_request_data)
    #     self.assertEqual(response.code, 200)
