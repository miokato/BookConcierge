"""
Parse input data from line app
"""


long_sample_message = 'あの花の名前をまだ僕は知らないを見た人の感想を知りたい'
short_sample_message = 'あの花'
blank_sample_message = ''


def cutoff_msg20(input):
    try:
        msg_length = len(input)
    except TypeError:
        return ''
    if msg_length > 20:
        return '20文字以内の単語でしらべてほしいにゃー'

    return input

