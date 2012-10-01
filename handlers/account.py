#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
from tornado.web import HTTPError
from tornado.options import options

from .base import BaseHandler

class SigninHandler(BaseHandler):
    def get(self):
        self.render("signin.html")

class SignupHandler(BaseHandler):
    def get(self):
        self.render("signup.html")

class SignoutHandler(BaseHandler):
    def get(self):
        pass

routes = [
    (r"/signin", SigninHandler),
    (r"/signup", SignupHandler),
    (r"/signout", SignoutHandler),
]
