import unittest
from nose.tools import ok_, eq_

from parse import cutoff_msg20


class TestCutOffMsg20(unittest.TestCase):
    """
    LINEから入力された文字列が渡されるので、入力はすべてstr
    """
    def test_cutoff_msg20_with_japanese_msg(self):
        msg = 'あの花'
        eq_(cutoff_msg20(msg), msg)

    def test_cutoff_msg20_with_english_msg(self):
        msg = 'anohana'
        eq_(cutoff_msg20(msg), msg)

    def test_cutoff_msg20_with_long_msg(self):
        msg = 'あの花の名前を僕はまだ知らないを見たんだけど、君どう思う?'
        eq_(cutoff_msg20(msg), '20文字以内の単語でしらべてほしいにゃー')

    def test_cutoff_msg20_with_blank_msg(self):
        msg = ''
        eq_(cutoff_msg20(msg), '')

    def test_cutoff_msg20_with_none(self):
        msg = None
        eq_(cutoff_msg20(msg), '')

