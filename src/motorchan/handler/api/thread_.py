
import datetime
import dateutil.tz
import tornado.web
from bson.objectid import ObjectId
from motorchan.handler.base import BaseHandler

import schema


def utc_now():
    return datetime.datetime.now(dateutil.tz.tzutc())


class ThreadAPIHandler(BaseHandler):

    @tornado.web.asynchronous
    def get(self):
        find_args = {
            'spec': {},
            'limit': 200,
            'skip': 0,
        }

        board_id = self.get_argument('board_id', None)
        if board_id:
            find_args['spec']['board_id'] = ObjectId(board_id)

        limit = self.get_argument('limit', None)
        if limit:
            find_args['limit'] = int(limit)

        offset = self.get_argument('offset', None)
        if offset:
            find_args['skip'] = int(offset)

        self.db.threads.find(**find_args).to_list(callback=self._on_thread_list_fetched)

    def _on_thread_list_fetched(self, threads, error):
        self.write({"data": threads})
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        schema.Post.validate(self.request.json)
        self.db.boards.find_and_modify(
            query={'_id': ObjectId(self.request.json['board_id'])},
            update={'$inc': {'post_max_id': 1}},
            callback=self._on_board_fetched,
        )

    def _on_board_fetched(self, board, error):
        if not board:
            self.set_status(400)
            self.write({'error': 'Board not found'})
            return self.finish()

        post = self.request.json
        post['date_created'] = utc_now()
        thread = {
            'no': board['post_max_id'] + 1,
            'board_id': board['_id'],
            'op': post,
            'replies': [],
        }
        self.db.threads.insert(thread, callback=self._on_thread_inserted)

    def _on_thread_inserted(self, obj_id, error):
        self.set_status(201)
        self.write({'_id': obj_id})
        self.finish()


class ThreadItemAPIHandler(BaseHandler):

    def _on_thread_fetched(self, thread, error):
        if not thread:
            self.set_status(404)
            return self.finish()
        self.write({"data": thread})
        self.finish()

    @tornado.web.asynchronous
    def get(self, thread_id):
        self.db.threads.find_one({'_id': ObjectId(thread_id)}, callback=self._on_thread_fetched)
