import json
import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build


class Video:
    """Класс для ютуб-видео"""
    api_key = os.getenv("YOUTUBE_API_KEY")

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._data = self.get_info(video_id)
        if self._data == None:
            self._video_id = video_id
            self.title = None
            self.url = None
            self.like_count = None
            self.view_count = None
        else:
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
        try:
            video_response = video_response.get('items', [])[0]
            return video_response
        except IndexError:
            return None

    def __str__(self):
        return self.title

    def print_info(self) -> None:
        channel = self.get_info(self._video_id)
        print(json.dumps(channel, indent=2, ensure_ascii=False))

class PLVideo(Video):
    """Класс для ютуб-видео"""
    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Initialize the PLVideo instance with video ID, playlist ID, and data from the YouTube API."""
        super().__init__(video_id)
        self.playlist_id = playlist_id


class PlayList(Video):
    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self._data = self.get_playlist_info(playlist_id)
        self._playlist_id = playlist_id
        self.title = self._data.get('items')[0].get('snippet', {}).get('title', '')
        self.url = f"https://www.youtube.com/playlist?list={self._playlist_id}"

    @staticmethod
    def get_info_about_videos_in_playlist(playlist_id: str) -> dict:
        youtube = PlayList.get_service()

        playlist_with_videos_response = youtube.playlistItems().list(playlistId=playlist_id,
                                               part='contentDetails, snippet',
                                               maxResults=50,
                                               ).execute()
        return playlist_with_videos_response

    @staticmethod
    def get_playlist_info(playlist_id: str) -> dict:
        youtube = PlayList.get_service()

        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()

        return playlist_response

    @property
    def duration(self) -> timedelta:
        total_duration_seconds = 0

        # Get the list of videos in the playlist
        playlist_items = self.get_info_about_videos_in_playlist(self._playlist_id)

        # Iterate over each video and sum up their durations
        for item in playlist_items['items']:
            video_id = item['contentDetails']['videoId']
            video_info = self.get_info(video_id)
            video_duration_iso = video_info['contentDetails']['duration']
            video_duration = isodate.parse_duration(video_duration_iso)
            total_duration_seconds += video_duration.total_seconds()
        return timedelta(seconds=total_duration_seconds)

    def show_best_video(self) -> str:
        # Get the list of videos in the playlist
        playlist_items = self.get_info_about_videos_in_playlist(self._playlist_id)

        best_video = None
        max_likes = 0

        # Iterate over each video and find the one with the most likes
        for item in playlist_items['items']:
            video_id = item['contentDetails']['videoId']
            video_info = self.get_info(video_id)
            video_likes = int(video_info['statistics']['likeCount'])

            if video_likes > max_likes:
                max_likes = video_likes
                best_video = video_id

        if best_video:
            return f"https://www.youtube.com/watch?v={best_video}"

        return "No videos found in the playlist."

# vid_id = 'alsdkfji'
# # video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
# # print(str(video2))
# # vid = Video(vid_id)
# # # print(vid._video_id)
# vid.print_info()
# print(vid.title)
# print(vid.url)
# print(vid.like_count)
# print(vid.view_count)
# # print(str(vid))
# pl = PlayList('PLRDzFCPr95fK7tr47883DFUbm4GeOjjc0')
# pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
# duration = pl.duration
# print(str(duration))
# print(duration.total_seconds())
# print(pl.show_best_video())
# print(pl.url)
# print(pl.title)
# print(pl.url)
# print(str(pl.duration))
# print(isinstance(pl.duration, datetime.timedelta))
# print(pl.show_best_video())