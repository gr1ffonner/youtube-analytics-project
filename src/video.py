import json
import os
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""
    api_key = os.getenv("YOUTUBE_API_KEY")

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._data = self.get_info(video_id)
        self._video_id = video_id
        self.title = self._data.get('snippet', {}).get('title', '')
        self.url = f"https://www.youtube.com/channel/{self._video_id}"
        self.like_count = self._data.get('statistics', {}).get('likeCount', 0)
        self.view_count = self._data.get('statistics', {}).get('viewCount', 0)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=cls.api_key)
        return youtube

    @staticmethod
    def get_info(video_id: str) -> dict:
        youtube = Video.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        return video_response.get('items', [])[0] if 'items' in video_response else {}

    def __str__(self):
        return self.title

class PLVideo(Video):
    """Класс для ютуб-видео"""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Initialize the PLVideo instance with video ID, playlist ID, and data from the YouTube API."""
        super().__init__(video_id)
        self.playlist_id = playlist_id

# vid_id = 'gaoc9MPZ4bw'
# video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
# print(str(video2))
# vid = Video(vid_id)
# # print(vid.title)
# # print(vid.url)
# # print(vid.like_count)
# # print(vid.view_count)
# # print(str(vid))
