#!/usr/bin/env bash
echo ""
echo "Opening TikTok authorization..."
echo "A browser window will open. Log in and click Authorize."
echo "If the browser doesn't open, check the URL printed below."
echo ""
source "$(dirname "$0")/venv/bin/activate"
python tiktok_auth.py
