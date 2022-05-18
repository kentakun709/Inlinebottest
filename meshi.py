from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage,ConfirmTemplate, TextSendMessage,TemplateSendMessage,ButtonsTemplate,PostbackAction,MessageAction,URIAction, template,
)
from linebot.models.messages import ImageMessage
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__)
import random

line_bot_api = LineBotApi('1ONwZnVgjbH/AWZnLDciC1mqJUeoBysS+zFnR7fGDoFDqoTQ8mMhg4nHX8/utS+vK7AMYvaQZFXhtkL7xr53joqFSB6zIzXv8lODgSj5Np6oLx2j44nnRL1yeJ9VXlqvFT6WWXBk2Bg2wkFq57gFyAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c2de10007b29c7ef76a4a14111ee8288')

def make_button_template():
    message_template = TemplateSendMessage(
        alt_text="にゃーん",
        template=ButtonsTemplate(
            text="どこに表示されるかな？",
            title="タイトルですよ",
            image_size="cover",
            thumbnail_image_url="https://任意の画像URL.jpg",
            actions=[
                URIAction(
                    uri="https://任意のページURL",
                    label="URIアクションのLABEL"
                )
            ]
        )
    )
    return message_template


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

from time import time
start = {}
users = {}
global mode
global food
global weight
global a
"""
class Person:
    def__init__(id,mo):
        self.id=user_id
        self.mo=modeaaaaaaaaaaaa"""

def sample():
  # 関数が呼び出された場合に何もしないようにPass文を設定
  pass

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    mesage_text = event.message.text
 
    if not user_id in users:
        # ユーザーを追加する
        users[user_id] = {}
        users[user_id]["mode"] = 0
        users[user_id]["food"]=[]
        users[user_id]["weight"]=[]

    if users[user_id]["mode"] == 0:
        # mode が 0 のとき (なにもないとき)
        if mesage_text == "稲員健太":
            reply_message ="私のマスターです"
        if mesage_text == "高橋":
            reply_message ="テニスしようぜ"
        if event.message.text == "退会して":
            reply_message="うっうっ"

            #グループトークからの退出処理
            if hasattr(event.source,"group_id"):
                line_bot_api.leave_group(event.source.group_id)

            #ルームからの退出処理
            if hasattr(event.source,"room_id"):
                line_bot_api.leave_room(event.source.room_id)
            
        elif mesage_text == "開始":
            reply_message ="計測を開始します"
            users[user_id]["total"]=0
            users[user_id]["start"] =time() 
        elif mesage_text == "終了":
            end = time()
            differnce = int(end-users[user_id]["start"])
            users[user_id]["total"]+= differnce
            hour = differnce //3600
            minute=differnce%3600//60
            second=differnce%60
            reply_message=f"使用時間は{hour}時間{minute}分{second}秒です。合計使用時間は{users[user_id]['total']}秒 "

        elif mesage_text == "メニュー":
            users[user_id]["mode"]=1
            #mode=1 から変更
            reply_message ="登録モードに移行します。メニュー名を入力してください"

        elif  mesage_text == "停止":
            reply_message ="プログラムを停止します、再開する場合はプログラム起動と言ってください"
            users[user_id]["mode"]=2

        elif  mesage_text == "測定":
            reply_message ="体重を入力してください"
            users[user_id]["mode"]=3

        elif  mesage_text == "システムコマンド":
            reply_message ="管理者パスワードを入力してください"
            users[user_id]["mode"]=4

        elif  mesage_text == "テストテストよしとよしと":
            reply_message ="そりゃやーんちゃ"
            users[user_id]["mode"]=6

        elif  mesage_text == "今日のご飯":
            a=random.choice(users[user_id]["food"])
            reply_message =f"{a}はどうですか？"

        else:
            reply_message =f"すみません私は{mesage_text}の意味が分かりませんww"

    elif users[user_id]["mode"] == 1:
        if mesage_text == "登録終了": 
            reply_message =f"登録モードを終了するで"
            users[user_id]["mode"]=0
        else:
            #こっから変更点
            # mode が 1 のとき (メニューを追加しかけてる)
            # ここの message_text にメニューの名前が入ってくるはず
            users[user_id]["food"].append(mesage_text)
            reply_message =f"{mesage_text}ですね"
            reply_message =f"終了する場合は登録終了と言ってください。続けて登録する場合はメニュー名を入力してください。"
            print(users[user_id]["food"])
            #問題点

    elif users[user_id]["mode"] == 2:
        if mesage_text == "プログラム起動":
            reply_message =f"プログラム起動します"
            users[user_id]["mode"]=0
        #else:
            #sample()

    elif users[user_id]["mode"] == 3:
        if mesage_text == "測定終了":
            reply_message =f"プログラム起動します"
            users[user_id]["mode"]=0
        
        else:
            #こっから変更点
            # mode が 1 のとき (メニューを追加しかけてる)
            # ここの message_text にメニューの名前が入ってくるはず
            users[user_id]["weight"].append(mesage_text)
            plt.plot(users[user_id]["weight"])
            plt.show()
            reply_message =f"{mesage_text}ですね"
            print(users[user_id]["weight"])

    elif users[user_id]["mode"] == 4:
        if not user_id=="Ue3c1ffa7d34bc0eb4fb6b41572502312":
            reply_message=f"適正ユーザーではありません"
            users[user_id]["mode"]=0
            
        else:
            reply_message =f"適正ユーザーです。一斉送信の内容を入力してください"
            users[user_id]["mode"]=5

    elif users[user_id]["mode"] == 5:
        messages = TextSendMessage(text=f"マスターからの伝言です{mesage_text}")
        line_bot_api.broadcast(messages=messages)
        users[user_id]["mode"]=0

    elif users[user_id]["mode"] == 6:
        def handle_image_message(event):
            message= make_button_template()
            line_bot_api.reply_message(
                event.reply_token,
                messages
            )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))
        

@handler.add(MessageEvent, message=(ImageMessage))
def handle_image_message(event):
    messages = make_button_template()
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )
    



        
if __name__ == "__main__":
    app.run()

   
