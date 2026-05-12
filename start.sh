#!/bin/bash
cd "$(dirname "$0")"

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Install it with: sudo apt install python3 python3-pip  (Debian/Ubuntu)"
    echo "                 brew install python3                   (macOS)"
    exit 1
fi

# Pull latest from GitHub
echo "Pulling latest updates from GitHub..."
git pull || echo "WARNING: git pull failed. Starting with current version."

# Install/update dependencies
echo "Installing / updating dependencies..."
python3 -m pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies."
    exit 1
fi
echo "Dependencies OK."

# Warn if no .env
if [ ! -f ".env" ]; then
    echo ""
    echo "NOTE: No .env file found — Discord bot features won't work until you add one."
    echo "      See Settings > Discord Bot inside the app for setup instructions."
    echo ""
fi

echo ""
echo "Starting Pantry Tracker..."
echo "Press Ctrl+C to stop."
echo ""

python3 pantry_app.py
