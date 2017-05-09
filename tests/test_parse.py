import unittest
from nose.tools import ok_, eq_
from parse import TextParser


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


class TestTextParser(unittest.TestCase):
    def setUp(self):
        self.parser = TextParser()

    def test_set_text(self):
        # 第三引数にテストが失敗した時のメッセージを出すことができる
        self.assertEqual(self.parser.set_text('hello'), 'hello', 'incorrect')

    def test_parse_str_to_word(self):
        self.assertEqual(self.parser.parse_str_to_word('hello'), ['h','e','l','l','o'])

    def test_is_list_parse_str_to_word(self):
        self.assertTrue(isinstance(self.parser.parse_str_to_word(), list))
