import unittest
from nose.tools import ok_, eq_

from search import BookScraper, fetch_books


class TestBookScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = BookScraper()

    def test_fetch_with_no_keyword(self):
        self.scraper.fetch('', number_of_books=1)
        eq_(self.scraper.books_title, [])

    def test_fetch_with_long_keyword(self):
        long_keyword = 'このねこの気持ちは誰がしっているというのか、いや知らない。'
        self.scraper.fetch(long_keyword, number_of_books=1)
        eq_(self.scraper.books_title, [])


class TestFetchBooks(unittest.TestCase):
    """
    Check below
    number of books parameter
    input Nonetype
    return Nonetype
    """
    # check common parameter
    def test_fetch_books_size(self):
        books = fetch_books('ねこ', number_of_books=2)
        eq_(len(books), 3)

    def test_fetch_books_type(self):
        books = fetch_books('ねこ', number_of_books=2)
        eq_(type(books), tuple)

    def test_fetch_books_none_type(self):
        books = fetch_books('', number_of_books=2)
        eq_(type(books), type(None))

    # check number of books
    def test_fetch_books_number_of_books_zero(self):
        books = fetch_books('ねこ', number_of_books=0)
        eq_(type(books), type(None))

    def test_fetch_books_number_of_books_6(self):
        books = fetch_books('ねこ', number_of_books=6)
        eq_(type(books), type(None))

    def test_fetch_books_number_of_books_5(self):
        books = fetch_books('ねこ', number_of_books=5)
        eq_(type(books), tuple)
