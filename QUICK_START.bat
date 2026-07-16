@echo off
title Indian Market Trading App - Quick Start
color 0A

echo.
echo ========================================
echo   Indian Market Trading App Launcher
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo 💡 Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if in correct directory
if not exist "perfect_indian_app.py" (
    echo ❌ perfect_indian_app.py not found
    echo 💡 Make sure you're in the project directory
    echo 💡 Right-click this .bat file and select "Open file location"
    pause
    exit /b 1
)

echo ✅ Project files found
echo.

REM Install dependencies if needed
echo 📦 Checking dependencies...
python -c "import flask, flask_socketio, yfinance, pandas, numpy, pytz, schedule" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install flask flask-socketio yfinance pandas numpy pytz schedule
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies ready
echo.

REM Start the Python app
echo 🚀 Starting Indian Market Trading App...
echo 📍 URL: http://127.0.0.1:5008
echo.
echo 🌐 Opening browser in 3 seconds...
echo.

REM Spawn a background command to open the browser after a 3s delay
start "" cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:5008"

REM Start the Python app
python perfect_indian_app.py

echo.
echo 🛑 App stopped
pause
