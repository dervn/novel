#!/usr/bin/env python
# encoding: utf-8

"""
main.py
Created by dn on 2011-07-24.
Copyright (c) 2011 shubz. All rights reserved.
"""
import os
import logging
import tornado
from tornado import web
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.options import define, options
from tornado.httpserver import HTTPServer
from jinja2 import Environment, FileSystemLoader

from lib.utils import datetimeformat, mdconvert, get_cover, get_status

define("config", default="config.py", help="config file path")
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="run the server mode Debug", type=bool)
define("cookie_secret", default="b23aadc7b8c0dbc5a9b38341944c3998b23aadc7b8", help="key for HMAC")
define("static_url_prefix", default="/static/", help="static url prefix")
define("login_url", default="/signin", help="login url")
define("database_echo", default=False, help="sqlalchemy database engine echo switch")
define("database_engine", default="mysql://root:123@127.0.0.1/jiushulou", help="the database connect string for sqlalchemy")
define("txt_path", default="/home/work/txt", help="text file path")
define("page_size", default=30, help="each page items num")
# mysql server Options
define("mysql_host_m", default='127.0.0.1', help="main hostname or IP address of the instance to connect to")
define("mysql_host_s", default='127.0.0.1', help="subordinate hostname or IP address of the instance to connect to")
define("mysql_port", default=3306, help="port number on which to connect", type=int)
define("mysql_db", default='jiushulou', help="database name")
define("mysql_user", default='root', help="database name")
define("mysql_password", default='123', help="database name")
define("max_idle_time", default=5, help="max idle time")

define("hot", default="21249,21028,8,13435", help="max idle time")
define("recommend", default="18320,21,69,42", help="max idle time")
define("finish", default="11578,11507,72,10", help="max idle time")

class Application(web.Application):
    def __init__ (self):
        from handlers import routes
        settings = dict(
            debug = options.debug,
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            static_url_prefix = options.static_url_prefix,
            cookie_secret = options.cookie_secret,
            xsrf_cookies = True,
            login_url = options.login_url,
        )

        super(Application, self).__init__(routes, **settings)

        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        self.env = Environment(
                loader=FileSystemLoader(template_path),
                extensions = ['jinja2.ext.i18n',
                              'lib.jinja2htmlcompress.HTMLCompress'
                             ],
                )
        #Custom Filters
        self.env.filters = {
            'datetimeformat' : datetimeformat,
            'mdconvert' : mdconvert,
            'get_cover' : get_cover,
            'get_status' : get_status,
        }

        self.env.install_null_translations(newstyle=True)
        self.env.globals['cfg'] = settings

        logging.info("load finished!")

def main():
    tornado.options.parse_command_line()
    if options.config:
        conf_path = os.path.join(os.path.dirname(__file__), options.config)
        #print conf_path
        tornado.options.parse_config_file(conf_path)
        #print tornado.options.options
    tornado.options.parse_command_line()

    http_server = HTTPServer(Application(), xheaders=True)
    http_server.bind(options.port)
    http_server.start()

    IOLoop.instance().start()

if __name__ == "__main__":
    main()
