import os
import json
import time
from datetime import datetime

from flask import Flask, request, abort

from amazon.api import AmazonAPI

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

from book import fetch_books, trim_str_60

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
AMAZON_ACCESS_SECRET = os.getenv('AMAZON_SECRET_KEY')
AMAZON_TAG = os.getenv('AMAZON_TAG')

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN, timeout=50.0)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
    # データをファイルとして保存
    # save_json(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    amazon_api = amazon_init()
    books = fetch_books(amazon_api, keyword=event.message.text, num=3)
    if books is None:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='おすすめの本を見つけることができませんでした。')
        )
    else:
        make_carousel(event, books, len(books))
        #make_button(event, books)


def amazon_init():
    amazon_api = AmazonAPI(AMAZON_ACCESS_KEY,
                           AMAZON_ACCESS_SECRET,
                           AMAZON_TAG,
                           ErrorHandler=error_handler,
                           region='JP',
                           )
    return amazon_api


def error_handler(err):
    """error handler for amazon api"""
    ex = err['exception']
    if ex.code == 503:
        time.sleep(1)
        return True


def save_json(dic_or_json):
    """json形式か辞書型のデータを整形してjsonファイルとして書き出す"""
    dir = './data/'
    now = datetime.now().strftime('%Y%m%d_%H%M_%s')
    prefix = 'time-'
    suffix = '.json'
    file = dir + prefix + now + suffix
    if isinstance(dic_or_json, dict):
        dic = dic_or_json
    else:
        dic = json.loads(dic_or_json)

    with open(file, 'wt') as f:
        json.dump(dic, f, ensure_ascii=False, indent=4)


def make_carousel(event, books, cnt):
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
        title = 'おすすめの本' + str(i)
        text = trim_str_60(books[i].title)
        image = books[i].large_image_url
        actions = [
            URITemplateAction(
                label=url_label, uri=books[i].detail_page_url
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