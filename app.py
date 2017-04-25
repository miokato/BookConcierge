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
)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
AMAZON_ACCESS_SECRET = os.getenv('AMAZON_SECRET_KEY')
AMAZON_TAG = os.getenv('AMAZON_TAG')

app = Flask(__name__)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)
    # データをファイルとして保存
    save_json(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    book_title = fetch_book(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=book_title)
    )


def fetch_book(keyword):
    """fetch one book using amazon api"""
    amazon_api = AmazonAPI(AMAZON_ACCESS_KEY,
                           AMAZON_ACCESS_SECRET,
                           AMAZON_TAG,
                           ErrorHandler=error_handler,
                           region='JP',
                           )
    book = amazon_api.search_n(1, Keywords=keyword,
                                     SearchIndex='Books')
    book_title = book[0].title
    return book_title


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


if __name__ == '__main__':
    app.debug = True
    app.run()