import requests

from bot.tg.dc import GetUpdatesResponse
from bot.tg.dc import SendMessageResponse


class TgClient:
    """Клиент по работе с телеграм ботом"""
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0,
                    timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        resp = requests.get(url, params={"offset": offset, "timeout": timeout})
        return GetUpdatesResponse.Schema().load(resp.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")

        json_data = {"chat_id": chat_id, "text": text}

        resp = requests.post(url, json=json_data)
        return SendMessageResponse.Schema().load(resp.json())
