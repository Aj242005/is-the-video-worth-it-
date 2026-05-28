'''YouTube transcript extraction controllers.'''

from typing import Any, cast
from models import Yturl
import yt_dlp
import os
from requests.exceptions import RetryError
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, IpBlocked
from youtube_transcript_api.proxies import WebshareProxyConfig


def _transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    try:
        return " ".join(s.text for s in api.fetch(video_id, languages=["en", "hi"]))
    except (NoTranscriptFound, TranscriptsDisabled, IpBlocked, RetryError) as e:
        print(f"[transcript] {type(e).__name__}: {e}")
        return "No transcript found."


def handle_url_and_prompt(yt_object: Yturl) -> str | dict[str, str]:
    '''Main entry point controller.'''
    url = yt_object.url.strip()
    opts: dict[str, Any] = {"skip_download": True, "quiet": True, "extract_flat": True}

    with yt_dlp.YoutubeDL(cast(Any, opts)) as ydl:
        info = ydl.extract_info(url, download=False)

    if info.get("_type") == "playlist" or "entries" in info:
        return {
            (e.get("title") or e.get("id") or "Unknown"): _transcript(e["id"])
            for e in info.get("entries", [])
            if e and e.get("id")
        }

    return _transcript(cast(dict, info)["id"])
