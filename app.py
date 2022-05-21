from email import message
from msilib import AMD64
from tokenize import group
from urllib.parse import _NetlocResultMixinBase
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


""""""
#揮発性ユーザーデータ
users = { }
#揮発性グループデータ
groups = { }


###
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    #送信元グループID
    group_id = NULL
    #送信元ユーザーID
    user_id = event.source.user_id
    #送信されたメッセージ
    message_text = event.message.text

    if event.source.type == 'group':
        group_id = event.source.group_id
        CreateGroupsData(group_id)
        if group_id != "C9f5f4a30a5dd0a0f9c63579c09235d61":
            WithdrawalProcess(group_id)
    else:
        CreateUsersData(user_id)

    if group_id != NULL:
        if groups[group_id]["mode"]["modeName"] == "0":
            GroupModeChange(group_id, message_text)

        elif message_text == CommandList.EndCommand:
            # "終了"の場合
            ResetGroupModeData(group_id)
        else:
            GroupModeProcess(group_id, message_text)
 
    else:
        if users[user_id]["mode"]["modeName"] == "0":
            UserModeChange(user_id, message_text)
        elif message_text == CommandList.EndCommand:
            # "終了"の場合
            ResetUserModeData(user_id)
        
    # line_bot_api.reply_message(
    #    event.reply_token,
    #    TextSendMessage("aaaWorldnanodaaaabunjinnanoda"))
###

def GroupModeProcess(group_id, message_text):
    for mode in CommandList.GroupCommandList:
        eval(mode + "(message_text)")
    ResetGroupModeData(group_id)


def SendAll(message_text):
    line_bot_api.broadcast(messages = TextSendMessage(text = message_text))


def GroupModeChange(group_id, message_text):
    # (group_id)のモード変更
    for command in CommandList.GroupCommandList.values():
        if command == message_text:
            groups[group_id]["mode"]["modeName"] = command
            break

def UserModeChange(user_id, message_text):
    # (user_id)のモード変更
    for command in CommandList.UserCommandList.values():
        if command == message_text:
            users[user_id]["mode"]["modeName"] = command
            break


def CreateGroupsData(group_id):
    # グループを追加する
    if not group_id in groups:
        groups[group_id] = { }
        groups[group_id]["mode"] = { }
        ResetGroupModeData(group_id)

def CreateUsersData(user_id):  
    # ユーザーを追加する
    if not user_id in users:
        users[user_id] = { }
        users[user_id]["mode"] = { }
        ResetUserModeData(user_id)
    

def ResetGroupModeData(group_id):
    # グループのモード情報をリセットする
    groups[group_id]["mode"]["modeName"] = "0"
    groups[group_id]["mode"]["phase"] = 0
    groups[group_id]["mode"]["Messages"] = []
    

def ResetUserModeData(user_id):
    # ユーザーのモード情報をリセットする
    users[user_id]["mode"]["modeName"] = "0"
    users[user_id]["mode"]["phase"] = 0
    users[user_id]["mode"]["messages"] = []


def WithdrawalProcess(group_id):
    # 退会処理
    line_bot_api.leave_group(group_id)

    
if __name__ == "__main__":
    app.run()