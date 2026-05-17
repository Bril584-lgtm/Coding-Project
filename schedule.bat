@echo off
echo.
echo Starting auto-scheduler (posts 3x per day).
echo Keep this window open. Press Ctrl+C to stop.
echo.
call venv\Scripts\activate.bat
python main.py --schedule
pause
