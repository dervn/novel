#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time
from db import DdwDb
from lib import write2file, htmlstrip, log, htmlremove, downimg

def mk_last ():
    db = DdwDb()
    count = db.get_book_count()['count']

    pageSize = 100
    page = count / pageSize + 1

    for i in range(0,page+1):
        step = i * pageSize
        rows = db.list(step)
        if rows is not None:
            for item in rows:
                one = db.get_book_last_one(item['id'])
                if one is not None:
                    #print one
                    db.update_book_last_one(item['id'], one['id'], one['title'], one['create_at'])
                    print item['id']
                #time.sleep(1)

def rows2txt ():
    db = DdwDb()
    count = db.get_book_count()['count']

    pageSize = 100
    page = count / pageSize + 1

    for i in range(0,page+1):
        step = i * pageSize+94
        rows = db.list(step)
        if rows is not None:
            for item in rows:
                print "book -------------------------------" + str(item["id"])
                path = mkdir(item["id"])
                chs = db.get_chapters(item['id'])
                if chs is not None:
                    for ch in chs:
                        #db.update_book_last_one(item['id'], one['id'], one['title'], one['create_at'])
                        chtext = db.get_chapter_text(ch['id'])
                        if chtext is not None:
                            try:
                                file_path = os.path.join(path, str(ch['id']))
                                text = htmlstrip(chtext["text"])
                                #write to file
                                write2file(file_path, text)
                                #update chapter size and text
                                db.update_chapter_size(ch['id'], len(text))
                                db.update_chapter_text(ch['id'], text)
                                print ch['id']
                            except Exception,ex:
                                log("Error: ch "+ str(ch['id']) + " " + str(Exception) + ":" + str(ex) )

                #time.sleep(10)

def mkdesc ():
    db = DdwDb()
    count = db.get_book_count()['count']

    pageSize = 100
    page = count / pageSize + 1

    for i in range(0,page+1):
        step = i * pageSize
        rows = db.list(step)
        if rows is not None:
            for item in rows:
                print "book -------------------------------" + str(item["id"])
                b = db.get_book(item['id'])
                try:
                    desc = htmlstrip(b["description"]).strip()
                    db.update_book_desc(item['id'], desc)
                except Exception,ex:
                    log("Error: mkdesc "+ str(item['id']) + " " + str(Exception) + ":" + str(ex),"desc.error")
                #time.sleep(20)

def downcover ():
    db = DdwDb()
    count = db.get_book_count()['count']

    pageSize = 100
    page = count / pageSize + 1

    for i in range(0,page+1):
        step = i * pageSize
        rows = db.list(step)
        if rows is not None:
            for item in rows:
                print "book -------------------------------" + str(item["id"])
                b = db.get_book(item["id"])
                if b is not None and b["cover"] == "":
                    cover = downimg(item["id"])
                    print cover
                    if cover != "":
                        db.update_book_cover(item['id'], cover)

def mkdir (id):
    path = "D:\\liubaikui\\jiushulou\\txt\\"
    path = os.path.join(path, str(id/1000), str(id))
    if os.path.exists(path) == False :
        os.makedirs(path)
    return path

if __name__ == "__main__":
    #rows2txt()
    downcover()