"""
Run this before anything else to verify your environment is ready.

Usage: python check_setup.py
"""

import sys
import os
import shutil
import importlib


REQUIRED_PACKAGES = [
    ("moviepy", "moviepy"),
    ("PIL", "Pillow"),
    ("gtts", "gTTS"),
    ("requests", "requests"),
    ("dotenv", "python-dotenv"),
    ("schedule", "schedule"),
    ("numpy", "numpy"),
]

OPTIONAL_PACKAGES = [
    ("elevenlabs", "elevenlabs"),
]


def check(label: str, ok: bool, fix: str = "") -> bool:
    status = "OK" if ok else "MISSING"
    pad = " " * (40 - len(label))
    print(f"  {label}{pad}[{status}]")
    if not ok and fix:
        print(f"         Fix: {fix}")
    return ok


def main() -> None:
    print(f"\nPython {sys.version}")
    print(f"Platform: {sys.platform}\n")

    all_ok = True

    print("--- Python version ---")
    ok = sys.version_info >= (3, 9)
    all_ok &= check("Python >= 3.9", ok, "Download from https://python.org/downloads/")

    print("\n--- Required packages ---")
    for import_name, pip_name in REQUIRED_PACKAGES:
        try:
            importlib.import_module(import_name)
            ok = True
        except ImportError:
            ok = False
        all_ok &= check(pip_name, ok, f"pip install {pip_name}")

    print("\n--- Optional packages ---")
    for import_name, pip_name in OPTIONAL_PACKAGES:
        try:
            importlib.import_module(import_name)
            check(f"{pip_name} (ElevenLabs voices)", True)
        except ImportError:
            check(f"{pip_name} (ElevenLabs voices)", False, f"pip install {pip_name}  (optional — gTTS is used otherwise)")

    print("\n--- ffmpeg ---")
    ffmpeg_ok = False

    # Prefer bundled ffmpeg that ships with imageio-ffmpeg (installed via pip)
    try:
        import imageio_ffmpeg
        bundled = imageio_ffmpeg.get_ffmpeg_exe()
        if bundled and os.path.exists(bundled):
            check("ffmpeg (bundled — no install needed)", True)
            ffmpeg_ok = True
    except Exception:
        pass

    if not ffmpeg_ok:
        system_ffmpeg = shutil.which("ffmpeg")
        ffmpeg_ok = system_ffmpeg is not None
        if sys.platform == "win32":
            fix = "Re-run: pip install imageio-ffmpeg  OR  winget install ffmpeg"
        elif sys.platform == "darwin":
            fix = "Re-run: pip install imageio-ffmpeg  OR  brew install ffmpeg"
        else:
            fix = "Re-run: pip install imageio-ffmpeg  OR  sudo apt install ffmpeg"
        all_ok &= check("ffmpeg (system)", ffmpeg_ok, fix)

    print("\n--- Fonts ---")
    if sys.platform == "win32":
        win_fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
        has_font = os.path.exists(os.path.join(win_fonts, "arial.ttf"))
        check("Arial (Windows Fonts)", has_font, "Should be present by default on Windows")
    elif sys.platform == "darwin":
        paths = ["/Library/Fonts/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"]
        has_font = any(os.path.exists(p) for p in paths)
        check("Arial / System font", has_font, "Install Microsoft fonts or Office — a fallback will be used if missing")
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
        has_font = any(os.path.exists(p) for p in paths)
        check("DejaVu / Liberation font", has_font, "sudo apt install fonts-dejavu  OR  fonts-liberation")

    print("\n--- .env file ---")
    has_env = os.path.exists(".env")
    check(".env exists", has_env, "cp .env.example .env  (Mac/Linux)  OR  copy .env.example .env  (Windows)")

    if has_env:
        from dotenv import load_dotenv
        load_dotenv()
        check("TIKTOK_CLIENT_KEY set", bool(os.getenv("TIKTOK_CLIENT_KEY")), "Add to .env — see README")
        check("TIKTOK_CLIENT_SECRET set", bool(os.getenv("TIKTOK_CLIENT_SECRET")), "Add to .env — see README")
        has_token = bool(os.getenv("TIKTOK_ACCESS_TOKEN"))
        check("TIKTOK_ACCESS_TOKEN set", has_token, "Run: python tiktok_auth.py")

    print()
    if all_ok:
        print("Everything looks good! Run: python main.py --preview")
    else:
        print("Fix the MISSING items above, then re-run this script.")
    print()


if __name__ == "__main__":
    main()
