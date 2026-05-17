@echo off
setlocal EnableDelayedExpansion

echo.
echo =============================================
echo   TikTok AI Video Poster ^| Windows Setup
echo =============================================
echo.

REM ── Check Python ──────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python not found.
        echo.
        echo  1. Go to https://www.python.org/downloads/
        echo  2. Download the latest Python 3.x installer
        echo  3. Run the installer and CHECK "Add Python to PATH"
        echo  4. Restart this script
        echo.
        pause
        exit /b 1
    )
    set PYTHON=py
) else (
    set PYTHON=python
)

for /f "tokens=2 delims= " %%v in ('!PYTHON! --version') do set PY_VER=%%v
echo [OK] Python %PY_VER% found
echo.

REM ── Create virtual environment ────────────────
if exist venv (
    echo [OK] Virtual environment already exists, skipping creation.
) else (
    echo Creating virtual environment...
    !PYTHON! -m venv venv
    if errorlevel 1 (
        echo [ERROR] Could not create virtual environment.
        echo Try running: %PYTHON% -m pip install virtualenv
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)
echo.

REM ── Activate and install packages ────────────
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Upgrading pip...
python -m pip install --upgrade pip --quiet

echo Installing packages (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Package installation failed.
    echo  - Check your internet connection
    echo  - Try running setup.bat again
    pause
    exit /b 1
)
echo [OK] All packages installed.
echo.

REM ── Copy .env ────────────────────────────────
if not exist .env (
    copy .env.example .env >nul
    echo [OK] Created .env file from template.
) else (
    echo [OK] .env file already exists.
)
echo.

REM ── Done ─────────────────────────────────────
echo =============================================
echo   Setup complete!
echo =============================================
echo.
echo What to do next:
echo.
echo   STEP 1: Open .env in Notepad and fill in your TikTok credentials
echo           (See README.md for how to get them)
echo.
echo   STEP 2: Double-click auth.bat to log into TikTok
echo.
echo   STEP 3: Double-click preview.bat to generate a test video
echo.
echo   STEP 4: Double-click run.bat to post your first video!
echo.
pause
