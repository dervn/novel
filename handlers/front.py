#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time
from tornado.web import HTTPError
from tornado.options import options

from .base import BaseHandler
from da.model import Category, Book, Author, Chapter, Volume

from lib.utils import get_cover, get_status, mdconvert, ObjectDict
from lib.pagination import Pagination

class IndexHandler(BaseHandler):
    def get(self):
        news = Book.get_all_books()
        recommends = Book.get_recommend_books()
        hots = Book.get_hot_books()

        _hot = Book.get_books_by_ids(options.hot)
        _recommend = Book.get_books_by_ids(options.recommend)
        _finish = Book.get_books_by_ids(options.finish)

        self.render("index.html",
            news=news,
            recommends=recommends,
            hots=hots,
            hot = _hot,
            recommend = _recommend,
            finish = _finish,
        )

class BookHandler(BaseHandler):
    def get(self, id):
        book = Book.get_book_by_id(id)
        if not book:
            raise HTTPError(404)

        cate = Category.get_cat_by_id(book["category_id"])
        author = Author.get_author_by_id(book["author_id"])

        cover = get_cover(book['id'], book['cover']);

        self.render("book.html", book=book, cover=cover, cate=cate, author=author)

class ChaptersHandler(BaseHandler):
    def get(self, id):
        book = Book.get_book_by_id(id)
        if not book:
            raise HTTPError(404)
        a = []
        author = Author.get_author_by_id(book["author_id"])
        volumes = Volume.get_volumes_by_book_id(id)
        chapters = Chapter.get_chapters_by_book_id(id)
        for i,item in enumerate(volumes):
            var ={}
            var['id'] = item.id
            var['title'] = item.title
            var['chs'] = []
            for ch in chapters:
                if ch.volume_id == item.id:
                    var['chs'].append(ch)
            a.append(var)
        self.render("chapters.html", book=book, volumes=a, author=author)

class ChapterHandler(BaseHandler):
    def get(self, book_id, id):
        chapter = Chapter.get_chapter_by_id(id)
        if not chapter:
            raise HTTPError(404)

        book = Book.get_book_by_id(chapter.book_id)
        author = Author.get_author_by_id(book["author_id"])
        text = ""
        from tornado.options import options
        filepath = os.path.join(options.txt_path, str(int(book_id)/1000), book_id, id)
        if os.path.exists(filepath):
            obj_file = open(filepath)
            try:
                text = obj_file.read()
            finally:
                obj_file.close()
        else:
            row = Chapter.get_text_by_id(id)
            if row is not None:
                text = row['text']
                #text = htmlremove(text)
            else:
                text = '正在努力的加载数据...'
        #text = htmlremove(text)

        previous = Chapter.get_previous(book_id, chapter["sort_num"])
        if not previous:
            previous = 'index'
        else:
            previous = previous["id"]
        next = Chapter.get_next(book_id, chapter["sort_num"])
        if not next:
            next = 'index'
        else:
            next = next["id"]

        self.render("chapter.html",
            book=book,
            chapter=chapter,
            text=text,
            author=author,
            previous=previous,
            next=next,
        )

class CategoryHandler(BaseHandler):
    def get(self, id):
        cate = Category.get_cat_by_id(id)
        page = self._get_page()
        books = Book.get_page_books_by_cate(id, page)
        if not books and page != 1:
            raise HTTPError(404)

        pagination = Pagination(page, 30, cate["count"])

        self.render("cate.html",
            cate=cate,
            pagination=pagination,
            books=books
        )

class FinishHandler(BaseHandler):
    def get(self):
        page_size = 30
        count = Book.get_count(True)["count"]
        page = self._get_page()
        books = Book.get_finish_books(page, page_size)
        if not books and page != 1:
            raise HTTPError(404)

        pagination = Pagination(page, page_size, count)

        self.render("finish.html",
            pagination=pagination,
            books=books
        )

class AllHandler(BaseHandler):
    def get(self):
        page_size = 30
        count = Book.get_count()["count"]
        page = self._get_page()
        books = Book.get_all_books(page, page_size)
        if not books and page != 1:
            raise HTTPError(404)

        pagination = Pagination(page, page_size, count)

        self.render("finish.html",
            pagination=pagination,
            books=books
        )

class AuthorHandler(BaseHandler):
    def get(self, id):
        author = Author.get_author_by_id(id)

        if not author:
            raise HTTPError(404)

        books = Book.get_books_by_author(id)

        self.render("author.html", author=author, books=books)

class AboutHandler(BaseHandler):
    def get(self):
        self.render("about.html")

routes = [
    (r"/", IndexHandler),
    (r"/book/(\d+).html", BookHandler),
    (r"/book/(\d+)/index.html", ChaptersHandler),
    (r"/book/(\d+)/(\d+?).html", ChapterHandler),
    (r"/book/cate/(\d+?).html", CategoryHandler),
    (r"/book/author/(\d+?)", AuthorHandler),
    (r"/book/all", AllHandler),
    (r"/book/finish", FinishHandler),
    (r"/about", AboutHandler),
]