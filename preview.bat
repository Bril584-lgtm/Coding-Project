@echo off
cd /d "%~dp0"
echo.
echo Generating a test video (no upload to TikTok)...
echo This will take about 30-60 seconds.
echo.
call venv\Scripts\activate.bat
python main.py --preview
echo.
echo Done! Open the "output_videos" folder in this directory to watch your video.
echo.
pause
