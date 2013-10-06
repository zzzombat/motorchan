
import tornado.gen
import tornado.web

import schema
from motorchan.handler.base import BaseHandler


class BoardAPIHandler(BaseHandler):

    @tornado.web.asynchronous
    def get(self):
        self.db.boards.find().to_list(1000, callback=self._on_fetched)

    def _on_fetched(self, boards, error):
        self.write({"data": boards})
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        schema.Board.validate(self.request.json)
        self.db.boards.insert(self.request.json, callback=self._on_inserted)

    def _on_inserted(self, documents, error):
        self.set_status(201)
        if error:
            self.write({"error": error.message})
            self.set_status(400)
        self.finish()
