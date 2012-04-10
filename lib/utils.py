#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
from hashlib import sha1
import random
from markdown import Markdown

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    dt = time.localtime(value)
    return time.strftime(format, dt)

def mdconvert (value):
    markdowner = Markdown()
    return markdowner.convert(value)

def get_cover (id, cover):
    t= ''
    if cover == "":
        t = 'images/cover.jpg'
    else:
        t = 'covers/' + str(id/1000) + "/" + cover +".jpg"
    return t

def get_status (status):
    t = u"连载中"
    if ord(status) == 1:
        t = u"已完本"
    return t

def hexuserpass(password):

    enpass = sha1(password.encode('utf-8')).hexdigest()
    return enpass

def checkuserpass(passwd,enpass):
    password = hexuserpass(passwd)
    if password==enpass:
        return True
    else:
        return False

def hexpassword(password):
    """
    加密密码
    """
    seed="1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa=[]
    for i in range(8):
        sa.append(random.choice(seed))
    salt=''.join(sa)
    enpass=sha1(sha1((salt+password).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()

    return str(salt)+'$'+str(enpass)

def checkpassword(passwd,enpass):
    salt=enpass[ :8]
    password=sha1(sha1((salt+passwd).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest()
    p=str(salt)+'$'+str(password)
    if p==enpass:
        return True
    else:
        return False

class ObjectDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        return None

    def __setattr__(self, key, value):
        self[key] = value
