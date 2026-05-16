"""
TikTok Content Posting API wrapper.

Setup guide:
1. Go to https://developers.tiktok.com/ and create an app
2. Enable the "Content Posting API" product
3. Set redirect URI to http://localhost:8080/callback
4. Run `python tiktok_auth.py` to get your access token
5. Add the token to your .env file
"""

import os
import time
import math
import requests


TIKTOK_API_BASE = "https://open.tiktokapis.com/v2"
CHUNK_SIZE = 10 * 1024 * 1024  # 10MB chunks


class TikTokUploader:
    def __init__(self):
        self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("TIKTOK_ACCESS_TOKEN not set in environment. Run tiktok_auth.py first.")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=UTF-8",
        }

    def _init_upload(self, file_size: int, chunk_count: int) -> dict:
        payload = {
            "post_info": {
                "title": self._build_caption(),
                "privacy_level": "SELF_ONLY",  # change to PUBLIC_TO_EVERYONE when ready
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": CHUNK_SIZE,
                "total_chunk_count": chunk_count,
            },
        }
        resp = requests.post(
            f"{TIKTOK_API_BASE}/post/publish/video/init/",
            headers=self._headers(),
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["data"]

    def _upload_chunk(self, upload_url: str, chunk_data: bytes, chunk_index: int, total_size: int) -> None:
        start = chunk_index * CHUNK_SIZE
        end = min(start + len(chunk_data) - 1, total_size - 1)
        headers = {
            "Content-Range": f"bytes {start}-{end}/{total_size}",
            "Content-Type": "video/mp4",
            "Content-Length": str(len(chunk_data)),
        }
        resp = requests.put(upload_url, headers=headers, data=chunk_data, timeout=120)
        resp.raise_for_status()

    def _check_status(self, publish_id: str) -> str:
        resp = requests.post(
            f"{TIKTOK_API_BASE}/post/publish/status/fetch/",
            headers=self._headers(),
            json={"publish_id": publish_id},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["data"]["status"]

    def _build_caption(self) -> str:
        tags = "#motivation #mindset #success #dailymotivation #quotes #inspire #fyp #foryou"
        return f"Daily motivation to keep you going! {tags}"

    def upload(self, video_path: str) -> str:
        """Upload a video to TikTok. Returns the publish_id."""
        file_size = os.path.getsize(video_path)
        chunk_count = math.ceil(file_size / CHUNK_SIZE)

        print(f"Initializing upload: {file_size / 1024 / 1024:.1f}MB, {chunk_count} chunk(s)")
        init_data = self._init_upload(file_size, chunk_count)
        upload_url = init_data["upload_url"]
        publish_id = init_data["publish_id"]

        with open(video_path, "rb") as f:
            for i in range(chunk_count):
                chunk = f.read(CHUNK_SIZE)
                print(f"Uploading chunk {i + 1}/{chunk_count}...")
                self._upload_chunk(upload_url, chunk, i, file_size)

        # Poll for completion (up to 2 minutes)
        print("Waiting for TikTok to process video...")
        for _ in range(24):
            status = self._check_status(publish_id)
            print(f"Status: {status}")
            if status == "PUBLISH_COMPLETE":
                print("Video published successfully!")
                return publish_id
            if status in ("FAILED", "SPAM_RISK_TOO_MANY_POSTS", "SPAM_RISK_USER_BANNED_FROM_POSTING"):
                raise RuntimeError(f"Upload failed with status: {status}")
            time.sleep(5)

        raise TimeoutError("Video processing timed out after 2 minutes")
