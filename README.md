# TikTok AI Quote Video Auto Poster

Automatically generates motivational quote videos and posts them to TikTok.
Works on **Windows 10/11**, **macOS**, and **Linux**.

No prior coding experience required — follow the steps below exactly.

---

## What it does

- Picks a random motivational quote from a built-in library
- Generates a 1080×1920 vertical video with a gradient background, styled text, and AI voiceover
- Uploads directly to TikTok via their official API
- Can post automatically on a schedule (default: 3 times per day)

---

## What you need before starting

- A computer running Windows 10/11, macOS, or Linux
- A TikTok account (regular account is fine)
- An internet connection
- About 15–20 minutes for first-time setup

---

## Part 1 — Install Python

Python is the programming language this runs on. You need version **3.9 or newer**.

### Windows 10 / Windows 11

> **Before you start — important Windows gotcha:**
> On Windows 10 and 11, typing `python` in the Command Prompt might open the **Microsoft Store** instead of running Python. This means Python is **not** installed yet. Do **not** install Python from the Store — follow the steps below instead.

1. Go to **https://www.python.org/downloads/**
2. Click the big yellow **Download Python 3.x.x** button
3. Run the downloaded `.exe` installer
4. **CRITICAL — do not skip this:** On the very first screen of the installer, at the bottom, check the box that says **"Add Python to PATH"**

   ![Add Python to PATH checkbox must be checked]

5. Click **Install Now** and wait for it to finish (about 1–2 minutes)
6. Click **Close** when done
7. Verify it worked — open **Command Prompt** (press `Windows key`, type `cmd`, press Enter) and run:
   ```
   python --version
   ```
   You should see `Python 3.x.x`. If you see an error or the Store opens, restart your computer and try again.

> **If you already have Python but it's older than 3.9:** Download and install the latest version from python.org. Multiple versions can coexist safely.

### macOS

**Option A — Homebrew (recommended):**

1. Open **Terminal** (search in Spotlight with Cmd+Space)
2. Install Homebrew if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python
   ```
4. Verify:
   ```bash
   python3 --version
   ```

**Option B — Direct download:**

1. Go to **https://www.python.org/downloads/**
2. Download and run the macOS installer
3. Open **Terminal** and verify:
   ```bash
   python3 --version
   ```

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### Linux (Fedora / RHEL)

```bash
sudo dnf install python3 python3-pip
python3 --version
```

---

## Part 2 — Download this project

### Option A — Using Git (recommended)

If you have Git installed:

```bash
git clone https://github.com/Bril584-lgtm/Coding-Project.git
cd Coding-Project
```

### Option B — Download ZIP

1. Go to **https://github.com/Bril584-lgtm/Coding-Project**
2. Click the green **Code** button
3. Click **Download ZIP**
4. Extract the ZIP file somewhere easy to find (like your Desktop)
5. Open the extracted folder

---

## Part 3 — Run the setup script

This installs everything automatically. **You only do this once.**

### Windows 10 / Windows 11

1. Open the project folder in **File Explorer**
2. Double-click **`setup.bat`**
3. A black Command Prompt window opens and installs everything automatically
4. Wait until it says **"Setup complete!"** — this takes 2–5 minutes depending on your internet speed
5. Press any key to close the window

**If you see a blue "Windows protected your PC" popup (SmartScreen):**
- Click **"More info"** (the small text link)
- Then click **"Run anyway"**
- This is normal for downloaded scripts — the program is safe

**If Windows asks "Do you want to allow this app to make changes to your device?":**
- Click **Yes** — this is the standard permission prompt for running setup scripts

**If the window closes instantly with an error:**
- Right-click `setup.bat` → **Run as administrator**
- If it still fails, open Command Prompt (`Windows key` → type `cmd` → Enter), navigate to the project folder with `cd Desktop\Coding-Project`, then type `setup.bat`

### macOS / Linux

1. Open **Terminal**
2. Navigate to the project folder:
   ```bash
   cd ~/Desktop/Coding-Project
   ```
   *(adjust the path to wherever you put the folder)*
3. Run the setup script:
   ```bash
   bash setup.sh
   ```
4. Wait until it says "Setup complete!" — this takes 2–5 minutes

> On Linux, the script will ask for your password to install fonts. Type it and press Enter (the password won't appear as you type — that's normal).

---

## Part 4 — Get TikTok API credentials

This lets the program log into your TikTok account and post videos.

1. Go to **https://developers.tiktok.com/** and sign in with your TikTok account

2. Click **Manage apps** in the top menu

3. Click **Create app**

4. Fill in the form:
   - **App name:** anything you want (e.g. "My Quote Poster")
   - **App description:** "Automatically posts motivational quote videos"
   - **Platform:** select **Web**
   - **Category:** Entertainment

5. After creating the app, you'll see your app dashboard. Under **Products**, find **Content Posting API** and click **Add**

6. Scroll down to find **Redirect URI / Redirect domain** and add:
   ```
   http://localhost:8080/callback
   ```
   Click **Add** or **Save**

7. At the top of the app dashboard, copy:
   - **Client Key** (sometimes called "App ID")
   - **Client Secret** (sometimes called "App Secret")

   Keep these handy — you'll need them in the next step.

---

## Part 5 — Add your credentials to the .env file

The `.env` file is where you store your private keys. **Never share this file with anyone.**

1. Open the project folder
2. Find the file named **`.env`** (it was created by the setup script)
   - On Windows: it might be hidden. In File Explorer, go to View → check "Hidden items"
   - On Mac: press Cmd+Shift+. to show hidden files
3. Open it with any text editor (Notepad on Windows, TextEdit on Mac, or nano/gedit on Linux)
4. It looks like this:
   ```
   TIKTOK_CLIENT_KEY=your_client_key_here
   TIKTOK_CLIENT_SECRET=your_client_secret_here
   TIKTOK_ACCESS_TOKEN=
   ```
5. Replace `your_client_key_here` with your actual Client Key
6. Replace `your_client_secret_here` with your actual Client Secret
7. Leave `TIKTOK_ACCESS_TOKEN=` blank for now — the next step fills it in
8. Save the file

---

## Part 6 — Verify your setup

Run the checker to make sure everything is installed correctly:

### Windows
Double-click **`run.bat`** and type:
```
python check_setup.py
```
Or open Command Prompt in the project folder and run:
```
venv\Scripts\activate
python check_setup.py
```

### macOS / Linux
```bash
./run.sh check_setup.py
```
Or:
```bash
source venv/bin/activate
python check_setup.py
```

Everything should say **[OK]**. Fix anything that says **[MISSING]** before continuing.

---

## Part 7 — Log into TikTok

This connects the program to your TikTok account. **You only do this once** (or when your token expires, typically every 24 hours for sandbox apps).

### Windows
Double-click **`auth.bat`**

### macOS / Linux
```bash
./auth.sh
```

What happens:
1. Your browser opens to a TikTok login page
2. Log in with your TikTok account
3. Click **Authorize** when TikTok asks for permission
4. Your browser will show "Authorization successful! You can close this tab."
5. The terminal will say your token was saved to `.env`

> **If the browser doesn't open automatically:** Copy the URL printed in the terminal and paste it into your browser manually.

> **Windows Firewall popup:** If Windows asks to allow network access, click **Allow**.

---

## Part 8 — Generate a test video

Before posting anything publicly, generate a video locally to make sure it looks good.

### Windows
Double-click **`preview.bat`**

### macOS / Linux
```bash
./preview.sh
```

This creates a video in the **`output_videos`** folder. Open it and watch it. If it looks good, you're ready to post.

---

## Part 9 — Post your first video

Videos are posted as **private (only you can see them)** by default. This lets you review them on your phone before making them public.

### Windows
Double-click **`run.bat`**

### macOS / Linux
```bash
./run.sh
```

Then:
1. Open TikTok on your phone
2. Go to your profile → tap the video
3. If it looks good, tap the three dots → **Privacy** → change to **Everyone**

When you're confident in the quality, you can make all future posts public automatically.
Open `tiktok_uploader.py` in a text editor, find line 36, and change:
```python
"privacy_level": "SELF_ONLY",
```
to:
```python
"privacy_level": "PUBLIC_TO_EVERYONE",
```

---

## Part 10 — Turn on automatic posting

This posts 3 videos per day automatically (9am, 2pm, 7pm).

### Windows
Double-click **`schedule.bat`**

Keep the window open. If you close it, posting stops.

### macOS / Linux
```bash
./schedule.sh
```

Keep the terminal open. Press **Ctrl+C** to stop.

### Changing the post times

Open `main.py` in a text editor and find this line near the top:
```python
POST_TIMES = ["09:00", "14:00", "19:00"]
```
Change the times to whatever you want (24-hour format). Save the file.

---

## Keeping it running 24/7 (optional)

If you want it to post even when your computer is off, you need to run it on a server.

### Cheapest option: a VPS
- **DigitalOcean** — $4/month Linux server
- **Hetzner** — $3/month Linux server
- Upload this project to the server and run `./schedule.sh` in a `screen` or `tmux` session

### Free option: GitHub Actions
You can schedule it to run on GitHub's servers. This requires additional setup — ask for help if you want this.

---

## Customization

### Add your own quotes

Open `quotes.py` and add to the `QUOTES` list:
```python
("Your quote here.", "Author Name"),
```

### Change the color theme

There are 5 built-in themes (0–4). To preview a specific one:

**Windows:**
```
run.bat --preview --theme 3
```

**Mac/Linux:**
```bash
./run.sh --preview --theme 3
```

### Better AI voice (ElevenLabs)

The default voice is Google TTS (free, robotic). For a more natural voice:

1. Sign up free at **https://elevenlabs.io**
2. Go to your profile → API Keys → copy your key
3. Open `.env` and add:
   ```
   ELEVENLABS_API_KEY=your_key_here
   ```
The program will automatically use ElevenLabs on the next run.

---

## Troubleshooting

### Windows: typing "python" opens the Microsoft Store

Python is not installed. The Microsoft Store shortcut is just a placeholder.
- Close the Store
- Go to **https://www.python.org/downloads/** and download the real installer
- During install, check **"Add Python to PATH"**
- After install, restart your computer, then run `setup.bat` again

### Windows: "python is not recognized as an internal or external command"

Python isn't in your PATH. Fix:
1. Open **Control Panel → Apps → Apps & features**
2. Find Python and click Uninstall
3. Re-install from python.org — check **"Add Python to PATH"** this time
4. Restart your computer

### Windows: setup.bat closes immediately with no message

Right-click `setup.bat` → **Run as administrator**. If that doesn't help:
1. Press `Windows key`, type `cmd`, press Enter
2. Type: `cd /d "%USERPROFILE%\Desktop\Coding-Project"` (adjust path if needed)
3. Type: `setup.bat`
4. Read the error message and follow the fix

### Windows: "Windows protected your PC" (SmartScreen)

This is normal for downloaded `.bat` files.
- Click **"More info"**
- Click **"Run anyway"**

### Windows: antivirus blocks ffmpeg download

Some antivirus software incorrectly flags the ffmpeg binary that gets downloaded automatically. Fix:
- Temporarily disable real-time protection
- Run `setup.bat` again
- Re-enable protection when done

### Windows: "Access is denied" or path errors

The project folder might be in a protected location (like `Program Files`). Move it to your Desktop or `Documents` and run `setup.bat` again.

### Windows 10: `winget` not found

`winget` requires Windows 10 version 1809 or later. If you're on an older build:
- Update Windows via **Settings → Windows Update**
- Or install ffmpeg manually from **https://ffmpeg.org/download.html** (not needed if `imageio-ffmpeg` installed correctly)

### "Permission denied" running setup.sh (Mac/Linux)

```bash
chmod +x setup.sh
bash setup.sh
```

### "No module named X"

The packages didn't install correctly. Run:
```bash
# Windows (in Command Prompt)
venv\Scripts\activate
pip install -r requirements.txt

# Mac/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### Video is black / no audio

Usually means ffmpeg had an issue. Run `python check_setup.py` and check the ffmpeg line. Then:
```bash
pip install --upgrade imageio-ffmpeg
```

### "TIKTOK_ACCESS_TOKEN not set"

Run `auth.bat` (Windows) or `./auth.sh` (Mac/Linux) to log in again.

### "SPAM_RISK_TOO_MANY_POSTS"

You're posting too fast. Wait 30–60 minutes before trying again, and spread posts out more in `POST_TIMES`.

### "Authorization failed" in browser

Your redirect URI doesn't match. Go to developers.tiktok.com → your app → make sure this is in Redirect URIs:
```
http://localhost:8080/callback
```

### Windows Firewall popup during auth

When `auth.bat` runs, Windows may ask if Python can access the network. Click **Allow** — this is required for the TikTok login to work.

### Port 8080 already in use (auth script fails)

Something else is using port 8080. Close other apps and try again, or restart your computer.

### Fonts look wrong / text is tiny

On Linux, install fonts:
```bash
sudo apt install fonts-dejavu fonts-liberation
```

On Windows, this should never happen — all required fonts ship with Windows 10/11 by default.

---

## File structure

```
├── main.py              # Main program — run this to post
├── video_generator.py   # Builds the video (background, text, audio)
├── tiktok_uploader.py   # Handles TikTok API uploads
├── tiktok_auth.py       # One-time login to TikTok
├── quotes.py            # Quote library — add your own here
├── check_setup.py       # Verifies your environment is ready
│
├── setup.bat            # Windows: first-time setup (run once)
├── run.bat              # Windows: post a video
├── auth.bat             # Windows: log into TikTok
├── preview.bat          # Windows: generate test video only
├── schedule.bat         # Windows: auto-post on a schedule
│
├── setup.sh             # Mac/Linux: first-time setup (run once)
├── run.sh               # Mac/Linux: post a video
├── auth.sh              # Mac/Linux: log into TikTok
├── preview.sh           # Mac/Linux: generate test video only
├── schedule.sh          # Mac/Linux: auto-post on a schedule
│
├── requirements.txt     # Python packages (installed automatically)
├── .env.example         # Credential template
└── .env                 # Your credentials (never share this)
```

---

## Notes

- The `.env` file contains your private keys — never upload it, share it, or put it on GitHub
- TikTok access tokens expire — if posting stops working, run the auth script again
- TikTok requires AI-generated content to be labeled — the "AI Generated" watermark is included automatically
- The program stays on schedule even if you miss a post time — it just waits for the next one
