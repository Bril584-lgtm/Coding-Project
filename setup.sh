#!/usr/bin/env bash
set -e

echo ""
echo "============================================="
echo "  TikTok AI Video Poster | Setup"
echo "============================================="
echo ""

# ── Detect OS ─────────────────────────────────────
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
fi

# ── Check Python ───────────────────────────────────
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "[ERROR] Python not found."
    echo ""
    if [ "$OS" = "mac" ]; then
        echo "Install with:"
        echo "  brew install python"
        echo "  (or download from https://www.python.org/downloads/)"
    else
        echo "Install with:"
        echo "  sudo apt install python3 python3-pip python3-venv"
    fi
    exit 1
fi

PY_VER=$($PYTHON --version 2>&1)
PY_MIN=$($PYTHON -c "import sys; print(sys.version_info >= (3,9))")
if [ "$PY_MIN" = "False" ]; then
    echo "[ERROR] Python 3.9 or newer is required."
    echo "Current: $PY_VER"
    echo "Download newer Python from https://www.python.org/downloads/"
    exit 1
fi
echo "[OK] $PY_VER"
echo ""

# ── Linux: install fonts ───────────────────────────
if [ "$OS" = "linux" ]; then
    echo "Installing fonts (may prompt for sudo password)..."
    sudo apt-get install -y fonts-dejavu fonts-liberation 2>/dev/null \
        || echo "  Note: Could not install fonts automatically. Videos will use a fallback font."
    echo ""
fi

# ── Create virtual environment ─────────────────────
if [ -d "venv" ]; then
    echo "[OK] Virtual environment already exists, skipping creation."
else
    echo "Creating virtual environment..."
    $PYTHON -m venv venv
    echo "[OK] Virtual environment created."
fi
echo ""

# ── Install packages ───────────────────────────────
echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip --quiet

echo "Installing packages (this may take a few minutes)..."
pip install -r requirements.txt
echo "[OK] All packages installed."
echo ""

# ── Copy .env ──────────────────────────────────────
if [ ! -f .env ]; then
    cp .env.example .env
    echo "[OK] Created .env file from template."
else
    echo "[OK] .env file already exists."
fi

# ── Make run scripts executable ────────────────────
chmod +x run.sh auth.sh preview.sh schedule.sh 2>/dev/null || true
echo ""

# ── Done ───────────────────────────────────────────
echo "============================================="
echo "  Setup complete!"
echo "============================================="
echo ""
echo "What to do next:"
echo ""
echo "  STEP 1: Open .env in a text editor and fill in your TikTok credentials"
echo "          (See README.md for how to get them)"
echo ""
echo "  STEP 2: Run ./auth.sh to log into TikTok"
echo ""
echo "  STEP 3: Run ./preview.sh to generate a test video"
echo ""
echo "  STEP 4: Run ./run.sh to post your first video!"
echo ""
