#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib import DbBase, unixtime, log

class DdwDb (DbBase):

    def get_book_count (self):
        return self.db.get("SELECT count(1) as count FROM tb_book WHERE 1;")

    def list (self, limit):
        return self.db.query("SELECT * FROM tb_book ORDER BY id LIMIT %s,100", limit)

    def get_book (self, id):
        return self.db.get("SELECT * FROM tb_book WHERE id=%s" % int(id))

    def get_book_last_one (self, id):
        return self.db.get(
            "SELECT * FROM tb_chapters WHERE book_id=%s ORDER BY sort_num DESC LIMIT 0,1" % int(id)
        )

    def update_book_last_one(self, book_id, id, title, time):
        return self.db.execute(
            "UPDATE tb_book SET last_chapter_id=%s, last_chapter_title=%s, last_update_at=%s WHERE id=%s", id, title, time, book_id
        )

    def update_book_desc(self, id, desc):
        return self.db.execute(
            "UPDATE tb_book SET description=%s WHERE id=%s", desc, id
        )

    def update_book_cover(self, id, cover):
        return self.db.execute(
            "UPDATE tb_book SET cover=%s WHERE id=%s", cover, id
        )

    def insert_book (self, id, name, description, author_id=0, category_id=0, is_finish=0, recommend_count=0):
        return self.db.execute(
            "INSERT INTO tb_book(id, name, description, author_id, category_id,is_finish,recommend_count,create_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)", int(id), name, description, int(author_id), int(category_id), int(is_finish), int(recommend_count), unixtime()
        )

    def get_category (self, name):
        _sql = "SELECT * FROM tb_category WHERE name='%s'" % name
        return self.db.get(_sql)

    def insert_category (self, name):
        _sql = "INSERT INTO tb_category(name,create_at) VALUES('%s',%s)" % (name, unixtime())
        return self.db.execute(_sql)

    def get_author (self, name):
        _sql = "SELECT * FROM tb_author WHERE name='%s'" % name
        return self.db.get(_sql)

    def insert_author (self, name):
        _sql = "INSERT INTO tb_author(name,create_at) VALUES('%s',%s)" % (name, unixtime())
        return self.db.execute(_sql)

    def get_volume (self, title, book_id):
        _sql = "SELECT * FROM tb_volume WHERE title='%s' AND book_id=%s" % (title, book_id)
        return self.db.get(_sql)

    def insert_volume (self, title, book_id):
        _sql = "INSERT INTO tb_volume(title,book_id,create_at) VALUES('%s',%s,%s)" % (title, book_id, unixtime())
        return self.db.execute(_sql)

    def get_chapter (self, id):
        _sql = "SELECT * FROM tb_chapters WHERE id=%s" % id
        return self.db.get(_sql)

    def insert_chapter (self, id, title, sort_num, book_id, volume_id):
        _sql = u"INSERT INTO tb_chapters(id, title, sort_num, book_id, volume_id, create_at) VALUES(%s, '%s', %s, %s, %s, %s)" % (int(id), title, int(sort_num), int(book_id), int(volume_id), unixtime())
        #print _sql
        return self.db.execute(_sql)

    def get_chapters_count (self, book_id):
        _sql = "SELECT count(1) as count FROM tb_chapters WHERE book_id=%s" % book_id
        return self.db.get(_sql)

    def get_last_sort (self, id):
        _sql = "SELECT sort_num FROM tb_chapters WHERE book_id=%s ORDER BY sort_num DESC LIMIT 0,1" % id
        return self.db.get(_sql)

    def insert_chapter_text (self, id, text):
        return self.db.execute(
            "INSERT INTO tb_chapter_text(id,text) VALUES(%s,%s)", int(id), text
        )

    def get_chapters (self, book_id):
        return self.db.query("SELECT id FROM tb_chapters WHERE book_id=%s", book_id)

    def get_chapter_text (self, id):
        return self.db.get("SELECT id,text FROM tb_chapter_text WHERE id=%s", id)

    def update_chapter_text (self, id, text):
        return self.db.execute(
            "UPDATE tb_chapter_text SET text=%s WHERE id=%s", text, int(id)
        )

    def update_chapter_size (self, id, size):
        return self.db.execute(
            "UPDATE tb_chapters SET size=%s WHERE id=%s", size, int(id)
        )