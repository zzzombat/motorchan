
import json
import motor
import tornado.gen
import tornado.web
from motorchan.handler.base import BaseHandler

class BoardAPIHandler(BaseHandler):

    def _on_fetched(self, documents, error):
        boards = []
        for doc in documents:
            boards.append({
                'id': unicode(doc['_id']),
                'name': doc['name'],
                'slug': doc['slug'],
            })
        self.write({"data": boards})
        self.finish()

    @tornado.web.asynchronous
    def get(self):
        self.db.boards.find().to_list(10000, callback=self._on_fetched)


    def _on_inserted(self, documents, error):
        self.set_status(201)
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        self.db.boards.insert(self.request.json, callback=self._on_inserted)




