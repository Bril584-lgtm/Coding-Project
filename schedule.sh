#!/usr/bin/env bash
echo ""
echo "Starting auto-scheduler (posts 3x per day)."
echo "Keep this window open. Press Ctrl+C to stop."
echo ""
source "$(dirname "$0")/venv/bin/activate"
python main.py --schedule
