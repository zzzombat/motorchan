# -*- coding: utf-8 -*-
import tornado
import motor

from base import BaseHandler
from motorchan.forms import TestForm

class TestHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        form = TestForm(self)
        self.render('test.html', form=form, errors=None)    
