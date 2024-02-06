import os
import sys
from typing import List, Tuple

import requests
from dotenv import load_dotenv

from dataclasses import dataclass

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
load_dotenv()


@dataclass
class Channel:
    id: int
    name: str
    custom_id: int

    def is_local(self) -> bool:
        return self.custom_id > 99999 and self.custom_id < 200000


@dataclass
class Music:
    title: str
    artists: List[str]
    timestamp: str
    played_duration: int


TOKEN = os.getenv("TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")


def get_channels() -> List[Channel]:
    url = "https://api-v2.acrcloud.com/api/" f"bm-bd-projects/{PROJECT_ID}/channels"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    response = requests.get(url, headers=headers)
    json = response.json()
    channels = []
    for data in json["data"]:
        channel = Channel(
            data["id"],
            data["name"],
            int(data["user_defined"]["id"]) if len(data["user_defined"]) > 0 else 0,
        )
        channels.append(channel)
    return channels


def get_musics(channel_id: int) -> List[Music]:
    url = (
        "https://api-v2.acrcloud.com/api/bm-bd-projects/"
        f"{PROJECT_ID}/channels/{channel_id}/results"
    )
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {TOKEN}",
    }

    response = requests.get(url, headers=headers)
    json = response.json()
    musics = []
    for data in json["data"]:
        timestamp = data["metadata"]["timestamp_utc"]
        played_duration = data["metadata"]["played_duration"]
        for music in data["metadata"]["music"]:
            title = music["title"]
            artists = [artist["name"] for artist in music["artists"]]
            music = Music(title, artists, timestamp, played_duration)
            musics.append(music)

    return musics


def search_musics(
    channel: Channel, musics: List[Music], title_query: str, artist_query: str
) -> Tuple[int, int]:
    founds = []
    for music in musics:
        if title_query and title_query.lower() in music.title.lower():
            founds.append(music)
        elif artist_query and artist_query.lower() in [
            artist.lower() for artist in music.artists
        ]:
            founds.append(music)
    return founds
