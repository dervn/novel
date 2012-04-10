#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, time
from db import DdwDb

def write_urls ():
    db = DdwDb()
    print os.path.dirname(__file__)
    _tmp_path = "D:\\liubaikui\\jiushulou\\script\\urls"
    _count = 24221
    for i in range(24154, _count+1):
        book = db.get_book(i)
        if book is not None:
            chs = db.get_chapters(i)
            if chs is not None and len(chs) > 0:
                print "write to " + str(i)
                path = os.path.join(_tmp_path, str(i))
                obj_file = open(path, 'w+')
                urls = []
                for var in chs:
                    t = db.get_chapter_text(var['id'])
                    if t is None:
                        urls.append(str(var['id'])+"\n")
                #print urls
                obj_file.writelines(urls)
                obj_file.close()

if __name__ == "__main__":
    write_urls()