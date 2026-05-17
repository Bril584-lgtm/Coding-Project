@echo off
cd /d "%~dp0"
echo.
echo Opening TikTok authorization...
echo.
echo A browser window will open. Log in with your TikTok account and click Authorize.
echo If the browser does not open automatically, copy the link printed below into your browser.
echo.
echo NOTE: If Windows Firewall asks to allow access, click "Allow".
echo.
call venv\Scripts\activate.bat
python tiktok_auth.py
echo.
pause
