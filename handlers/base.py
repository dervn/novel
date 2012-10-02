#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler, HTTPError
from jinja2 import TemplateNotFound

from da.model import Category

class BaseHandler(RequestHandler):
    @property
    def env(self):
        return self.application.env

    def get_error_html(self, status_code, **args):
        try:
            self.render('%s.html' % status_code)
        except TemplateNotFound:
            try:
                self.render('50x.html', status_code=status_code)
            except TemplateNotFound:
                self.write('epic fail')

    def render(self, template, **args):
        try:
            template = self.env.get_template(template)
        except TemplateNotFound:
            raise HTTPError(404)

        args['categories'] = Category.get_all_cat()

        self.env.globals['request']  = self.request
        self.env.globals['static_url'] = self.static_url
        self.env.globals['xsrf_form_html'] = self.xsrf_form_html
        self.write(template.render(args))

    def _get_page(self):
        page = self.get_argument('p', 1)
        try:
            return int(page)
        except:
            return 1

class NoDestinationHandler(BaseHandler):
    def get(self):
        raise HTTPError(404)
