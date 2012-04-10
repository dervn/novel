#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import uuid
import time
import base64
import datetime
import logging
import urllib2
from HTMLParser import HTMLParser
import tornado.database

import socket
socket.setdefaulttimeout(30)

def unixtime ():
    return time.time()

class DbBase():
    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db =  tornado.database.Connection(
                host = "127.0.0.1",
                database = "jiushulou",
                user = "root",
                password = "123")
        return self._db

def log(msg, file_name = "error.txt",no_time = False) :
    logger=logging.getLogger()
    handler=logging.FileHandler(file_name)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    if no_time != True:
        msg = str(datetime.datetime.utcnow()) + ":"+ msg
    logger.error(msg)
    #print msg

def htmlstrip(html):
    html = html.strip()
    html = html.replace('</>', '');
    html = html.strip("http://")
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)

def htmlremove (text):
    items = [
        u"（谢谢支持　读读窝 Ｗｗｗ．Ｄｕｄｕwo．Ｃｏｍ　）",
        u"读读窝（www.duduwo.com），免费下载txt文本，大家收藏一下吧！百度搜索： 读读窝",
        u"（该小说由读读窝 www.duduwo.com　网络收集上传）",
        u"(请牢记或收藏读读窝 www.duduwo.com)",
        u"( 键盘同时按下Ctrl+D可以收藏！请牢记或收藏读读窝www.duduwo.com )",
        u"（该小说由读读窝小说网http:// 会员收集上传）",
    ]
    for i in items:
        text = text.replace(i,"")
    return text

def write2file (path, text):
    obj_file = open(path, 'w')
    obj_file.write(text.encode("utf-8"))
    obj_file.close()

def readfile (path):
    all_the_text = ""
    obj_file = open(path)
    try:
        all_the_text = obj_file.read()
    finally:
        obj_file.close()
    return all_the_text

def genuuid ():
    return uuid.uuid4().hex[:16]

def downimg (id):
    guid = genuuid()
    picurl="http://www.duduwo.com/files/article/image/%s/%s/%ss.jpg" % ((id/1000), id, id)
    save_path="D:\\liubaikui\\jiushulou\\covers\\"
    save_path = os.path.join(save_path, str(id/1000))
    if os.path.exists(save_path) == False :
        os.makedirs(save_path)
    # 给定图片存放名称
    fileName = os.path.join(save_path, guid + ".jpg")
    # 文件名是否存在
    if os.path.exists(fileName) == False:
        try:
            imgData = urllib2.urlopen(picurl).read()
            output = open(fileName,'wb+')
            output.write(imgData)
            output.close()
            return guid
        except Exception,ex:
            print picurl
            print str(Exception)+":"+str(ex)
            return ''
