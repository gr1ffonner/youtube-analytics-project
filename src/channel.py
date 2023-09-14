import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv("YOUTUBE_API_KEY")

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._data = self.get_info(channel_id)
        self._channel_id = channel_id
        self.title = self._data.get('snippet', {}).get('title', '')
        self.description = self._data.get('snippet', {}).get('description', '')
        self.url = f"https://www.youtube.com/channel/{self._channel_id}"
        self.subs = int(self._data.get('statistics', {}).get('subscriberCount', 0))
        self.video_count = self._data.get('statistics', {}).get('videoCount', 0)
        self.view_count = self._data.get('statistics', {}).get('viewCount', 0)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @staticmethod
    def get_info(channel_id: str) -> dict:
        youtube = Channel.get_service()
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return channel.get('items', [])[0] if 'items' in channel else {}

    def print_info(self) -> None:
        channel = self.get_info(self.channel_id)
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def to_json(self, file_path: str) -> None:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self._data, file, indent=2, ensure_ascii=False)

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __eq__(self, other):
        return self.subs == other.subs

    def __lt__(self, other):
        return self.subs < other.subs

    def __le__(self, other):
        return self.subs <= other.subs

    def __add__(self, other):
        if isinstance(other, Channel):
            return self.subs + other.subs
        raise TypeError("Unsupported operand type for +: 'Channel' and {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Channel):
            return self.subs - other.subs
        raise TypeError("Unsupported operand type for -: 'Channel' and {}".format(type(other)))

    @property
    def channel_id(self):
        return self._channel_id


# mosc_py_id = 'UC-OVMPlMA3-YCIeg4z5z23A'
# django_shcool_id = "UC_hPYclmFCIENpMUHpPY8FQ"
# moscowpython = Channel(mosc_py_id)
# django_shcool = Channel(django_shcool_id)


