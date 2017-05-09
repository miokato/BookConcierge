import unittest
from nose.tools import ok_, eq_
from amazon.api import AmazonAPI
from app import amazon_init

from book import fetch_books, trim_str_60


class TestFetchBook(unittest.TestCase):

    def setUp(self):
        self.amazon_api = amazon_init()
        self.number_of_books = 20
        self.keyword = '?'

    def test_amazon_api_search_n(self):
        books = self.amazon_api.search_n(self.number_of_books,
                                         Keywords=self.keyword,
                                         SearchIndex='Books')
        self.assertEqual(len(books), 20)


class TestStringMethods(unittest.TestCase):
    """テストケースサンプル"""
    def test_upper(self):
        eq_('foo'.upper(), 'FOO')
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        ok_('FOO'.isupper())
        ok_(not 'Foo'.isupper())
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        with self.assertRaises(TypeError):
            s.split(2)


