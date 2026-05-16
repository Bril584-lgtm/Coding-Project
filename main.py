"""
TikTok Auto Poster — Motivational Quotes

Usage:
  python main.py              # Post one video now
  python main.py --schedule   # Auto-post on a schedule (3x/day)
  python main.py --preview    # Generate video locally without posting
"""

import os
import sys
import argparse
import tempfile
import time
from datetime import datetime
from dotenv import load_dotenv

import schedule

from quotes import get_random_quote, get_quote_by_index
from video_generator import generate_video
from tiktok_uploader import TikTokUploader

load_dotenv()

POST_TIMES = ["09:00", "14:00", "19:00"]  # 3 posts per day


def post_one(preview_only: bool = False, theme_index: int | None = None) -> None:
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

    try:
        uploader = TikTokUploader()
        publish_id = uploader.upload(output_path)
        print(f"Posted! Publish ID: {publish_id}")
    except ValueError as e:
        print(f"Upload skipped: {e}")
        print("Run `python tiktok_auth.py` to set up your TikTok credentials.")


def run_schedule() -> None:
    print(f"Scheduler started. Posting at: {', '.join(POST_TIMES)} daily.")
    for t in POST_TIMES:
        schedule.every().day.at(t).do(post_one)

    # Post immediately on start too
    post_one()

    while True:
        schedule.run_pending()
        time.sleep(30)


def main() -> None:
    parser = argparse.ArgumentParser(description="TikTok AI Quote Video Auto Poster")
    parser.add_argument("--schedule", action="store_true", help="Run on a posting schedule (3x/day)")
    parser.add_argument("--preview", action="store_true", help="Generate video without posting to TikTok")
    parser.add_argument("--theme", type=int, default=None, help="Color theme 0-4 (default: random)")
    args = parser.parse_args()

    if args.schedule:
        run_schedule()
    else:
        post_one(preview_only=args.preview, theme_index=args.theme)


if __name__ == "__main__":
    main()
