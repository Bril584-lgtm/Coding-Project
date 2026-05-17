@echo off
echo.
echo Generating a test video (no upload)...
echo Check the output_videos folder when done.
echo.
call venv\Scripts\activate.bat
python main.py --preview
echo.
echo Done! Open the output_videos folder to see your video.
pause
