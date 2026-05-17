#!/usr/bin/env bash
echo ""
echo "Generating a test video (no upload)..."
echo "Check the output_videos folder when done."
echo ""
source "$(dirname "$0")/venv/bin/activate"
python main.py --preview
echo ""
echo "Done! Open the output_videos folder to see your video."
