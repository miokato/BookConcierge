import unittest
from nose.tools import ok_, eq_

from search import fetch_books


class TestFetchBooks(unittest.TestCase):
    """
    Check below
    number of books parameter
    input Nonetype
    return Nonetype
    """
    def setUp(self):
        pass

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
