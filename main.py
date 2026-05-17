"""
AI Quote Video Auto Poster — TikTok & YouTube Shorts

Usage:
  python main.py                        # Post to all configured platforms
  python main.py --platform tiktok      # TikTok only
  python main.py --platform youtube     # YouTube Shorts only
  python main.py --schedule             # Auto-post 3x/day
  python main.py --preview              # Generate video without posting
"""

import os
import argparse
import time
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

import schedule

from quotes import get_random_quote
from video_generator import generate_video
from tiktok_uploader import TikTokUploader
from youtube_uploader import YouTubeUploader

load_dotenv()

POST_TIMES = ["09:00", "14:00", "19:00"]  # 3 posts per day


def post_one(
    preview_only: bool = False,
    theme_index: Optional[int] = None,
    platform: str = "all",
) -> None:
    quote, author = get_random_quote()
    theme = theme_index if theme_index is not None else int(time.time()) % 5

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Generating video...")
    print(f'Quote: "{quote}" — {author}')

    output_dir = "output_videos"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, f"quote_{timestamp}.mp4")

    generate_video(quote, author, output_path, theme_index=theme)
    print(f"Video saved: {output_path}")

    if preview_only:
        print("Preview mode — skipping upload.")
        return

    if platform in ("all", "tiktok"):
        try:
            uploader = TikTokUploader()
            publish_id = uploader.upload(output_path)
            print(f"TikTok posted! Publish ID: {publish_id}")
        except ValueError as e:
            print(f"TikTok skipped: {e}")
            print("Run `python tiktok_auth.py` to set up TikTok credentials.")

    if platform in ("all", "youtube"):
        try:
            uploader = YouTubeUploader()
            title = f'"{quote}" — {author} #Shorts'[:100]
            uploader.upload(output_path, title=title)
        except ValueError as e:
            print(f"YouTube skipped: {e}")
            print("Run `python youtube_auth.py` to set up YouTube credentials.")


def run_schedule(platform: str = "all") -> None:
    print(f"Scheduler started. Posting at: {', '.join(POST_TIMES)} daily.")
    for t in POST_TIMES:
        schedule.every().day.at(t).do(post_one, platform=platform)

    post_one(platform=platform)

    while True:
        schedule.run_pending()
        time.sleep(30)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Quote Video Auto Poster")
    parser.add_argument("--schedule", action="store_true", help="Run on a posting schedule (3x/day)")
    parser.add_argument("--preview", action="store_true", help="Generate video without posting")
    parser.add_argument("--theme", type=int, default=None, help="Color theme 0-4 (default: random)")
    parser.add_argument(
        "--platform",
        choices=["all", "tiktok", "youtube"],
        default="all",
        help="Platform to post to (default: all)",
    )
    args = parser.parse_args()

    if args.schedule:
        run_schedule(platform=args.platform)
    else:
        post_one(preview_only=args.preview, theme_index=args.theme, platform=args.platform)


if __name__ == "__main__":
    main()
