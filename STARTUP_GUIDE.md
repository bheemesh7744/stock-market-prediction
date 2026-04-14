# 🚀 Startup Guide

## Quick Start

### Option 1: Windows Launcher (Easiest)
Double-click `QUICK_START.bat` — it handles everything automatically.

### Option 2: Command Line
```bash
# Navigate to the project directory
cd path/to/agentic_ai_trader

# (Optional) Activate virtual environment
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the app
python perfect_indian_app.py
```

### Option 3: Custom Port
```bash
# Windows
set PORT=5009
python perfect_indian_app.py

# macOS/Linux
PORT=5009 python perfect_indian_app.py
```

## 🌐 Access the App

Once running, open your browser:
**http://localhost:5008**

## ✅ Before Starting Checklist

1. You have Python 3.8+ installed (`python --version`)
2. Dependencies are installed (`pip install -r requirements.txt`)
3. You have an internet connection (for live market data)
4. Port 5008 is available (or set a different `PORT`)

## 🛠️ Troubleshooting

### Dependencies not found
```bash
pip install -r requirements.txt
```

### Port already in use
Set a different port using the `PORT` environment variable (see above).

### Python not found
Download and install Python from https://python.org. Make sure to check "Add Python to PATH" during installation.

### Clear Python cache
```bash
# Windows
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# macOS/Linux
find . -name "__pycache__" -type d -exec rm -rf {} +
```

## 📱 Mobile Access

1. Connect to the same WiFi network
2. Find your IP: `ipconfig` (Windows) / `ifconfig` (Mac/Linux)
3. Open `http://YOUR_IP:5008` on your phone

## 🛑 Stopping the App

Press `Ctrl + C` in the terminal to stop the server.

---

**Use `python perfect_indian_app.py` for the best experience!**
