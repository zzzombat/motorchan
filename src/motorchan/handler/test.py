# -*- coding: utf-8 -*-
import logging
from functools import partial

import tornado
import motor

from base import BaseHandler
from motorchan.forms import TestForm

logger = logging.getLogger(__name__)


class TestHandler(BaseHandler):
   
    @tornado.web.asynchronous
    def get(self):
        form = TestForm(self)
        self.render('test.html', form=form, errors=None)
       
#    @tornado.gen.coroutine   
    def _on_connection_opened(self, fs, error):
        cb = partial(self._on_new_file, img=self.request.files['image'][0])
        return fs.new_file(callback=cb)
    
    def _on_new_file(self, gridin, error, img=None):
        gridin.write(img['body'])
        gridin.set('content_type', img['content_type'])
        gridin.close()
        logger.info('Uploaded with id %s', gridin._id)
        self.write(unicode(gridin._id))
        self.finish()
    
    @tornado.web.asynchronous
    def post(self):
        form = TestForm(self)
        return motor.MotorGridFS(self.db).open(self._on_connection_opened)           
