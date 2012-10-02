#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import database
from tornado.options import options

MYSQL_DB = options.mysql_db
MYSQL_USER = options.mysql_user
MYSQL_PASS = options.mysql_password
MYSQL_HOST_M = options.mysql_host_m #主数据库 进行Create,Update,Delete 操作
MYSQL_HOST_S = options.mysql_host_s #从数据库 读取
MYSQL_PORT = options.mysql_port
MAX_IDLE_TIME = options.max_idle_time

PAGE_SIZE = options.page_size

mdb = database.Connection("%s:%s"%(MYSQL_HOST_M, str(MYSQL_PORT)), MYSQL_DB, MYSQL_USER, MYSQL_PASS, max_idle_time = MAX_IDLE_TIME)
sdb = database.Connection("%s:%s"%(MYSQL_HOST_S, str(MYSQL_PORT)), MYSQL_DB, MYSQL_USER, MYSQL_PASS, max_idle_time = MAX_IDLE_TIME)

class Category():
    def get_all_cat(self):
        return sdb.query('SELECT * FROM `tb_category` ORDER BY `id` ASC')

    def get_cat_by_id(self, id = ''):
        return sdb.get('SELECT * FROM `tb_category` WHERE `id` = %s LIMIT 1' % str(id))

Category = Category()

class Book():
    def get_count (self, finish=False):
        if finish:
            return sdb.get('SELECT count(1) AS count FROM `tb_book` WHERE is_finish=1 LIMIT 1')
        else:
            return sdb.get('SELECT count(1) AS count FROM `tb_book` LIMIT 1')

    def get_book_by_id (self, id = ''):
        return sdb.get('SELECT * FROM `tb_book` WHERE `id` = %s LIMIT 1' % str(id))

    def get_recommend_books (self):
        return sdb.query('''
            SELECT b.*, a.`name` as author_name
            FROM `tb_book` b, tb_author a
            WHERE b.author_id=a.id
            ORDER BY b.recommend_count DESC
            LIMIT 0,10'''
        )

    def get_hot_books (self):
        return sdb.query('''
            SELECT b.*, a.`name` as author_name
            FROM `tb_book` b, tb_author a
            WHERE b.author_id=a.id
            ORDER BY b.read_count DESC
            LIMIT 0,10'''
        )

    def get_all_books (self, page = 1, page_size = 30):
        sql = '''
            SELECT b.id, b.name, b.is_finish, b.last_update_at, b.last_chapter_id, b.last_chapter_title, c.name AS cate_name, a.id AS author_id, a.name AS author_name
            FROM tb_book AS b ,tb_author AS a, tb_category AS c
            WHERE b.author_id = a.id AND b.category_id = c.id
            ORDER BY b.last_update_at DESC
            LIMIT %s,%s'''
        return sdb.query(sql, (page - 1) * page_size, page_size)

    def get_finish_books (self, page = 1, page_size = 30):
        sql = '''
            SELECT b.id, b.name, b.is_finish, b.last_update_at, b.last_chapter_id, b.last_chapter_title, c.name AS cate_name, a.id AS author_id, a.name AS author_name
            FROM tb_book AS b ,tb_author AS a, tb_category AS c
            WHERE b.author_id = a.id AND b.category_id = c.id AND b.is_finish=1
            ORDER BY b.last_update_at DESC
            LIMIT %s,%s'''
        return sdb.query(sql, (page - 1) * page_size, page_size)

    def get_search_books (self, key, page = 1, page_size = 30):
        sql = '''
            SELECT b.id, b.name, b.is_finish, b.last_update_at, b.last_chapter_id, b.last_chapter_title, c.name AS cate_name, a.id AS author_id, a.name AS author_name
            FROM tb_book AS b ,tb_author AS a, tb_category AS c
            WHERE b.author_id = a.id AND b.category_id = c.id AND b.name LIKE "%%%s%%"
            ORDER BY b.last_update_at DESC
            LIMIT %s,%s'''
        return sdb.query(sql, key, (page - 1) * page_size, page_size)

    def get_search_books_count (self, key):
        sql = '''
            SELECT count(1) as count
            FROM tb_book AS b
            WHERE b.name LIKE "%%%s%%"
            '''
        return sdb.get(sql, key)

    #direction = 'next', page = 1 , base_id = '', limit = PAGE_SIZE
    def get_page_books_by_cate (self, id = '', page = 1, page_size = 30):
        sql = '''
            SELECT b.id, b.name, b.is_finish, b.last_update_at, b.last_chapter_id, b.last_chapter_title, a.id AS author_id, a.name AS author_name
            FROM tb_book AS b ,tb_author AS a
            WHERE b.author_id = a.id AND b.category_id =%s
            ORDER BY b.last_update_at DESC
            LIMIT %s,%s'''
        return sdb.query(sql, id, (page - 1) * page_size, page_size)

    def get_books_by_author (self, id = ''):
        sql = '''
            SELECT b.id, b.name, b.is_finish, b.last_update_at, b.last_chapter_id, b.last_chapter_title, c.name AS cate_name
            FROM tb_book AS b, tb_category AS c
            WHERE b.author_id = %s AND b.category_id=c.id
            ORDER BY b.last_update_at DESC'''
        return sdb.query(sql, id)

    def get_books_by_ids (self, ids=""):
        sql = '''
            SELECT b.id, b.name, b.cover, b.description, c.name AS cate_name, a.name AS author_name
            FROM tb_book AS b ,tb_author AS a, tb_category AS c
            WHERE b.author_id = a.id AND b.category_id = c.id AND b.id in('''+ids+''')'''
        return sdb.query(sql)

Book= Book()

class Author():
    def get_author_by_id (self, id = ''):
        return sdb.get('SELECT * FROM `tb_author` WHERE `id` = %s LIMIT 1' % str(id))

Author = Author()

class Chapter():
    def get_chapter_by_id (self, id = ''):
        return sdb.get('SELECT * FROM `tb_chapters` WHERE `id` = %s LIMIT 1' % str(id))

    def get_chapters_by_book_id (self, id = ''):
        return sdb.query('SELECT * FROM `tb_chapters` WHERE `book_id` = %s' % str(id))

    def get_text_by_id (self, id = ''):
        return sdb.get('SELECT * FROM `tb_chapter_text` WHERE `id` = %s LIMIT 1' % str(id))

    def get_previous (self, book_id, sort_num):
        sql = 'SELECT * FROM tb_chapters WHERE book_id=%s AND sort_num < %s ORDER BY sort_num LIMIT 0,1'
        return sdb.get(sql, book_id, sort_num )

    def get_next (self, book_id, sort_num):
        sql = 'SELECT * FROM tb_chapters WHERE book_id=%s AND sort_num > %s ORDER BY sort_num LIMIT 0,1'
        return sdb.get(sql, book_id, sort_num )

Chapter = Chapter()

class Volume():
    def get_volumes_by_book_id (self, id = ''):
        return sdb.query('SELECT * FROM `tb_volume` WHERE `book_id` = %s' % str(id))

Volume = Volume()
