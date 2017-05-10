"""
Create and send message using Line Bot API.
"""

import os
import json
import time
from datetime import datetime

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    CarouselTemplate, CarouselColumn,
    URITemplateAction, PostbackTemplateAction,
    MessageTemplateAction, TemplateSendMessage,
    ButtonsTemplate
)

from book import trim_str_60
from search import fetch_books

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN, timeout=50.0)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route('/callback', methods=['POST'])
def callback():
    """
    エンドポイントを叩かれると呼び出される関数
    :return: 
    """
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    イベントハンドラ。メッセージを受け取ると実行される
    :param event: 
    :return: 
    """

    books_title, books_image_url, books_detail_url = fetch_books(event.message.text, number_of_books=1)
    if books_title is None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='おすすめの本を見つけることができませんでした。')
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=books_title[0])
        )
        #make_carousel(event,
        #              books_title,
        #              books_image_url,
        #              books_detail_url,
        #              len(books_title))
        #make_button(event, books)


def make_carousel(event, books_title, books_image_url, books_detail_url, cnt):
    """
    1~3冊の本を取得してカルーセル型のリプライメッセージを作成し、返信する
    max characters of title are 40
    max characters of text are 60 
    :param event: 
    :param books: 
    """
    columns_list = []
    url_label = 'ウェブでさがす'
    for i in range(cnt):
        title = 'おすすめの本 : ' + str(i+1) + '冊目'
        # text = trim_str_60(books_title[i])
        text = books_title[i]
        image = books_image_url[i]
        actions = [
            URITemplateAction(
                label=url_label, uri=books_detail_url[i]
            )
        ]
        c_column = CarouselColumn(title=title,
                       text=text,
                       thumbnail_image_url=image,
                       actions=actions)
        columns_list.append(c_column)
    carousel_template = CarouselTemplate(columns=columns_list)
    template_message = TemplateSendMessage(
        alt_text='Buttons alt text', template=carousel_template
    )
    line_bot_api.reply_message(event.reply_token,
                               template_message)


def make_button(event, books):
   buttons_template = ButtonsTemplate(
       title='button sample', type='buttons', text='hello my button', action=[
           URITemplateAction(
               label='go to line.me', uri='https://line.me'
           ),
           PostbackTemplateAction(label='ping', data='ping'),
           PostbackTemplateAction(
               label='ping with text', data='ping',
               text='ping'
           ),
       ]
   )
   template_message = TemplateSendMessage(
       alt_text='Buttons alt text', template=buttons_template
   )
   line_bot_api.reply_message(event.reply_token, template_message)


if __name__ == '__main__':
    app.debug = True
    app.run()