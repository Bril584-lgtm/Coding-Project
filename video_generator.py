import os
import sys
import textwrap
import tempfile
from pathlib import Path

# Auto-configure bundled ffmpeg before moviepy loads — no system install needed
try:
    import imageio_ffmpeg
    os.environ.setdefault("IMAGEIO_FFMPEG_EXE", imageio_ffmpeg.get_ffmpeg_exe())
except Exception:
    pass

from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
)
import numpy as np


# TikTok vertical format
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30

# Video length limits (seconds)
MIN_DURATION = 15.0
MAX_DURATION = 30.0
FADE_DURATION = 1.0  # fade-in and fade-out length

# Color themes (background_start, background_end, text_color, author_color)
THEMES = [
    ((15, 15, 35), (40, 0, 80), (255, 255, 255), (180, 180, 255)),
    ((10, 30, 10), (0, 70, 40), (255, 255, 255), (150, 255, 180)),
    ((40, 10, 0), (90, 30, 0), (255, 255, 255), (255, 200, 120)),
    ((10, 10, 50), (0, 30, 90), (255, 255, 255), (120, 200, 255)),
    ((50, 0, 30), (100, 0, 60), (255, 255, 255), (255, 150, 200)),
]


def _make_gradient_bg(color_start: tuple, color_end: tuple) -> np.ndarray:
    img = np.zeros((VIDEO_HEIGHT, VIDEO_WIDTH, 3), dtype=np.uint8)
    for y in range(VIDEO_HEIGHT):
        ratio = y / VIDEO_HEIGHT
        r = int(color_start[0] * (1 - ratio) + color_end[0] * ratio)
        g = int(color_start[1] * (1 - ratio) + color_end[1] * ratio)
        b = int(color_start[2] * (1 - ratio) + color_end[2] * ratio)
        img[y, :] = [r, g, b]
    return img


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    if sys.platform == "win32":
        win_fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        candidates = [
            os.path.join(win_fonts, "arialbd.ttf" if bold else "arial.ttf"),
            os.path.join(win_fonts, "verdanab.ttf" if bold else "verdana.ttf"),
            os.path.join(win_fonts, "calibrib.ttf" if bold else "calibri.ttf"),
            os.path.join(win_fonts, "trebucbd.ttf" if bold else "trebuc.ttf"),
        ]
    elif sys.platform == "darwin":
        candidates = [
            "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Microsoft/Arial Bold.ttf" if bold else "/Library/Fonts/Microsoft/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
        ]

    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    # Last resort: Pillow's bundled bitmap font (no size control, but always works)
    return ImageFont.load_default()


def _draw_text_frame(
    quote: str,
    author: str,
    theme_index: int = 0,
    progress: float = 0.0,
) -> np.ndarray:
    theme = THEMES[theme_index % len(THEMES)]
    bg_array = _make_gradient_bg(theme[0], theme[1])
    img = Image.fromarray(bg_array)
    draw = ImageDraw.Draw(img)

    # Decorative top accent line
    accent_color = theme[3]
    line_width = int(VIDEO_WIDTH * 0.6)
    line_x = (VIDEO_WIDTH - line_width) // 2
    draw.rectangle([line_x, 180, line_x + line_width, 186], fill=accent_color)

    # Quotation mark
    quote_font = _get_font(160, bold=True)
    draw.text((VIDEO_WIDTH // 2 - 40, 200), "“", font=quote_font, fill=(*accent_color, 60))

    # Quote text — wrap to fit width
    font_size = 68
    quote_font = _get_font(font_size, bold=True)
    max_chars = 28
    wrapped = textwrap.fill(quote, width=max_chars)
    lines = wrapped.split("\n")

    total_text_height = len(lines) * (font_size + 16)
    start_y = (VIDEO_HEIGHT - total_text_height) // 2 - 80

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=quote_font)
        text_w = bbox[2] - bbox[0]
        x = (VIDEO_WIDTH - text_w) // 2
        y = start_y + i * (font_size + 16)
        # Subtle shadow
        draw.text((x + 3, y + 3), line, font=quote_font, fill=(0, 0, 0, 80))
        draw.text((x, y), line, font=quote_font, fill=theme[2])

    # Author name
    if author and author != "Unknown":
        author_font = _get_font(44)
        author_text = f"— {author}"
        bbox = draw.textbbox((0, 0), author_text, font=author_font)
        text_w = bbox[2] - bbox[0]
        x = (VIDEO_WIDTH - text_w) // 2
        y = start_y + total_text_height + 50
        draw.text((x, y), author_text, font=author_font, fill=accent_color)

    # Bottom accent line
    draw.rectangle([line_x, VIDEO_HEIGHT - 186, line_x + line_width, VIDEO_HEIGHT - 180], fill=accent_color)

    # AI disclosure watermark (required by TikTok)
    small_font = _get_font(32)
    draw.text((40, VIDEO_HEIGHT - 100), "AI Generated", font=small_font, fill=(150, 150, 150))

    # Progress bar at bottom
    bar_width = int(VIDEO_WIDTH * progress)
    draw.rectangle([0, VIDEO_HEIGHT - 12, bar_width, VIDEO_HEIGHT], fill=accent_color)

    return np.array(img)


def _generate_voiceover(text: str, output_path: str, use_elevenlabs: bool = False) -> None:
    api_key = os.getenv("ELEVENLABS_API_KEY", "")

    if use_elevenlabs and api_key:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import save

        client = ElevenLabs(api_key=api_key)
        audio = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_multilingual_v2",
        )
        save(audio, output_path)
    else:
        tts = gTTS(text=text, lang="en", slow=False)
        tts.save(output_path)


def _fade_alpha(t: float, total: float) -> float:
    """Returns opacity 0→1 at start, 1→0 at end, 1.0 in the middle."""
    if t < FADE_DURATION:
        return t / FADE_DURATION
    if t > total - FADE_DURATION:
        return max(0.0, (total - t) / FADE_DURATION)
    return 1.0


def generate_video(quote: str, author: str, output_path: str, theme_index: int = 0) -> str:
    """Generate a TikTok-formatted motivational quote video. Returns the output path."""

    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_path = os.path.join(tmp_dir, "voiceover.mp3")

        spoken_text = f"{quote}... by {author}" if author and author != "Unknown" else quote
        _generate_voiceover(spoken_text, audio_path, use_elevenlabs=bool(os.getenv("ELEVENLABS_API_KEY")))

        audio_clip = AudioFileClip(audio_path)

        # Clamp total video length to 15–30 seconds.
        # Audio plays first; remaining time holds the quote on screen.
        duration = float(np.clip(audio_clip.duration + 3.0, MIN_DURATION, MAX_DURATION))
        print(f"Video duration: {duration:.1f}s  (audio: {audio_clip.duration:.1f}s)")

        def make_frame(t: float) -> np.ndarray:
            progress = min(t / duration, 1.0)
            frame = _draw_text_frame(quote, author, theme_index, progress)
            alpha = _fade_alpha(t, duration)
            if alpha < 1.0:
                frame = (frame.astype(np.float32) * alpha).astype(np.uint8)
            return frame

        video_clip = ImageClip(make_frame(0)).set_duration(duration)
        video_clip = video_clip.set_make_frame(make_frame)
        video_clip = video_clip.set_audio(audio_clip)

        video_clip.write_videofile(
            output_path,
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile=os.path.join(tmp_dir, "temp_audio.m4a"),
            remove_temp=True,
            logger=None,
        )

    return output_path
