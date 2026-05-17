@echo off
echo.
echo Opening TikTok authorization...
echo A browser window will open. Log in and click Authorize.
echo If the browser doesn't open, check the URL printed in the terminal.
echo.
call venv\Scripts\activate.bat
python tiktok_auth.py
pause
