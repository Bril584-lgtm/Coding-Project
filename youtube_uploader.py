"""
Uploads a video to YouTube as a Short.
"""

import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

from youtube_auth import authenticate, TOKEN_FILE


class YouTubeUploader:
    def __init__(self):
        if not os.path.exists(TOKEN_FILE):
            raise ValueError("YouTube not authorized. Run `python youtube_auth.py` first.")
        self.creds = authenticate()
        self.youtube = build("youtube", "v3", credentials=self.creds)

    def upload(self, video_path: str, title: str = "", description: str = "") -> str:
        if not title:
            title = "Motivational Quote of the Day #Shorts"
        if not description:
            description = (
                "Daily motivational quote to keep you inspired. "
                "#Shorts #Motivation #Quotes #AIGenerated"
            )

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["motivation", "quotes", "shorts", "AI", "inspiration"],
                "categoryId": "22",  # People & Blogs
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            },
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")

        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )

        response = None
        while response is None:
            _, response = request.next_chunk()

        video_id = response.get("id", "")
        print(f"YouTube Shorts URL: https://youtube.com/shorts/{video_id}")
        return video_id
