---
title: Agentic AI Trader
emoji: 📈
colorFrom: green
colorTo: teal
sdk: docker
app_port: 7860
pinned: false
---

# 🚀 Agentic AI Trader — Indian Market Intelligence

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)

AI-powered Indian stock market analysis with real-time data, technical indicators, and intelligent trading signals for NIFTY 50, Bank NIFTY, and SENSEX.

![Dark Trading Dashboard](https://img.shields.io/badge/UI-Glassmorphism-blueviolet)

---

## ✨ Features

- 📊 **Real-time Market Data** — Live prices for NIFTY 50, BANK NIFTY, SENSEX via Yahoo Finance
- 📈 **Day-by-Day Historical Values** — 7 days of closing data with change indicators
- 🤖 **AI-Powered Analysis** — Technical indicator-based predictions (RSI, MACD, Bollinger Bands)
- 📱 **Interactive Charts** — Intraday charts with Plotly.js
- 🎨 **Premium UI** — Modern glassmorphism design with smooth animations
- ⏰ **Market Hours Aware** — Respects IST trading hours (9:15 AM – 3:30 PM)
- 🔌 **WebSocket Streaming** — Real-time updates via Socket.IO
- 🧠 **RAG System** — Optional Retrieval-Augmented Generation for enhanced insights

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/agentic_ai_trader.git
cd agentic_ai_trader
```

### 2. Set up a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
python perfect_indian_app.py
```

### 5. Open in your browser
```
http://localhost:5008
```

> **Windows shortcut:** Double-click `QUICK_START.bat` to do all of the above automatically.

## 📦 Requirements

- **Python 3.8** or higher
- Internet connection (for live market data)
- ~100 MB disk space (core dependencies)

### Optional: Full AI Features
For advanced AI agents, RAG system, and ML models:
```bash
pip install -r requirements_full.txt
```
> ⚠️ This installs TensorFlow, PyTorch, LangChain, ChromaDB, etc. (~5–10 GB)

## ⚙️ Configuration

Copy the example environment file and customize:
```bash
cp .env.example .env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | Auto-generated | Flask session secret key |
| `PORT` | `5008` | Server port |
| `DEBUG` | `False` | Enable debug mode (never use in production) |

## 🧩 Project Structure

```
agentic_ai_trader/
├── perfect_indian_app.py      # Main application (Flask + UI)
├── requirements.txt           # Core dependencies
├── requirements_full.txt      # Full dependencies (AI/ML/RAG)
├── .env.example               # Environment variable template
├── QUICK_START.bat             # Windows one-click launcher
├── backend/
│   ├── agents/                # AI trading agents
│   │   ├── market_agent.py    # Market data processing
│   │   ├── strategy_agent.py  # Trading strategy analysis
│   │   ├── risk_agent.py      # Risk assessment
│   │   └── analysis_agent.py  # AI analysis generation
│   ├── rag/                   # RAG system
│   │   ├── rag_pipeline.py    # Question-answer pipeline
│   │   ├── rag_service.py     # RAG service layer
│   │   ├── embed.py           # Document embeddings
│   │   ├── retrieve.py        # Document retrieval
│   │   └── llm_integration.py # LLM connectivity
│   └── data/
│       └── historical_data_manager.py
└── data/
    └── historical/            # Local data cache
```

## 🖥️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main trading dashboard |
| `/api/health` | GET | Health check |
| `/api/market/latest` | GET | Latest market data |
| `/api/market-status` | GET | Market session status |
| `/api/market-data` | GET | Full market data with metadata |
| `/api/historical-data/<symbol>` | GET | 7-day historical data |
| `/api/chart-data/<symbol>` | GET | Intraday chart data |
| `/api/ai-analysis/<symbol>` | GET | Full AI analysis |
| `/api/ai-analysis-fast/<symbol>` | GET | Quick AI analysis |
| `/api/technical-analysis/<symbol>` | GET | Technical indicators |
| `/api/system/status` | GET | System health dashboard |
| `/api/rag/status` | GET | RAG system status |

**Supported symbols:** `NIFTY_50`, `BANK_NIFTY`, `SENSEX`

## 🕐 Market Hours (IST)

| Session | Time |
|---------|------|
| Pre-Market Analysis | 8:45 AM |
| Market Open | 9:15 AM – 3:30 PM |
| Post-Market | 3:30 PM – 4:00 PM |

## 📊 Data Sources

- **Primary:** Yahoo Finance API (via `yfinance`)
- **Fallback:** Simulated data for reliability when API is unavailable
- **Update Frequency:** Every 30 seconds during market hours

## 📱 Mobile Access

1. Connect your phone to the same WiFi network
2. Find your computer's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. Open `http://YOUR_IP:5008` on your phone

## 🔧 Troubleshooting

### Port already in use
```bash
# Use a different port
set PORT=5009         # Windows
export PORT=5009      # macOS/Linux
python perfect_indian_app.py
```

### Missing dependencies
```bash
pip install -r requirements.txt
```

### Market data not loading
- Check your internet connection
- Yahoo Finance may have rate limits — wait 30 seconds and refresh
- During non-market hours, historical data is still available

## ⚠️ Disclaimer

This application is for **educational and informational purposes only**. It does not constitute financial advice. Trading in the stock market involves risk. Always do your own research before making investment decisions.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Built with ❤️ for the Indian trading community**
