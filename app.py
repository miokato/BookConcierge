import os
import json
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
)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

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
    id = event
    #profile = line_bot_api.get_profile(id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


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