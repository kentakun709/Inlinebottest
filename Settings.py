from linebot import (LineBotApi, WebhookHandler)

LINE_BOT_API = LineBotApi('RtimZ0mxW4QR8Ivf5zvnmo4TAMx446B9TVzL7K7j97F9993PPn79W3vuJc2pd2xATrm+uT31FXuJXU4Tzkns/wgOw/eURcv9QJaz3LrI66iViSoV0tO7E3nTZVxEVNKUmv12phYeIOwJZeayoNuczAdB04t89/1O/w1cDnyilFU=')
LINE_BOT_HANDLER = WebhookHandler('1b44e8b733146e212dbb1f1ffa4986a6')

# 一斉送信権限グループ
FORCE_GROUP_ID = "C9f5f4a30a5dd0a0f9c63579c09235d61"