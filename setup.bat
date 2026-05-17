@echo off
setlocal EnableDelayedExpansion

REM Always run from the folder this script lives in (safe for double-click)
cd /d "%~dp0"

echo.
echo =============================================
echo   TikTok AI Video Poster ^| Windows Setup
echo =============================================
echo.

REM ── Detect Windows version ────────────────────
for /f "tokens=4-5 delims=. " %%i in ('ver') do set WIN_VER=%%i.%%j
echo Windows version: %WIN_VER%
echo.

REM ── Find Python ───────────────────────────────
REM Try 'python' first, but guard against the Windows Store stub.
REM The stub returns exit code 9009 or opens the Store without printing a version.

set PYTHON=
python --version >nul 2>&1
if not errorlevel 1 (
    REM Make sure it actually printed a version (not the Store stub)
    for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do (
        if "%%v" NEQ "" set PYTHON=python
    )
)

if "!PYTHON!"=="" (
    py --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON=py
    )
)

if "!PYTHON!"=="" (
    echo [ERROR] Python was not found on this computer.
    echo.
    echo  How to fix:
    echo  1. Go to:  https://www.python.org/downloads/
    echo  2. Click the yellow "Download Python 3.x" button
    echo  3. Run the downloaded installer
    echo  4. IMPORTANT: On the first screen of the installer,
    echo     CHECK THE BOX that says "Add Python to PATH"
    echo  5. Click "Install Now" and wait for it to finish
    echo  6. Close this window and double-click setup.bat again
    echo.
    echo  NOTE: If Windows opens the Microsoft Store when you
    echo  type "python", that means Python is NOT installed yet.
    echo  Follow the steps above to install it from python.org.
    echo.
    pause
    exit /b 1
)

REM ── Check Python version ──────────────────────
for /f "tokens=2 delims= " %%v in ('!PYTHON! --version 2^>^&1') do set PY_VER=%%v
echo [OK] Python %PY_VER% found

REM Extract major.minor for version check
for /f "tokens=1,2 delims=." %%a in ("%PY_VER%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)
if !PY_MAJOR! LSS 3 (
    echo [ERROR] Python 3.9 or newer is required. You have %PY_VER%.
    echo Download the latest Python 3 from https://www.python.org/downloads/
    pause
    exit /b 1
)
if !PY_MAJOR! EQU 3 if !PY_MINOR! LSS 9 (
    echo [ERROR] Python 3.9 or newer is required. You have %PY_VER%.
    echo Download the latest Python 3 from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

REM ── Create virtual environment ────────────────
if exist venv (
    echo [OK] Virtual environment already exists, skipping creation.
) else (
    echo Creating virtual environment...
    !PYTHON! -m venv venv
    if errorlevel 1 (
        echo [ERROR] Could not create virtual environment.
        echo.
        echo  Possible fixes:
        echo  - Reinstall Python and make sure "pip" and "venv" are included
        echo  - Try: !PYTHON! -m pip install --upgrade pip
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.
)
echo.

REM ── Activate and install packages ────────────
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Could not activate virtual environment.
    echo  Try deleting the "venv" folder and running setup.bat again.
    pause
    exit /b 1
)

echo Upgrading pip...
python -m pip install --upgrade pip --quiet

echo Installing packages (this downloads ~200MB and may take 3-5 minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo [ERROR] Package installation failed.
    echo.
    echo  Possible fixes:
    echo  - Check your internet connection
    echo  - Temporarily disable antivirus and try again
    echo  - Delete the "venv" folder and run setup.bat again
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
echo   STEP 1: Open the .env file in Notepad
echo           and fill in your TikTok credentials
echo           (See README.md for how to get them)
echo.
echo   STEP 2: Double-click auth.bat to log into TikTok
echo.
echo   STEP 3: Double-click preview.bat to generate a test video
echo.
echo   STEP 4: Double-click run.bat to post your first video!
echo.
pause
