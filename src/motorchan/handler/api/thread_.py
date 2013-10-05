
import json
import datetime
import tornado.web
from bson.objectid import ObjectId

from motorchan.handler.base import BaseHandler

def json_serialize_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))


class ThreadAPIHandler(BaseHandler):

    @tornado.web.asynchronous
    def get(self):
        query_params = {}
        board_id = self.get_argument('board_id', None)
        if board_id:
            query_params['board_id'] = board_id

        self.db.threads.find(query_params).to_list(callback=self._on_thread_list_fetched)

    def _on_thread_list_fetched(self, thread_list, error):
        threads = []
        for thread in thread_list:
            threads.append({
                '_id': unicode(thread['_id']),
                'no': thread['no'],
                'op': thread['op']
            })
        self.write(json.dumps({"data": threads}, default=json_serialize_handler))
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        self.db.boards.find_and_modify(
            query={'_id': ObjectId(self.request.json['board_id'])},
            update={'$inc': {'post_max_id': 1}},
            callback=self._on_board_fetched,
        )

    def _on_board_fetched(self, board, error):
        thread = {
            'no': board['post_max_id'] + 1,
            'board_id': board['_id'],
            'op': self.request.json,
            'replies': [],
        }
        self.db.threads.insert(thread, callback=self._on_thread_inserted)

    def _on_thread_inserted(self, obj_id, error):
        self.set_status(201)
        self.write(json.dumps({'id': unicode(obj_id)}))
        self.finish()

