#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import time
import urllib2
import datetime
import logging
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

import socket
socket.setdefaulttimeout(30)

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

__encode__ = "gbk"
__url__ = "http://www.duduwo.com/"
__root_path__ = "/home/work/htdocs/php/development/d"  #"D:\\liubaikui\\jiushulou\\script"

def log(msg, file_name = "error",no_time = False) :
    logger=logging.getLogger()
    handler=logging.FileHandler(file_name)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    if no_time != True:
        msg = str(datetime.datetime.utcnow()) + ":"+ msg
    logger.error(msg)
    #print msg

def htmlremove (text):
    items = [
        u"（谢谢支持　读读窝 Ｗｗｗ．Ｄｕｄｕwo．Ｃｏｍ　）",
        u"读读窝（www.duduwo.com），免费下载txt文本，大家收藏一下吧！百度搜索： 读读窝",
        u"（该小说由读读窝 www.duduwo.com　网络收集上传）",
        u"(请牢记或收藏读读窝 www.duduwo.com)",
        u"( 键盘同时按下Ctrl+D可以收藏！请牢记或收藏读读窝www.duduwo.com )",
        u"（该小说由读读窝小说网http:// 会员收集上传）",
        u"（该小说由读读窝 Ｗｗｗ．Ｄｕｄｕwo．Ｃｏｍ　网络收集上传）",
        u"【本文由“读读窝小说网”书友更新上传我们的网址是“www.duduwo.com”如章节错误/举报谢谢】",
        u"读读窝小说网，Ｗｗｗ．ｄｕduwo．Ｃｏｍ，用手机也能看。",
        u"（该小说由读读窝小说网www.duduwo.com 会员收集上传）",
        u"欢迎读者登录读读窝小说网www.duduwo.com查看更多优秀作品。",
        u"读读窝小说网www.duduwo.com更新超快，百度搜索： 读读窝",
    ]
    for i in items:
        text = text.replace(i,"")
    text = text.replace("www.duduwo.com","www.jiushulou.com")
    text = text.replace("duduwo.com","www.jiushulou.com")
    text = text.replace("Duduwo.com","www.jiushulou.com")
    text = text.replace("Ｗｗｗ．ｄｕduwo．Ｃｏｍ","www.ｊｉｕｓｈｕｌｏｕ.com")
    text = text.replace(u"读读窝","旧书楼")
    return text.strip()

def write2file (path, text):
    obj_file = open(path, 'w')
    obj_file.write(text.encode("utf-8"))
    obj_file.close()

def htmlstrip(html):
    #html = html.strip()
    #html = html.strip("http://")
    html = html.replace(u"<!面页章节尾部广告>","")

    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_script_1=re.compile(r'<script type="text/javascript">.+</script>',re.I)
    re_script_2=re.compile(r'<script>.+</script>',re.I)
    re_script_3=re.compile(r'<script&nbsp;type="text/javascript.+</script>',re.I)
    re_comment=re.compile(r'<!--.+//-->',re.I)
    re_iframe=re.compile(r'<iframe.+</iframe>',re.I)
    html=re_script.sub('',html) #去掉SCRIPT
    html=re_script_1.sub('',html)#strip script
    html=re_script_2.sub('',html)
    html=re_script_3.sub('',html)
    html=re_comment.sub('',html)
    html=re_iframe.sub('',html)

    html = html.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '');
    html = html.replace('<br />', '\n');
    html = html.replace('<br>', '\n');
    html = html.replace('<br/>', '\n');
    html = html.replace('\n\n\n\n', '\n\n');
    #soup = BeautifulSoup(html, fromEncoding = "utf-8")
    #html = soup.prettify()

    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)

def get_chapter(url):
    try:
        html = urllib2.urlopen(url).read()
        html = unicode(html, __encode__, "ignore")
        m = re.compile(r'<!--go-->(?P<T>.*?)<!--over-->', re.S).search(html)
        text = ''
        if m:
            text = m.group('T')
            text = re.sub(r"(<STRONG>.*</STRONG><br><br>)", "", text)
        return text.strip()
    except urllib2.HTTPError:
        log("Error: url:"+ url + " not exists.")
    except Exception,ex:
        log("Error: url:"+ url + " " + str(Exception) + ":" + str(ex) )

def main ():
    url_path = os.path.join(__root_path__, "urls")
    complete_path = os.path.join(__root_path__, "complete")
    txt_path = os.path.join(__root_path__, "txt")
    filenames = os.listdir(url_path)
    for name in filenames:
        print "---------------------------------------" + name
        path = os.path.join(txt_path, str(int(name)/1000), name)
        if os.path.exists(path) == False :
            os.makedirs(path)
        filePath = os.path.join(url_path, name)
        obj_file = open(filePath, 'r')
        lines = obj_file.readlines()
        for line in lines:
            print line
            file_path = os.path.join(path, line.strip("\n"))
            if os.path.exists(file_path):
                print '--- exists'
                continue
            url = __url__ + "%d/%d/%d.html" % (int(name)/1000, int(name), int(line.strip("\n")))
            print url
            text = get_chapter(url)
            if text is not None and text != "":
                try:
                    text = htmlstrip(text)
                    text = htmlremove(text)
                    #print text
                    write2file(file_path, text.strip())
                except Exception,ex:
                    log("Error: "+ url + " " + str(Exception) + ":" + str(ex) )
            print "end of url:" + url
            #time.sleep(10)
        os.rename(filePath, os.path.join(complete_path, name))
        print "--------------------------------- -----end of " + name

if __name__ == "__main__":
    main()