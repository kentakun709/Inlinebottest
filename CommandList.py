from enum import Enum

class GroupCommandList(Enum):
    SendAll = "一斉送信"
    
class UserCommandList(Enum):
    Reserve = "予約"

EndCommand = {
    "終了",
    "EXIT",
    "Exit",
    "exit"
}