# TikTok AI Quote Video Auto Poster

Automatically generates motivational quote videos and posts them to TikTok using AI voiceover and animated text.

## What it does

- Picks a random motivational quote
- Generates a TikTok-format (1080x1920) video with animated text and gradient background
- Adds AI voiceover (Google TTS free, or ElevenLabs for premium voices)
- Uploads directly to TikTok via their Content Posting API
- Can run on a schedule (3 posts/day by default)

## Setup

### 1. Install Python

Requires **Python 3.9 or newer**.

- **Windows**: Download from [python.org](https://www.python.org/downloads/) — check "Add Python to PATH" during install
- **macOS**: `brew install python` or download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)

### 2. Install ffmpeg

ffmpeg is required to encode video files.

```bash
# Windows (pick one)
winget install ffmpeg
choco install ffmpeg        # if you have Chocolatey
# Or download manually: https://ffmpeg.org/download.html → Windows builds → add to PATH

# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Fedora / RHEL
sudo dnf install ffmpeg
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

On Linux, if you hit font-related errors:
```bash
sudo apt install fonts-dejavu fonts-liberation
```

### 4. Verify your setup

```bash
python check_setup.py
```

This checks Python version, packages, ffmpeg, fonts, and your `.env` — run it any time something seems off.

### 5. Get TikTok API credentials

1. Go to [developers.tiktok.com](https://developers.tiktok.com/) and sign in
2. Click **Manage apps** → **Create app**
3. Fill in app name, description, select **Web** as platform
4. Under **Products**, add **Content Posting API**
5. Set **Redirect URI** to `http://localhost:8080/callback`
6. Copy your **Client Key** and **Client Secret**

### 6. Configure environment

**Mac / Linux:**
```bash
cp .env.example .env
```

**Windows (Command Prompt):**
```cmd
copy .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your `TIKTOK_CLIENT_KEY` and `TIKTOK_CLIENT_SECRET`.

### 7. Authorize your TikTok account

```bash
python tiktok_auth.py
```

This opens TikTok in your browser, you log in and approve, and your access token is saved automatically.

### 8. Run it

```bash
# Generate and post one video now
python main.py

# Preview only (no upload)
python main.py --preview

# Auto-post 3x per day on a schedule
python main.py --schedule

# Use a specific color theme (0-4)
python main.py --theme 2
```

## Optional Upgrades

### Better AI voices (ElevenLabs)
1. Sign up at [elevenlabs.io](https://elevenlabs.io/) (free tier available)
2. Copy your API key to `.env` as `ELEVENLABS_API_KEY`

### Change posting schedule

Edit `POST_TIMES` in `main.py`:
```python
POST_TIMES = ["08:00", "13:00", "20:00"]
```

### Add your own quotes

Edit `quotes.py` and add to the `QUOTES` list:
```python
("Your quote here.", "Author Name"),
```

## File structure

```
├── main.py              # Entry point + scheduler
├── video_generator.py   # Creates the video with text + audio
├── tiktok_uploader.py   # TikTok API upload logic
├── tiktok_auth.py       # One-time OAuth setup
├── quotes.py            # Quote database
├── check_setup.py       # Verifies your environment is ready
├── requirements.txt
└── .env.example
```

## Notes

- Videos are saved to `output_videos/` locally before uploading
- First posts default to `SELF_ONLY` privacy — change to `PUBLIC_TO_EVERYONE` in `tiktok_uploader.py` when ready
- TikTok requires AI-generated content to be labeled — the watermark is included automatically