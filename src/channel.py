import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str, api_key: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.__api_key = api_key

    @staticmethod
    def yt_connection(self):
        youtube = build('youtube', 'v3', developerKey=self.__api_key)
        return youtube

    @staticmethod
    def get_info(self) -> dict:
        youtube = self.yt_connection(self)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        return channel

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_info(self)
        print(json.dumps(channel, indent=2, ensure_ascii=False))


api_key = os.getenv("YOUTUBE_API_KEY")
channel_id = 'UCwHL6WHUarjGfUM_586me8w'
ch = Channel(channel_id, api_key)
ch.print_info()