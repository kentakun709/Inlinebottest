import CommandList
import Settings

from asyncio.windows_events import NULL
from flask import Flask, request, abort

from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

app = Flask(__name__)
    
if __name__ == "__main__":
    app.run()


LINE_BOT_API = Settings.LINE_BOT_API
LINE_BOT_HANDLER = Settings.LINE_BOT_HANDLER

# 一斉送信権限グループ
FORCE_GROUP_ID = Settings.FORCE_GROUP_ID

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        LINE_BOT_HANDLER.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


""""""
# 揮発性ユーザーデータ
users = { }

# 揮発性グループデータ
groups = { }


###
@LINE_BOT_HANDLER.add(MessageEvent, message=TextMessage)
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
        if group_id != FORCE_GROUP_ID:
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
###

def GroupModeProcess(group_id, message_text):
    for mode in CommandList.GroupCommandList:
        eval(mode + "(group_id, message_text)")


def SendAll(group_id, message_text):
    LINE_BOT_API.broadcast(messages = TextSendMessage(text = message_text))
    ResetGroupModeData(group_id)


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
    LINE_BOT_API.leave_group(group_id)