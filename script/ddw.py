#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import time
import urllib2

import socket
socket.setdefaulttimeout(30)

import markdown
md = markdown.Markdown(safe_mode=True)

from BeautifulSoup import BeautifulSoup

from lib import log, htmlstrip
from db import DdwDb

__url__ = "http://www.duduwo.com/"
__encode__ = "gbk"

def get_book_detail (id):
    try:
        _url = __url__ + "info/%d/%d.htm" % ((id/1000), id)
        html = urllib2.urlopen(_url).read()
        #html = unicode(html, __encode__, "ignore")

        soup = BeautifulSoup(html)
        info = soup.findAll(id=['In'])[0]

        #print type(info)
        #print info.__dict__
        #print info.prettify()

        a = dict()

        m = re.compile(r'作 者：(?P<T>.*?)<', re.S).search(info.prettify())
        if m: a['author'] = m.group('T').strip()

        m = re.compile(r'类 别：(?P<T>.*?)<', re.S).search(info.prettify())
        if m: a['cate'] = m.group('T').strip()

        m = re.compile(r'状 态：(?P<T>.*?)<', re.S).search(info.prettify())
        if m:
            tmp = m.group('T').strip()
            a['is_finish'] = False
            if tmp == "已完成":
                a['is_finish'] = True

        m = re.compile(r'票 票：(?P<T>.*?)<', re.S).search(info.prettify())
        if m: a['recommend_count'] = int(m.group('T'))

        m = re.compile(r'内容简介：(?P<T>.*/>)(?P<Name>.*?)最新章节', re.S).search(info.prettify())
        if m:
            a['desc'] = m.group('T').strip()#md.convert
            a['name'] = m.group('Name').strip()

        #print a
        return a

    except urllib2.HTTPError:
        log("Error: book_id "+ str(id) + " not exists.")
    except Exception,ex:
        log("Error: book_id "+ str(id) + " " + str(Exception) + ":" + str(ex) )

def get_chapters (id):
    try:
        _url = __url__ + "%d/%d/index.html" % ((id/1000), id)
        print _url
        html = urllib2.urlopen(_url).read()

        soup = BeautifulSoup(html,fromEncoding="gbk")

        a = dict()

        volumes = soup.findAll(attrs={'class' : re.compile("^book_article_")})
        flag = False
        i = 0
        j = 0
        sort = 0
        count = len(volumes)
        _re = re.compile(r'(?P<T>\d+?)\.html')
        for v in volumes:

            if v.attrs[0][1] == "book_article_texttitle":
                a[i] = {}
                a[i]['title'] = v.contents[0]
                a[i]['chs'] = []
                flag = True


            if v.attrs[0][1] == "book_article_listtext" and flag == True:
                chs = v.findAll({"a":True})
                for x in chs:
                    id = int(_re.search(x.attrs[0][1]).group("T"))
                    title = x.contents[0]
                    var = id, title, sort
                    a[i]['chs'].append(var)
                    sort += 1

            if j < count-1 :
                if volumes[j+1].attrs[0][1] == "book_article_texttitle":
                    flag = False
                    i += 1

            j += 1

        return a
    except urllib2.HTTPError:
        log("Error: get_chapters book_id "+ str(id) + " not exists.")
    except Exception,ex:
        log("Error: get_chapters book_id "+ str(id) + " " + str(Exception) + ":" + str(ex) )

def get_chapter(book_id, id):
    try:
        _url = __url__ + "%d/%d/%d.html" % (book_id/1000, book_id, id)
        print _url

        html = urllib2.urlopen(_url).read()
        """
        soup = BeautifulSoup(html,fromEncoding="gbk")

        info = soup.findAll(attrs={'id' : "booktext"})[0]
        info.strong.extract()
        s = info.prettify()
        s = s.replace('<div id="booktext">\n<!--go-->','')
        s = s.replace('<!--over-->\n</div>','')
        s = s.strip()
        print s
        return unicode(s, 'utf-8', "ignore")
        """
        html = unicode(html, __encode__, "ignore")
        m = re.compile(r'<!--go-->(?P<T>.*?)<!--over-->', re.S).search(html)
        text = ''
        if m:
            text = m.group('T')
            text = re.sub(r"(<STRONG>.*</STRONG><br><br>)", "", text)
        return text.strip()

    except urllib2.HTTPError:
        log("Error: get_chapter book_id "+ str(book_id) + " not exists.")
    except Exception,ex:
        log("Error: get_chapter book_id "+ str(book_id) + " " + str(Exception) + ":" + str(ex) )

def save_book (id):
    dw = DdwDb()
    book = dw.get_book(id)
    if book is None:
        print '-------------begin '+ str(id)+'-------------'
        book = get_book_detail(id)

        if book is not None:
            print '-------------saving-------------'
            #author
            author_id = 0
            author = dw.get_author(book['author'])
            if author is None:
                author_id = dw.insert_author(book['author'])
            else:
                author_id = int(author['id'])
            #category
            cate_id = 0
            cate = dw.get_category(book['cate'])
            if cate is None:
                cate_id = dw.insert_category(book['cate'])
            else:
                cate_id = int(cate['id'])
            #book
            desc = book['desc']
            try:
                desc = htmlstrip(desc).strip()
            except Exception,ex:
                log("Error: desc.error")
            dw.insert_book(id, book['name'], desc, author_id, cate_id, book['is_finish'],book['recommend_count'])

            print '-------------end of '+ str(id)+'-----------'
    else:
        print "Info: "+ str(id) + " already exists!"

def save_chapters (id):
    dw = DdwDb()
    book = dw.get_book(id)
    if book is not None:
        print '-------------begin '+ str(id)+'-------------'
        count = dw.get_chapters_count(id)
        if count is None or count['count'] > 0:
            print count['count']
            print 'Info: get_chapters_count %s > 0' % int(id)
            return
        chapters = get_chapters(id)
        #print chapters
        for item in chapters :
            var = chapters[item]
            v_title = var['title']
            print v_title
            #volume
            v = dw.get_volume(v_title,id)
            v_id = 0
            if v is None:
                v_id = dw.insert_volume(v_title,id)
            else:
                v_id = int(v['id'])
            #chapters
            for ch in var['chs']:
                chapter = dw.get_chapter(ch[0])
                if chapter is None:
                    print ch[1]
                    dw.insert_chapter(ch[0], ch[1], ch[2]*100, id, v_id)
        #
        one = db.get_book_last_one(id)
        if one is not None:
            #print one
            db.update_book_last_one(id, one['id'], one['title'], one['create_at'])
        print '-------------end of '+ str(id)+'-----------'
    else:
        print "Info: save_chapters "+ str(id) + " not exists!"

def save_text (id):
    dw = DdwDb()
    book = dw.get_book(id)
    if book is not None:
        print '-------------begin '+ str(id)+'-------------'
        chs = dw.get_chapters(id)
        if chs is not None or len(chs) > 0:
            for var in chs:
                print var['id']
                text = ''
                t = dw.get_chapter_text(var['id'])
                if t is None:
                    try:
                        text = get_chapter(id, var['id'])
                        if text is not None and text != '':
                            dw.insert_chapter_text(var['id'], text)
                            print '-------------end of '+ str(id)+'-----------'
                    except Exception,ex:
                        log("Error: get_chapter "+ str(id) + " " + str(Exception)+":"+str(ex) )
                print "Info: chapter "+str(var['id'])+" exists"
        else:
            print 'Info: have no chapters'
    else:
        print "Info: save_chapters "+ str(id) + " not exists!"

def books ():
    _count = 24221
    for i in range(24154, _count+1):
        if i%50==1:
            print "sleeping..."
            time.sleep(2)
        try:
            save_book(i)
        except Exception,ex:
            log("Error: book_id "+ str(i) + " " + str(Exception)+":"+str(ex) )

def chapters ():
    _count = 24221
    for i in range(24154, _count+1):
        #if i%10==1:
            #print "sleeping..."
            #time.sleep(2)
        try:
            save_chapters(i)
        except Exception,ex:
            log("Error: chapters book_id "+ str(i) + " " + str(Exception)+":"+str(ex) )

def text ():
    _count = 22962
    for i in range(2900, _count+1):
        #if i%10==1:
            #print "sleeping..."
            #time.sleep(2)
        try:
            save_text(i)
        except Exception,ex:
            log("Error: chapters book_id "+ str(i) + " " + str(Exception)+":"+str(ex) )

if __name__ == "__main__":
    #books()
    chapters()
    #text()
    #print get_chapter(2,929)