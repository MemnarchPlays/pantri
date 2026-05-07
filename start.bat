@echo off
cd /d "%~dp0"
title Pantry Tracker

echo Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found.
    echo Download and install it from https://python.org ^(check "Add to PATH" during install^)
    pause
    exit /b 1
)

echo Installing / updating dependencies...
python -m pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b 1
)
echo Dependencies OK.

if not exist ".env" (
    echo.
    echo NOTE: No .env file found — Discord bot features won't work until you add one.
    echo       See Settings ^> Discord Bot inside the app for setup instructions.
    echo.
)

echo.
echo Starting Pantry Tracker...
echo Press Ctrl+C to stop.
echo.
python pantry_app.py
pause
