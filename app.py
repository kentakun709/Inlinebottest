from email import message
from msilib import AMD64
import CommandList

from asyncio.windows_events import NULL
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

app = Flask(__name__)

line_bot_api = LineBotApi('RtimZ0mxW4QR8Ivf5zvnmo4TAMx446B9TVzL7K7j97F9993PPn79W3vuJc2pd2xATrm+uT31FXuJXU4Tzkns/wgOw/eURcv9QJaz3LrI66iViSoV0tO7E3nTZVxEVNKUmv12phYeIOwJZeayoNuczAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1b44e8b733146e212dbb1f1ffa4986a6')

@app.route("/")
def test():
    return "ok" 

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    group_id = NULL

    if event.source.type == 'group':
        if event.source.group_id == "C9f5f4a30a5dd0a0f9c63579c09235d61":
            group_id = event.source.group_id
            
        else:  WithdrawalProcess(event.source.group_id)

    for command in CommandList.CommandList:
        if message == event.message.text:
            hoge
        
    # line_bot_api.reply_message(
    #    event.reply_token,
    #    TextSendMessage("aaaWorldnanodaaaabunjinnanoda"))

    
#退会処理
def WithdrawalProcess(group_id):
    line_bot_api.leave_group(group_id)

    
if __name__ == "__main__":
    app.run()