#!/usr/bin/env python
# encoding: utf-8

routes = []

from handlers import front
from handlers import account

routes.extend(front.routes)
routes.extend(account.routes)
