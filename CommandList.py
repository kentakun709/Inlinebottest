from enum import Enum

class GroupCommandList(Enum):
    SendAll = "一斉送信"
    
class UserCommandList(Enum):
    hoge = "hoge"

EndCommand = {
    "終了",
    "Exit"
}