@echo off
cd /d "%~dp0"
echo.
echo Starting auto-scheduler — posts 3 videos per day (9am, 2pm, 7pm).
echo Keep this window open. Press Ctrl+C to stop.
echo.
call venv\Scripts\activate.bat
python main.py --schedule
echo.
pause
