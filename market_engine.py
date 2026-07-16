#!/usr/bin/env python3
"""
Perfect Indian Market Trading App
Day-by-day market closed values and neat time formatting
"""

import sys
import os
import time
import json
import random
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Set
import pytz
from flask import Flask, jsonify, request, Response, session
from flask_socketio import SocketIO, emit
import logging
import yfinance as yf
import pandas as pd
import numpy as np
import threading
import schedule
import requests
try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None
from concurrent.futures import ThreadPoolExecutor

# ══════════════════════════════════════════════════════════════
# CONFIGURATION CONSTANTS — No more magic numbers
# ══════════════════════════════════════════════════════════════

# Data & Caching
CACHE_TTL_SECONDS = 10          # Market data cache TTL (reduced for faster updates)
RAG_CACHE_TIMEOUT = 300         # RAG pipeline cache (5 min)
STOCKS_FETCH_WORKERS = 10       # ThreadPoolExecutor workers

# Rate Limiting
RATE_LIMIT_REQUESTS = 60        # Max requests per window
RATE_LIMIT_WINDOW = 60          # Window size in seconds

# Valid symbols whitelist (security: input validation)
VALID_INDEX_SYMBOLS: Set[str] = {'NIFTY_50', 'BANK_NIFTY', 'SENSEX'}
VALID_TIMEFRAMES: Set[str] = {'5min', '1hr', '1day', '1yr', '3yr', '5yr', 'lifetime'}


# ══════════════════════════════════════════════════════════════
# THREAD-SAFE CACHE — Replaces unsafe global dicts
# ══════════════════════════════════════════════════════════════

class ThreadSafeCache:
    """Thread-safe TTL cache for market data and predictions."""

    def __init__(self, default_ttl: int = CACHE_TTL_SECONDS):
        self._store: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._default_ttl = default_ttl

    def get(self, key: str, default=None):
        with self._lock:
            if key in self._store:
                age = time.time() - self._timestamps.get(key, 0)
                if age < self._default_ttl:
                    return self._store[key]
                else:
                    del self._store[key]
                    del self._timestamps[key]
        return default

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        with self._lock:
            self._store[key] = value
            self._timestamps[key] = time.time()

    def delete(self, key: str):
        with self._lock:
            self._store.pop(key, None)
            self._timestamps.pop(key, None)

    def get_all(self) -> Dict[str, Any]:
        with self._lock:
            now = time.time()
            return {k: v for k, v in self._store.items()
                    if (now - self._timestamps.get(k, 0)) < self._default_ttl}

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    def __setitem__(self, key: str, value: Any):
        self.set(key, value)

    def __getitem__(self, key: str):
        val = self.get(key)
        if val is None:
            raise KeyError(key)
        return val


# ══════════════════════════════════════════════════════════════
# RATE LIMITER — Prevents API abuse (no external dependency)
# ══════════════════════════════════════════════════════════════

class RateLimiter:
    """Simple sliding-window rate limiter per IP address."""

    def __init__(self, max_requests: int = RATE_LIMIT_REQUESTS, window_seconds: int = RATE_LIMIT_WINDOW):
        self._requests: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()
        self._max = max_requests
        self._window = window_seconds

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        with self._lock:
            # Prune old entries
            self._requests[client_ip] = [
                t for t in self._requests[client_ip] if now - t < self._window
            ]
            if len(self._requests[client_ip]) >= self._max:
                return False
            self._requests[client_ip].append(now)
            return True

    def remaining(self, client_ip: str) -> int:
        now = time.time()
        with self._lock:
            active = [t for t in self._requests.get(client_ip, []) if now - t < self._window]
            return max(0, self._max - len(active))


# Initialize shared infrastructure
market_data_cache = ThreadSafeCache(default_ttl=CACHE_TTL_SECONDS)
rate_limiter = RateLimiter()
shared_executor = ThreadPoolExecutor(max_workers=STOCKS_FETCH_WORKERS)

# Import User DB Manager
from backend.data.user_db_manager import UserDBManager
user_db = UserDBManager()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Global variables for RAG caching
rag_pipeline_cache = None
rag_cache_timestamp = None
rag_cache_timeout = RAG_CACHE_TIMEOUT

def get_rag_pipeline_cached():
    """Get RAG pipeline with caching to improve performance"""
    global rag_pipeline_cache, rag_cache_timestamp
    
    current_time = time.time()
    
    # Check if cache is valid
    if (rag_pipeline_cache is not None and 
        rag_cache_timestamp is not None and 
        (current_time - rag_cache_timestamp) < rag_cache_timeout):
        return rag_pipeline_cache
    
    # Initialize new pipeline
    try:
        logger.info("Initializing RAG pipeline (cached)...")
        try:
            from backend.rag.rag_pipeline import get_rag_pipeline
            rag_pipeline_cache = get_rag_pipeline()
        except ImportError:
            logger.warning("RAG pipeline not available (import failed)")
            rag_pipeline_cache = None
        rag_cache_timestamp = current_time
        logger.info("RAG pipeline cached successfully")
        return rag_pipeline_cache
    except Exception as e:
        logger.error(f"Failed to initialize RAG pipeline: {e}")
        return None

def process_trading_question_cached(question, context):
    """Process trading question with cached RAG pipeline"""
    try:
        pipeline = get_rag_pipeline_cached()
        if pipeline:
            return pipeline.process_question(question, context)
        else:
            return {'success': False, 'answer': 'RAG system not available', 'sources': [], 'context_used': ''}
    except Exception as e:
        logger.error(f"Error in cached RAG processing: {e}")
        return {'success': False, 'answer': 'RAG processing failed', 'sources': [], 'context_used': ''}

# Import RAG system and AI agents status flags
# Set to True by default, will fail dynamically inside routes if dependencies cannot load
RAG_AVAILABLE = True
AGENTS_AVAILABLE = True

# Initialize Flask app
app = Flask(__name__)

# Security: Require SECRET_KEY in production, use dev fallback only in debug mode
_is_debug = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
_secret_key = os.environ.get('SECRET_KEY')
if not _secret_key and not _is_debug:
    _secret_key = os.urandom(24).hex()
    logger.warning("SECRET_KEY not set — generated a random key. Sessions will not persist across restarts. Set SECRET_KEY in .env for production.")
elif not _secret_key:
    _secret_key = 'dev-only-insecure-key-do-not-use-in-production'
app.config['SECRET_KEY'] = _secret_key
app.permanent_session_lifetime = timedelta(days=30)
# Security: Restrict CORS to localhost origins only (not wildcard)
_ALLOWED_ORIGINS = [
    'http://localhost:5008', 'http://127.0.0.1:5008',
    'http://localhost:5009', 'http://127.0.0.1:5009',
    f"http://localhost:{os.environ.get('PORT', '5008')}",
]
socketio = SocketIO(app, cors_allowed_origins=_ALLOWED_ORIGINS, async_mode='threading')

# Indian Market Configuration
INDIAN_TIMEZONE = pytz.timezone('Asia/Kolkata')
MARKET_OPEN_TIME = datetime.strptime("09:15", "%H:%M").time()
MARKET_CLOSE_TIME = datetime.strptime("15:30", "%H:%M").time()
MARKET_START = MARKET_OPEN_TIME
MARKET_END = MARKET_CLOSE_TIME
PRE_MARKET_START = datetime.strptime("09:00", "%H:%M").time()
PRE_MARKET_ANALYSIS_TIME = datetime.strptime("08:45", "%H:%M").time()

# Indian Market Symbols - Clean configuration
INDIAN_MARKET_CONFIG = {
    'NIFTY_50': {
        'symbol': '^NSEI',
        'name': 'NIFTY 50',
        'display_name': 'NIFTY 50',
        'exchange': 'NSE'
    },
    'BANK_NIFTY': {
        'symbol': '^NSEBANK',
        'name': 'BANK NIFTY',
        'display_name': 'BANK NIFTY',
        'exchange': 'NSE'
    },
    'SENSEX': {
        'symbol': '^BSESN',
        'name': 'SENSEX',
        'display_name': 'SENSEX',
        'exchange': 'BSE'
    }
}

INDIAN_STOCKS_CONFIG = {
    'RELIANCE': {
        'symbol': 'RELIANCE.NS',
        'name': 'Reliance Industries Ltd.',
        'display_name': 'Reliance',
        'exchange': 'NSE',
        'sector': 'Energy'
    },
    'TCS': {
        'symbol': 'TCS.NS',
        'name': 'Tata Consultancy Services',
        'display_name': 'TCS',
        'exchange': 'NSE',
        'sector': 'IT Services'
    },
    'HDFCBANK': {
        'symbol': 'HDFCBANK.NS',
        'name': 'HDFC Bank Limited',
        'display_name': 'HDFC Bank',
        'exchange': 'NSE',
        'sector': 'Banking'
    },
    'INFY': {
        'symbol': 'INFY.NS',
        'name': 'Infosys Limited',
        'display_name': 'Infosys',
        'exchange': 'NSE',
        'sector': 'IT Services'
    },
    'ICICIBANK': {
        'symbol': 'ICICIBANK.NS',
        'name': 'ICICI Bank Limited',
        'display_name': 'ICICI Bank',
        'exchange': 'NSE',
        'sector': 'Banking'
    },
    'HINDUNILVR': {
        'symbol': 'HINDUNILVR.NS',
        'name': 'Hindustan Unilever Ltd.',
        'display_name': 'HUL',
        'exchange': 'NSE',
        'sector': 'FMCG'
    },
    'SBIN': {
        'symbol': 'SBIN.NS',
        'name': 'State Bank of India',
        'display_name': 'SBI',
        'exchange': 'NSE',
        'sector': 'Banking'
    },
    'BHARTIARTL': {
        'symbol': 'BHARTIARTL.NS',
        'name': 'Bharti Airtel Limited',
        'display_name': 'Bharti Airtel',
        'exchange': 'NSE',
        'sector': 'Telecom'
    },
    'ITC': {
        'symbol': 'ITC.NS',
        'name': 'ITC Limited',
        'display_name': 'ITC',
        'exchange': 'NSE',
        'sector': 'FMCG'
    },
    'KOTAKBANK': {
        'symbol': 'KOTAKBANK.NS',
        'name': 'Kotak Mahindra Bank Ltd.',
        'display_name': 'Kotak Bank',
        'exchange': 'NSE',
        'sector': 'Banking'
    },
    'LT': {
        'symbol': 'LT.NS',
        'name': 'Larsen & Toubro Limited',
        'display_name': 'L&T',
        'exchange': 'NSE',
        'sector': 'Infrastructure'
    },
    'AXISBANK': {
        'symbol': 'AXISBANK.NS',
        'name': 'Axis Bank Limited',
        'display_name': 'Axis Bank',
        'exchange': 'NSE',
        'sector': 'Banking'
    },
    'BAJFINANCE': {
        'symbol': 'BAJFINANCE.NS',
        'name': 'Bajaj Finance Limited',
        'display_name': 'Bajaj Finance',
        'exchange': 'NSE',
        'sector': 'Finance'
    },
    'MARUTI': {
        'symbol': 'MARUTI.NS',
        'name': 'Maruti Suzuki India Ltd.',
        'display_name': 'Maruti Suzuki',
        'exchange': 'NSE',
        'sector': 'Automotive'
    },
    'TATAMOTORS': {
        'symbol': 'TATAMOTORS.NS',
        'name': 'Tata Motors Limited',
        'display_name': 'Tata Motors',
        'exchange': 'NSE',
        'sector': 'Automotive'
    },
    'TATASTEEL': {
        'symbol': 'TATASTEEL.NS',
        'name': 'Tata Steel Limited',
        'display_name': 'Tata Steel',
        'exchange': 'NSE',
        'sector': 'Metals'
    },
    'SUNPHARMA': {
        'symbol': 'SUNPHARMA.NS',
        'name': 'Sun Pharmaceutical Industries',
        'display_name': 'Sun Pharma',
        'exchange': 'NSE',
        'sector': 'Pharmaceuticals'
    },
    'ADANIENT': {
        'symbol': 'ADANIENT.NS',
        'name': 'Adani Enterprises Limited',
        'display_name': 'Adani Ent',
        'exchange': 'NSE',
        'sector': 'Conglomerate'
    },
    'WIPRO': {
        'symbol': 'WIPRO.NS',
        'name': 'Wipro Limited',
        'display_name': 'Wipro',
        'exchange': 'NSE',
        'sector': 'IT Services'
    },
    'POWERGRID': {
        'symbol': 'POWERGRID.NS',
        'name': 'Power Grid Corp. of India',
        'display_name': 'Power Grid',
        'exchange': 'NSE',
        'sector': 'Power Transmission'
    }
}

# AI Analysis Storage
ai_predictions = {}
pre_market_analysis = {}

class AIAnalyzer:
    def __init__(self):
        self.models_trained = False
        self.prediction_history = []
        
    def analyze_market_data(self, symbol, historical_data):
        """Analyze market data and generate AI predictions"""
        try:
            if historical_data is None or len(historical_data) < 20:
                return self._generate_fallback_prediction(symbol)
            
            # Technical indicators calculation
            df = historical_data.copy()
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Moving Averages
            sma_20 = df['Close'].rolling(window=20).mean()
            sma_50 = df['Close'].rolling(window=50).mean()
            
            # MACD
            exp1 = df['Close'].ewm(span=12).mean()
            exp2 = df['Close'].ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            
            # Bollinger Bands
            bb_middle = df['Close'].rolling(window=20).mean()
            bb_std = df['Close'].rolling(window=20).std()
            bb_upper = bb_middle + (bb_std * 2)
            bb_lower = bb_middle - (bb_std * 2)
            
            # Volume analysis
            volume_sma = df['Volume'].rolling(window=20).mean()
            volume_ratio = df['Volume'] / volume_sma
            
            # Get latest values
            latest_data = {
                'rsi': rsi.iloc[-1] if not rsi.empty else 50,
                'price': df['Close'].iloc[-1],
                'sma_20': sma_20.iloc[-1] if not sma_20.empty else df['Close'].iloc[-1],
                'sma_50': sma_50.iloc[-1] if not sma_50.empty else df['Close'].iloc[-1],
                'macd': macd.iloc[-1] if not macd.empty else 0,
                'signal': signal.iloc[-1] if not signal.empty else 0,
                'bb_upper': bb_upper.iloc[-1] if not bb_upper.empty else df['Close'].iloc[-1],
                'bb_middle': bb_middle.iloc[-1] if not bb_middle.empty else df['Close'].iloc[-1],
                'bb_lower': bb_lower.iloc[-1] if not bb_lower.empty else df['Close'].iloc[-1],
                'volume_ratio': volume_ratio.iloc[-1] if not volume_ratio.empty else 1,
                'price_change_5d': (df['Close'].iloc[-1] / df['Close'].iloc[-6] - 1) * 100 if len(df) > 5 else 0,
                'volatility': df['Close'].pct_change().rolling(window=20).std().iloc[-1] * 100 if len(df) > 20 else 1
            }
            
            # Generate prediction based on technical analysis
            prediction = self._generate_technical_prediction(symbol, latest_data)
            
            return prediction
            
        except Exception as e:
            logger.error(f"Error in AI analysis for {symbol}: {e}")
            return self._generate_fallback_prediction(symbol)
    
    def _generate_technical_prediction(self, symbol, data):
        """Generate prediction based on technical indicators"""
        
        # Initialize scores
        bullish_signals = 0
        bearish_signals = 0
        total_signals = 0
        
        # RSI Analysis
        if data['rsi'] < 30:
            bullish_signals += 2  # Oversold
        elif data['rsi'] > 70:
            bearish_signals += 2  # Overbought
        elif 40 <= data['rsi'] <= 60:
            bullish_signals += 1  # Neutral to slightly bullish
        total_signals += 2
        
        # Moving Average Analysis
        if data['price'] > data['sma_20'] > data['sma_50']:
            bullish_signals += 2  # Strong uptrend
        elif data['price'] < data['sma_20'] < data['sma_50']:
            bearish_signals += 2  # Strong downtrend
        elif data['price'] > data['sma_20']:
            bullish_signals += 1  # Mild uptrend
        else:
            bearish_signals += 1  # Mild downtrend
        total_signals += 2
        
        # MACD Analysis
        if data['macd'] > data['signal'] and data['macd'] > 0:
            bullish_signals += 2  # Bullish crossover
        elif data['macd'] < data['signal'] and data['macd'] < 0:
            bearish_signals += 2  # Bearish crossover
        elif data['macd'] > data['signal']:
            bullish_signals += 1  # Mildly bullish
        else:
            bearish_signals += 1  # Mildly bearish
        total_signals += 2
        
        # Bollinger Bands Analysis
        if data['price'] < data['bb_lower']:
            bullish_signals += 2  # Below lower band - oversold
        elif data['price'] > data['bb_upper']:
            bearish_signals += 2  # Above upper band - overbought
        elif data['price'] > data['bb_middle']:
            bullish_signals += 1  # Above middle - bullish
        else:
            bearish_signals += 1  # Below middle - bearish
        total_signals += 2
        
        # Volume Analysis
        if data['volume_ratio'] > 1.5:
            bullish_signals += 1  # High volume supports trend
        elif data['volume_ratio'] < 0.5:
            bearish_signals += 1  # Low volume - weak trend
        total_signals += 1
        
        # Recent Price Action
        if data['price_change_5d'] > 2:
            bullish_signals += 1  # Strong recent performance
        elif data['price_change_5d'] < -2:
            bearish_signals += 1  # Weak recent performance
        total_signals += 1
        
        # Calculate final prediction
        if total_signals == 0:
            prediction = 'HOLD'
            confidence = 50
        else:
            bullish_score = (bullish_signals / total_signals) * 100
            bearish_score = (bearish_signals / total_signals) * 100
            
            if bullish_score > bearish_score + 10:
                prediction = 'UP'
                confidence = min(95, bullish_score)
            elif bearish_score > bullish_score + 10:
                prediction = 'DOWN'
                confidence = min(95, bearish_score)
            else:
                prediction = 'HOLD'
                confidence = 50 + abs(bullish_score - bearish_score) / 2
        
        # Generate detailed analysis
        analysis = {
            'symbol': symbol,
            'prediction': prediction,
            'confidence': round(confidence, 1),
            'up_probability': round(confidence if prediction == 'UP' else (100 - confidence) / 2, 1),
            'down_probability': round(confidence if prediction == 'DOWN' else (100 - confidence) / 2, 1),
            'hold_probability': round(100 - confidence if prediction == 'HOLD' else 0, 1),
            'technical_indicators': {
                'rsi': round(data['rsi'], 2),
                'macd': round(data['macd'], 4),
                'signal': round(data['signal'], 4),
                'price_vs_sma20': round(((data['price'] / data['sma_20']) - 1) * 100, 2),
                'volume_ratio': round(data['volume_ratio'], 2),
                'volatility': round(data['volatility'], 2)
            },
            'signals': {
                'bullish': bullish_signals,
                'bearish': bearish_signals,
                'total': total_signals
            },
            'analysis_text': self._generate_analysis_text(prediction, data, bullish_signals, bearish_signals),
            'timestamp': datetime.now(INDIAN_TIMEZONE).isoformat(),
            'analysis_type': 'technical'
        }
        
        return analysis
    
    def _generate_analysis_text(self, prediction, data, bullish_signals, bearish_signals):
        """Generate human-readable analysis text"""
        
        texts = []
        
        # RSI Analysis
        if data['rsi'] < 30:
            texts.append(f"RSI at {data['rsi']:.1f} indicates oversold conditions")
        elif data['rsi'] > 70:
            texts.append(f"RSI at {data['rsi']:.1f} indicates overbought conditions")
        else:
            texts.append(f"RSI at {data['rsi']:.1f} is in neutral range")
        
        # Moving Average Analysis
        if data['price'] > data['sma_20']:
            texts.append("Price is above 20-day SMA indicating bullish momentum")
        else:
            texts.append("Price is below 20-day SMA indicating bearish momentum")
        
        # MACD Analysis
        if data['macd'] > data['signal']:
            texts.append("MACD is above signal line suggesting upward momentum")
        else:
            texts.append("MACD is below signal line suggesting downward momentum")
        
        # Volume Analysis
        if data['volume_ratio'] > 1.2:
            texts.append(f"Volume ratio of {data['volume_ratio']:.1f} shows strong participation")
        elif data['volume_ratio'] < 0.8:
            texts.append(f"Volume ratio of {data['volume_ratio']:.1f} shows weak participation")
        
        # Overall sentiment
        if bullish_signals > bearish_signals * 1.5:
            texts.append("Overall technical indicators strongly suggest upward movement")
        elif bearish_signals > bullish_signals * 1.5:
            texts.append("Overall technical indicators strongly suggest downward movement")
        else:
            texts.append("Technical indicators show mixed signals with no clear direction")
        
        return " | ".join(texts)
    
    def _generate_fallback_prediction(self, symbol):
        """Generate fallback prediction when data is insufficient — always HOLD, never random"""
        return {
            'symbol': symbol,
            'prediction': 'HOLD',
            'confidence': 40.0,
            'up_probability': 30.0,
            'down_probability': 30.0,
            'hold_probability': 40.0,
            'technical_indicators': {},
            'signals': {'bullish': 0, 'bearish': 0, 'total': 0},
            'analysis_text': "Insufficient market data for technical analysis. Defaulting to HOLD — no directional signal available.",
            'timestamp': datetime.now(INDIAN_TIMEZONE).isoformat(),
            'analysis_type': 'fallback',
            'is_fallback': True
        }


# Global AI Analyzer
ai_analyzer = AIAnalyzer()

def get_market_session():
    """Get current market session with enhanced logic - 24/7 ACCESS ENABLED"""
    now = datetime.now(INDIAN_TIMEZONE).time()
    today = datetime.now(INDIAN_TIMEZONE).date()
    
    # 24/7 ACCESS - Always allow analysis and refresh
    # Check if today is a weekend
    if today.weekday() >= 5:  # Saturday, Sunday
        return {
            'status': 'closed', 
            'session': 'weekend', 
            'next_open': 'Monday 9:15 AM',
            'can_refresh': True,  # Always allow refresh
            'can_analyze': True    # Always allow analysis
        }
    
    # Pre-market hours
    if now < PRE_MARKET_ANALYSIS_TIME:
        return {
            'status': 'closed', 
            'session': 'pre_analysis', 
            'next_open': '9:15 AM',
            'can_refresh': True,  # Always allow refresh
            'can_analyze': True    # Always allow analysis
        }
    elif PRE_MARKET_ANALYSIS_TIME <= now < PRE_MARKET_START:
        return {
            'status': 'pre_analysis', 
            'session': 'pre_market_analysis', 
            'market_open': '9:15 AM',
            'can_refresh': True,  # Always allow refresh
            'can_analyze': True    # Always allow analysis
        }
    elif PRE_MARKET_START <= now < MARKET_START:
        return {
            'status': 'pre_market', 
            'session': 'pre_market', 
            'market_open': '9:15 AM',
            'can_refresh': True,  # Always allow refresh
            'can_analyze': True    # Always allow analysis
        }
    elif MARKET_START <= now < MARKET_END:
        return {
            'status': 'open', 
            'session': 'market_hours', 
            'market_close': '3:30 PM',
            'can_refresh': True,  # Always allow refresh
            'can_analyze': True    # Always allow analysis
        }
    else:
        # Convert time to datetime for comparison
        now_datetime = datetime.combine(today, now)
        market_end_datetime = datetime.combine(today, MARKET_END)
        
        if market_end_datetime <= now_datetime < market_end_datetime + timedelta(minutes=30):
            return {
                'status': 'post_market', 
                'session': 'post_market', 
                'next_open': 'Tomorrow 9:15 AM',
                'can_refresh': True,  # Always allow refresh
                'can_analyze': True    # Always allow analysis
            }
        else:
            return {
                'status': 'closed', 
                'session': 'after_hours', 
                'next_open': 'Tomorrow 9:15 AM',
                'can_refresh': True,  # Always allow refresh
                'can_analyze': True    # Always allow analysis
            }

def calculate_vwap(closes, highs, lows, volumes):
    """Calculate Volume Weighted Average Price (VWAP) over the period."""
    total_pv = 0.0
    total_v = 0.0
    for c, h, l, v in zip(closes, highs, lows, volumes):
        tp = (c + h + l) / 3.0
        total_pv += tp * v
        total_v += v
    return (total_pv / total_v) if total_v > 0 else (closes[0] if closes else 0.0)

def calculate_supertrend(highs, lows, closes, period=7, multiplier=3):
    """Calculate Supertrend direction and value for the latest bar."""
    try:
        # Check if enough data
        if len(closes) < period + 2:
            return (closes[0] if closes else 0.0), "NEUTRAL"
            
        atr_list = []
        for i in range(len(closes) - period):
            h_slice = highs[i:i+period]
            l_slice = lows[i:i+period]
            c_slice = closes[i:i+period]
            atr_list.append(calculate_atr(h_slice, l_slice, c_slice, period))
            
        # Reverse lists so that index 0 is oldest, index -1 is newest
        h = highs[:len(atr_list)+1][::-1]
        l = lows[:len(atr_list)+1][::-1]
        c = closes[:len(atr_list)+1][::-1]
        atrs = atr_list[::-1]
        
        trend = 1
        supertrend = 0.0
        upper_band = 0.0
        lower_band = 0.0
        
        for idx in range(len(atrs)):
            hl2 = (h[idx] + l[idx]) / 2.0
            basic_ub = hl2 + (multiplier * atrs[idx])
            basic_lb = hl2 - (multiplier * atrs[idx])
            
            if idx == 0:
                upper_band = basic_ub
                lower_band = basic_lb
                supertrend = upper_band
            else:
                if basic_ub < upper_band or c[idx-1] > upper_band:
                    upper_band = basic_ub
                if basic_lb > lower_band or c[idx-1] < lower_band:
                    lower_band = basic_lb
                    
                if trend == 1:
                    if c[idx] <= lower_band:
                        trend = -1
                        supertrend = upper_band
                    else:
                        supertrend = lower_band
                else:
                    if c[idx] >= upper_band:
                        trend = 1
                        supertrend = lower_band
                    else:
                        supertrend = upper_band
                        
        return supertrend, "BULLISH" if trend == 1 else "BEARISH"
    except Exception as e:
        logger.error(f"Error calculating Supertrend: {e}")
        return (closes[0] if closes else 0.0), "NEUTRAL"

def calculate_technical_indicators(symbol, historical_data=None):
    """Calculate comprehensive technical indicators for market analysis"""
    try:
        # Get historical data if not provided
        if historical_data is None:
            historical_data = get_day_by_day_historical_data(symbol, days=50)
        
        if not historical_data or len(historical_data) < 20:
            logger.warning(f"Insufficient data for technical indicators on {symbol}")
            return get_default_technical_indicators()
        
        # Extract prices and volumes (up to 40 days for Supertrend calculation)
        prices = [day['close'] for day in historical_data[:40]]
        volumes = [day['volume'] for day in historical_data[:40]]
        highs = [day['high'] for day in historical_data[:40]]
        lows = [day['low'] for day in historical_data[:40]]
        
        # Limit to 20 days for basic indicator parameters
        prices_20 = prices[:20]
        volumes_20 = volumes[:20]
        highs_20 = highs[:20]
        lows_20 = lows[:20]
        
        current_price = prices_20[0] if prices_20 else 0
        previous_price = prices_20[1] if len(prices_20) > 1 else current_price
        
        # Calculate RSI (14-period)
        rsi = calculate_rsi(prices_20, period=14)
        
        # Calculate MACD
        macd_line, signal_line, histogram = calculate_macd(prices_20)
        
        # Calculate support and resistance levels
        support_level, resistance_level = calculate_support_resistance(prices_20, highs_20, lows_20)
        
        # Calculate trend strength
        trend_strength = calculate_trend_strength(prices_20)
        
        # Calculate volatility (ATR-based)
        volatility = calculate_atr(highs_20, lows_20, prices_20, period=14)
        
        # Calculate market sentiment
        sentiment_score = calculate_market_sentiment(prices_20, volumes_20, rsi, macd_line)
        
        # Calculate VWAP
        vwap = calculate_vwap(prices_20, highs_20, lows_20, volumes_20)
        
        # Calculate Supertrend
        supertrend_value, supertrend_direction = calculate_supertrend(highs, lows, prices, period=7, multiplier=3)
        
        # Generate option strategy recommendation
        option_strategy = generate_option_strategy(
            current_price, previous_price, rsi, macd_line, signal_line, 
            trend_strength, volatility, sentiment_score
        )
        
        # Determine market trend
        market_trend = determine_market_trend(prices_20, trend_strength, rsi, macd_line)
        
        logger.info(f"Technical indicators calculated for {symbol}: RSI={rsi:.1f}, MACD={macd_line:.2f}, Trend={market_trend}, VWAP={vwap:.2f}, Supertrend={supertrend_value:.2f} ({supertrend_direction})")
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'previous_price': previous_price,
            'change': current_price - previous_price,
            'change_percent': ((current_price - previous_price) / previous_price * 100) if previous_price > 0 else 0,
            'market_trend': market_trend,
            'support_level': support_level,
            'resistance_level': resistance_level,
            'rsi': rsi,
            'macd': {
                'macd_line': macd_line,
                'signal_line': signal_line,
                'histogram': histogram
            },
            'volatility': volatility,
            'volatility_percent': (volatility / current_price * 100) if current_price > 0 else 0,
            'trend_strength': trend_strength,
            'sentiment_score': sentiment_score,
            'option_strategy': option_strategy,
            'vwap': round(vwap, 2),
            'supertrend': {
                'value': round(supertrend_value, 2),
                'direction': supertrend_direction
            },
            'data_points': len(prices_20),
            'last_updated': datetime.now(INDIAN_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
        }
        
    except Exception as e:
        logger.error(f"Error calculating technical indicators for {symbol}: {e}")
        return get_default_technical_indicators()

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index"""
    if len(prices) < period + 1:
        return 50.0
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    if len(prices) < slow:
        return 0, 0, 0
    
    # Calculate EMAs
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    # MACD line
    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    
    # Signal line (EMA of MACD)
    macd_values = [ema_fast[i] - ema_slow[i] for i in range(len(ema_fast))]
    signal_line = calculate_ema(macd_values, signal)
    
    # Histogram
    histogram = [m - s for m, s in zip(macd_line, signal_line)]
    
    return macd_line, signal_line, histogram

def calculate_ema(prices, period):
    """Calculate Exponential Moving Average"""
    if len(prices) < period:
        return [prices[-1]] * len(prices) if prices else []
    
    multiplier = 2 / (period + 1)
    ema = [prices[0]] * period # padding start
    ema[-1] = sum(prices[:period]) / period
    
    for price in prices[period:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    
    return ema

def calculate_support_resistance(prices, highs, lows):
    """Calculate dynamic support and resistance levels"""
    if len(prices) < 10:
        return prices[-1] * 0.98, prices[-1] * 1.02
    
    # Support: Recent lows + Fibonacci levels
    recent_lows = sorted(lows[:10])[:3]
    support_base = sum(recent_lows) / len(recent_lows)
    fib_support = support_base * 0.98
    
    # Resistance: Recent highs + Fibonacci levels  
    recent_highs = sorted(highs[:10], reverse=True)[:3]
    resistance_base = sum(recent_highs) / len(recent_highs)
    fib_resistance = resistance_base * 1.02
    
    return fib_support, fib_resistance

def calculate_trend_strength(prices):
    """Calculate trend strength using multiple methods"""
    if len(prices) < 10:
        return 0.5
    
    # Linear regression slope
    x = list(range(len(prices)))
    n = len(prices)
    sum_x = sum(x)
    sum_y = sum(prices)
    sum_xy = sum(x[i] * prices[i] for i in range(n))
    sum_x2 = sum(x[i]**2 for i in range(n))
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    
    # Normalize slope to -1 to 1 range
    max_slope = prices[-1] * 0.05  # 5% of current price as max slope
    trend_strength = max(-1, min(1, slope / max_slope))
    
    return (trend_strength + 1) / 2  # Convert to 0-1 range

def calculate_atr(highs, lows, closes, period=14):
    """Calculate Average True Range for volatility"""
    if len(highs) < period + 1:
        return closes[0] * 0.02 if closes else 0
    
    true_ranges = []
    for i in range(1, len(highs)):
        high_low = highs[i] - lows[i]
        high_close = abs(highs[i] - closes[i-1])
        low_close = abs(lows[i] - closes[i-1])
        true_range = max(high_low, high_close, low_close)
        true_ranges.append(true_range)
    
    atr = sum(true_ranges[-period:]) / period
    return atr

def calculate_market_sentiment(prices, volumes, rsi, macd):
    """Calculate market sentiment score (-1 to 1)"""
    try:
        # Price momentum sentiment
        price_momentum = (prices[0] - prices[-1]) / prices[-1] if len(prices) > 1 and prices[-1] > 0 else 0
        price_sentiment = max(-1, min(1, price_momentum * 10))  # Normalize
        
        # Volume sentiment
        avg_volume = sum(volumes) / len(volumes) if volumes else 1
        current_volume = volumes[0] if volumes else avg_volume
        volume_sentiment = (current_volume / avg_volume - 1) if avg_volume > 0 else 0
        volume_sentiment = max(-0.5, min(0.5, volume_sentiment))
        
        # RSI sentiment
        if rsi > 70:
            rsi_sentiment = -0.3  # Overbought
        elif rsi < 30:
            rsi_sentiment = 0.3   # Oversold
        else:
            rsi_sentiment = 0    # Neutral
        
        # MACD sentiment
        macd_sentiment = 0.2 if macd > 0 else -0.2
        
        # Combine sentiments
        total_sentiment = price_sentiment * 0.4 + volume_sentiment * 0.3 + rsi_sentiment * 0.2 + macd_sentiment * 0.1
        
        return max(-1, min(1, total_sentiment))
        
    except Exception as e:
        logger.error(f"Error calculating sentiment: {e}")
        return 0

def generate_option_strategy(current_price, previous_price, rsi, macd_line, signal_line, trend_strength, volatility, sentiment):
    """Generate option strategy recommendation"""
    try:
        # Initialize scores
        call_score = 0
        put_score = 0
        hold_score = 0
        
        # Trend analysis
        if trend_strength > 0.6:
            call_score += 2
        elif trend_strength < 0.4:
            put_score += 2
        else:
            hold_score += 1
        
        # RSI analysis
        if rsi > 70:
            put_score += 2  # Overbought - expect reversal
        elif rsi < 30:
            call_score += 2  # Oversold - expect bounce
        else:
            hold_score += 1
        
        # MACD analysis
        if macd_line > signal_line:
            call_score += 1
        else:
            put_score += 1
        
        # Volatility analysis
        if volatility > current_price * 0.02:  # High volatility
            hold_score += 1  # Prefer to wait in high volatility
        else:
            if trend_strength > 0.6:
                call_score += 1
            elif trend_strength < 0.4:
                put_score += 1
        
        # Sentiment analysis
        if sentiment > 0.3:
            call_score += sentiment
        elif sentiment < -0.3:
            put_score += abs(sentiment)
        else:
            hold_score += 0.5
        
        # Determine recommendation
        max_score = max(call_score, put_score, hold_score)
        
        if max_score == call_score:
            strategy = "BUY CALL"
            side = "CALL"
        elif max_score == put_score:
            strategy = "BUY PUT"
            side = "PUT"
        else:
            strategy = "HOLD"
            side = "HOLD"
        
        return {
            'strategy': strategy,
            'side': side,
            'call_score': call_score,
            'put_score': put_score,
            'hold_score': hold_score,
            'confidence': max_score / (call_score + put_score + hold_score) if (call_score + put_score + hold_score) > 0 else 0.5
        }
        
    except Exception as e:
        logger.error(f"Error generating option strategy: {e}")
        return {'strategy': 'HOLD', 'side': 'HOLD', 'confidence': 0.5}

def determine_market_trend(prices, trend_strength, rsi, macd):
    """Determine overall market trend"""
    try:
        trend_score = 0
        
        # Trend strength contribution
        if trend_strength > 0.7:
            trend_score += 3
            trend_name = "Strong Uptrend"
        elif trend_strength > 0.6:
            trend_score += 2
            trend_name = "Moderate Uptrend"
        elif trend_strength < 0.2:
            trend_score -= 3
            trend_name = "Strong Downtrend"
        elif trend_strength < 0.3:
            trend_score -= 2
            trend_name = "Moderate Downtrend"
        else:
            trend_score += 1
            trend_name = "Sideways"
        
        # RSI contribution
        if rsi > 50:
            trend_score += 1
        else:
            trend_score -= 1
        
        # MACD contribution
        if macd > 0:
            trend_score += 1
        else:
            trend_score -= 1
        
        # Final trend determination
        if trend_score >= 3:
            return f"Bullish ({trend_name})"
        elif trend_score <= -2:
            return f"Bearish ({trend_name})"
        else:
            return f"Neutral ({trend_name})"
            
    except Exception as e:
        logger.error(f"Error determining market trend: {e}")
        return "Unknown"

def get_default_technical_indicators():
    """Return default technical indicators when data is unavailable"""
    return {
        'symbol': 'UNKNOWN',
        'current_price': 0,
        'previous_price': 0,
        'change': 0,
        'change_percent': 0,
        'market_trend': 'No Data',
        'support_level': 0,
        'resistance_level': 0,
        'rsi': 50,
        'macd': {'macd_line': 0, 'signal_line': 0, 'histogram': 0},
        'volatility': 0,
        'volatility_percent': 0,
        'trend_strength': 0.5,
        'sentiment_score': 0,
        'option_strategy': {'strategy': 'HOLD', 'side': 'HOLD', 'confidence': 0.5},
        'vwap': 0,
        'supertrend': {'value': 0, 'direction': 'NEUTRAL'},
        'data_points': 0,
        'last_updated': datetime.now(INDIAN_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
    }

def get_news_query(symbol):
    """Map symbol/index to a clean query for NewsAPI"""
    if symbol == 'NIFTY_50':
        return 'Nifty 50'
    elif symbol == 'BANK_NIFTY':
        return 'Bank Nifty'
    elif symbol == 'SENSEX':
        return 'BSE Sensex'
    
    config = INDIAN_STOCKS_CONFIG.get(symbol)
    if config:
        name = config['name']
        for suffix in [' Ltd.', ' Limited', ' Corp.', ' Corp. of India']:
            name = name.replace(suffix, '')
        return name
    return symbol.replace('_', ' ')

def fetch_news_and_sentiment(symbol):
    """Fetch recent news from NewsAPI and calculate sentiment using TextBlob"""
    try:
        api_key = os.environ.get('NEWS_API_KEY')  # Security: keys ONLY from environment
        if not api_key:
            logger.warning("NEWS_API_KEY not found in environment")
            return {'articles': [], 'news_sentiment_score': 0.0, 'news_sentiment_label': 'Neutral'}

        query = get_news_query(symbol)
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}&language=en&sortBy=relevancy&pageSize=4"
        
        logger.info(f"Fetching news for {symbol} with query '{query}'")
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            logger.warning(f"NewsAPI returned status code {response.status_code}: {response.text}")
            return {'articles': [], 'news_sentiment_score': 0.0, 'news_sentiment_label': 'Neutral'}

        data = response.json()
        articles = data.get('articles', [])
        
        processed_articles = []
        sentiment_scores = []
        
        for art in articles:
            title = art.get('title', '')
            desc = art.get('description', '') or ''
            
            text_to_analyze = f"{title}. {desc}"
            if TextBlob is not None:
                blob = TextBlob(text_to_analyze)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
            else:
                polarity = 0.0
                subjectivity = 0.0
            
            if polarity > 0.1:
                label = 'Bullish'
            elif polarity < -0.1:
                label = 'Bearish'
            else:
                label = 'Neutral'
                
            sentiment_scores.append(polarity)
            
            published_str = art.get('publishedAt', '')
            if published_str:
                try:
                    dt = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ")
                    published_formatted = dt.strftime("%d %b %Y, %I:%M %p")
                except Exception:
                    published_formatted = published_str
            else:
                published_formatted = ""
                
            processed_articles.append({
                'title': title,
                'description': desc,
                'source': art.get('source', {}).get('name', 'Unknown'),
                'url': art.get('url', '#'),
                'published_at': published_formatted,
                'polarity': round(polarity, 2),
                'subjectivity': round(subjectivity, 2),
                'label': label
            })
            
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        
        if avg_sentiment > 0.1:
            overall_label = 'Bullish'
        elif avg_sentiment < -0.1:
            overall_label = 'Bearish'
        else:
            overall_label = 'Neutral'
            
        logger.info(f"Successfully processed {len(processed_articles)} articles for {symbol}. Avg sentiment: {avg_sentiment:.2f}")
        return {
            'articles': processed_articles,
            'news_sentiment_score': round(avg_sentiment, 2),
            'news_sentiment_label': overall_label
        }
        
    except Exception as e:
        logger.error(f"Error fetching news for {symbol}: {e}")
        return {'articles': [], 'news_sentiment_score': 0.0, 'news_sentiment_label': 'Neutral'}

def get_alphavantage_symbol(symbol):
    """Translate app symbol/config to AlphaVantage symbol"""
    config = INDIAN_MARKET_CONFIG.get(symbol) or INDIAN_STOCKS_CONFIG.get(symbol)
    if not config:
        return None
    yf_symbol = config['symbol']
    
    if yf_symbol.endswith('.NS'):
        return yf_symbol.replace('.NS', '.BSE')
    elif yf_symbol.startswith('^'):
        return yf_symbol.strip('^')
    return yf_symbol

def fetch_alphavantage_quote(symbol):
    """Fetch real-time stock quote from AlphaVantage as a fallback"""
    try:
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')  # Security: keys ONLY from environment
        av_symbol = get_alphavantage_symbol(symbol)
        
        if not api_key or not av_symbol:
            return None
            
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={av_symbol}&apikey={api_key}"
        logger.info(f"Fetching AlphaVantage fallback for {symbol} (AV symbol: {av_symbol})...")
        response = requests.get(url, timeout=5)
        
        if response.status_code != 200:
            return None
            
        data = response.json()
        quote = data.get('Global Quote', {})
        if not quote:
            logger.warning(f"AlphaVantage returned no Global Quote for {av_symbol}: {data}")
            return None
            
        price = float(quote.get('05. price', 0))
        if price == 0:
            return None
            
        open_val = float(quote.get('02. open', price))
        high_val = float(quote.get('03. high', price))
        low_val = float(quote.get('04. low', price))
        prev_close = float(quote.get('08. previous close', price))
        change = float(quote.get('09. change', 0))
        
        change_pct_str = quote.get('10. change percent', '0%')
        change_pct = float(change_pct_str.replace('%', '')) if change_pct_str else 0.0
        
        volume = int(quote.get('06. volume', 0))
        
        now = datetime.now(INDIAN_TIMEZONE)
        
        result = {
            'symbol': symbol,
            'name': (INDIAN_MARKET_CONFIG.get(symbol) or INDIAN_STOCKS_CONFIG.get(symbol))['display_name'],
            'price': round(price, 2),
            'change': round(change, 2),
            'change_percent': round(change_pct, 2),
            'open': round(open_val, 2),
            'high': round(high_val, 2),
            'low': round(low_val, 2),
            'previous_close': round(prev_close, 2),
            'volume': volume,
            'timestamp': format_time_neat(now),
            'data_source': 'alphavantage_fallback',
            'last_updated': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        logger.info(f"Successfully fetched AlphaVantage fallback data for {symbol}: ₹{price}")
        return result
    except Exception as e:
        logger.error(f"Error fetching AlphaVantage fallback for {symbol}: {e}")
        return None

def _format_market_data(symbol, name, latest_row, previous_close, data_source, now_dt, daily_high=None, daily_low=None):
    """Unified formatter for market data structures to prevent duplication."""
    current_price = float(latest_row['Close'])
    change = current_price - previous_close
    change_percent = (change / previous_close) * 100 if previous_close > 0 else 0
    
    high_val = daily_high if daily_high is not None else float(latest_row['High'])
    low_val = daily_low if daily_low is not None else float(latest_row['Low'])
    
    return {
        'symbol': symbol,
        'name': name,
        'price': round(current_price, 2),
        'change': round(change, 2),
        'change_percent': round(change_percent, 2),
        'open': round(float(latest_row['Open']), 2),
        'high': round(high_val, 2),
        'low': round(low_val, 2),
        'previous_close': round(previous_close, 2),
        'volume': int(latest_row['Volume']) if not pd.isna(latest_row['Volume']) else 0,
        'timestamp': format_time_neat(now_dt),
        'data_source': data_source,
        'last_updated': latest_row.name.strftime('%Y-%m-%d %H:%M:%S') if hasattr(latest_row.name, 'strftime') else now_dt.strftime('%Y-%m-%d %H:%M:%S')
    }

def get_current_market_data(symbol, retries=3):
    """Get current market data with highest accuracy and retry logic"""
    config = INDIAN_MARKET_CONFIG.get(symbol) or INDIAN_STOCKS_CONFIG.get(symbol)
    if not config:
        logger.error(f"Invalid symbol: {symbol}")
        return None
        
    # Check cache first
    cached_data = market_data_cache.get(symbol)
    if cached_data:
        return cached_data
        
    for attempt in range(retries):
        try:
            logger.info(f"Fetching market data for {symbol} (Attempt {attempt + 1}/{retries})...")
            ticker = yf.Ticker(config['symbol'])
            
            # Try multiple approaches for current data
            now = datetime.now(INDIAN_TIMEZONE)
            
            # Method 1: Try to get today's data (1-minute intervals)
            try:
                today_data = ticker.history(period="1d", interval="1m")
                if not today_data.empty:
                    latest = today_data.iloc[-1]
                    
                    # Get previous close for change calculation
                    yesterday_data = ticker.history(period="2d", interval="1d")
                    if len(yesterday_data) >= 2:
                        previous_close = float(yesterday_data.iloc[-2]['Close'])
                    else:
                        previous_close = float(latest['Close'])
                    
                    daily_high = float(today_data['High'].max())
                    daily_low = float(today_data['Low'].min())
                    
                    data = _format_market_data(symbol, config['display_name'], latest, previous_close, 'yahoo_finance_live', now, daily_high, daily_low)
                    logger.info(f"Successfully fetched live data for {symbol}: ₹{data['price']}")
                    market_data_cache.set(symbol, data)
                    return data
            except Exception as e:
                logger.warning(f"Live data method failed for {symbol}: {e}")
            
            # Method 2: Try daily data (recent 5 days)
            try:
                daily_data = ticker.history(period="5d", interval="1d")
                if not daily_data.empty:
                    latest = daily_data.iloc[-1]
                    
                    if len(daily_data) >= 2:
                        previous_close = float(daily_data.iloc[-2]['Close'])
                    else:
                        previous_close = float(latest['Close'])
                    
                    daily_high = float(latest['High'])
                    daily_low = float(latest['Low'])
                    
                    data = _format_market_data(symbol, config['display_name'], latest, previous_close, 'yahoo_finance_daily', now, daily_high, daily_low)
                    logger.info(f"Successfully fetched daily data for {symbol}: ₹{data['price']}")
                    market_data_cache.set(symbol, data)
                    return data
            except Exception as e:
                logger.warning(f"Daily data method failed for {symbol}: {e}")
            
            # Method 3: Try weekly data as last resort
            try:
                weekly_data = ticker.history(period="1wk", interval="1d")
                if not weekly_data.empty:
                    latest = weekly_data.iloc[-1]
                    
                    if len(weekly_data) >= 2:
                        previous_close = float(weekly_data.iloc[-2]['Close'])
                    else:
                        previous_close = float(latest['Close'])
                    
                    daily_high = float(latest['High'])
                    daily_low = float(latest['Low'])
                    
                    data = _format_market_data(symbol, config['display_name'], latest, previous_close, 'yahoo_finance_weekly', now, daily_high, daily_low)
                    logger.info(f"Successfully fetched weekly data for {symbol}: ₹{data['price']}")
                    market_data_cache.set(symbol, data)
                    return data
            except Exception as e:
                logger.warning(f"Weekly data method failed for {symbol}: {e}")
                
            # Wait before next attempt with exponential backoff
            if attempt < retries - 1:
                backoff_delay = min(2 ** attempt, 8)  # 1s, 2s, 4s (max 8s)
                time.sleep(backoff_delay)
                
        except Exception as e:
            logger.error(f"Error in attempt {attempt + 1} for {symbol}: {e}")
            if attempt < retries - 1:
                backoff_delay = min(2 ** attempt, 8)
                time.sleep(backoff_delay)
    
    logger.warning(f"All yfinance attempts failed for {symbol}. Trying AlphaVantage fallback...")
    av_data = fetch_alphavantage_quote(symbol)
    if av_data:
        market_data_cache.set(symbol, av_data)
        return av_data

    logger.error(f"All data sources and retries failed for {symbol}. Returning None.")
    return None

def get_day_by_day_historical_data(symbol, days=7):
    """Get day-by-day historical closing values with correct latest closing price"""
    try:
        config = INDIAN_MARKET_CONFIG.get(symbol) or INDIAN_STOCKS_CONFIG.get(symbol)
        ticker = yf.Ticker(config['symbol'])
        
        # Get historical data for specified days (recent data only)
        end_date = datetime.now(INDIAN_TIMEZONE)
        start_date = end_date - timedelta(days=days + 2)  # Get recent days only
        
        historical_data = ticker.history(start=start_date, end=end_date, interval="1d")
        
        if historical_data.empty:
            logger.warning(f"No historical data found for {symbol}")
            return []
        
        # Process data and get current price for reference
        current_data = get_current_market_data(symbol)
        current_price = current_data.get('price', 0) if current_data else 0
        
        # Sort by date (newest first)
        historical_data = historical_data.sort_index(ascending=False)
        
        data = []
        for i, (date, row) in enumerate(historical_data.iterrows()):
            if i >= days:  # Limit to requested days
                break
                
            # Get the close price
            close_price = float(row['Close'])
            
            # For the most recent day, adjust to match current data if it's today
            if i == 0 and current_price > 0:
                # Check if this is today's data
                today = end_date.date()
                data_date = date.date()
                if data_date == today:
                    # Use current price for today to maintain consistency
                    close_price = current_price
            
            # Calculate change from previous day
            if i + 1 < len(historical_data):
                prev_close = float(historical_data.iloc[i+1]['Close'])
            else:
                prev_close = close_price
            
            change = close_price - prev_close
            change_percent = (change / prev_close * 100) if prev_close > 0 else 0
            
            # Determine if it's a weekend
            day_of_week = date.strftime('%A')
            is_weekend = day_of_week in ['Saturday', 'Sunday']
            
            data.append({
                'date': date.strftime('%d %b %Y'),
                'day': day_of_week,
                'close': close_price,
                'change': change,
                'change_percent': change_percent,
                'high': float(row['High']),
                'low': float(row['Low']),
                'volume': int(row['Volume']) if not pd.isna(row['Volume']) else 0,
                'is_weekend': is_weekend
            })
        
        logger.info(f"Generated {len(data)} days of recent historical data for {symbol}")
        return data
        
    except Exception as e:
        logger.error(f"Error fetching historical data for {symbol}: {e}")
        return []

def format_time_neat(dt):
    """Format time in neat, professional format"""
    return dt.strftime('%I:%M %p')

# ── Candlestick chart timeframe configuration ──
CANDLE_TIMEFRAMES = {
    '5min':     {'period': '1d',   'interval': '5m',  'label': '5 Min'},
    '1hr':      {'period': '5d',   'interval': '1h',  'label': '1 Hour'},
    '1day':     {'period': '1mo',  'interval': '1d',  'label': '1 Day'},
    '1yr':      {'period': '1y',   'interval': '1d',  'label': '1 Year'},
    '3yr':      {'period': '3y',   'interval': '1wk', 'label': '3 Years'},
    '5yr':      {'period': '5y',   'interval': '1wk', 'label': '5 Years'},
    'lifetime': {'period': 'max',  'interval': '1mo', 'label': 'Lifetime'},
}

def get_candlestick_data(symbol, timeframe='1day'):
    """Get OHLC candlestick data for any timeframe"""
    try:
        config = INDIAN_MARKET_CONFIG.get(symbol) or INDIAN_STOCKS_CONFIG.get(symbol)
        ticker = yf.Ticker(config['symbol'])
        tf = CANDLE_TIMEFRAMES.get(timeframe, CANDLE_TIMEFRAMES['1day'])

        logger.info(f"Fetching candle data: {symbol} | period={tf['period']} interval={tf['interval']}")
        data = ticker.history(period=tf['period'], interval=tf['interval'])

        if data.empty:
            logger.warning(f"No candle data for {symbol}/{timeframe}, using fallback")
            return generate_fallback_candle_data(symbol, timeframe)

        # Build OHLC arrays
        dates, hover_dates, opens, highs, lows, closes, volumes = [], [], [], [], [], [], []
        for ts, row in data.iterrows():
            # Format date depending on timeframe
            if timeframe == '5min':
                dt_label = ts.strftime('%I:%M %p')
                hover_label = ts.strftime('%d %b %Y, %I:%M %p')
            elif timeframe == '1hr':
                dt_label = ts.strftime('%d %b %I %p')
                hover_label = ts.strftime('%d %b %Y, %I:%M %p')
            elif timeframe in ('1day', '1yr'):
                dt_label = ts.strftime('%d %b %Y')
                hover_label = ts.strftime('%d %b %Y')
            else:
                dt_label = ts.strftime('%b %Y')
                hover_label = ts.strftime('%B %Y')

            dates.append(dt_label)
            hover_dates.append(hover_label)
            opens.append(round(float(row['Open']), 2))
            highs.append(round(float(row['High']), 2))
            lows.append(round(float(row['Low']), 2))
            closes.append(round(float(row['Close']), 2))
            volumes.append(int(row['Volume']) if not pd.isna(row['Volume']) else 0)

        now = datetime.now(INDIAN_TIMEZONE)
        return {
            'symbol': symbol,
            'display_name': config['display_name'],
            'timeframe': timeframe,
            'timeframe_label': tf['label'],
            'dates': dates,
            'hover_dates': hover_dates,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': volumes,
            'data_points': len(dates),
            'date': now.strftime('%Y-%m-%d'),
            'data_source': 'yahoo_finance'
        }

    except Exception as e:
        logger.error(f"Error fetching candle data for {symbol}/{timeframe}: {e}")
        return generate_fallback_candle_data(symbol, timeframe)


def generate_fallback_candle_data(symbol, timeframe='1day'):
    """Generate realistic fallback OHLC candle data"""
    config = INDIAN_MARKET_CONFIG.get(symbol) or INDIAN_STOCKS_CONFIG.get(symbol)
    now = datetime.now(INDIAN_TIMEZONE)
    base_prices = {'NIFTY_50': 22450, 'BANK_NIFTY': 46200, 'SENSEX': 73800}
    base = base_prices.get(symbol, 22450)

    # Number of candles per timeframe
    candle_counts = {'5min': 75, '1hr': 30, '1day': 30, '1yr': 252, '3yr': 156, '5yr': 260, 'lifetime': 180}
    n = candle_counts.get(timeframe, 30)
    tf = CANDLE_TIMEFRAMES.get(timeframe, CANDLE_TIMEFRAMES['1day'])

    dates, hover_dates, opens, highs, lows, closes, volumes = [], [], [], [], [], [], []
    price = base
    for i in range(n):
        o = round(price + (np.random.random() - 0.5) * 20, 2)
        c = round(o + (np.random.random() - 0.48) * 40, 2)
        h = round(max(o, c) + np.random.random() * 15, 2)
        l = round(min(o, c) - np.random.random() * 15, 2)
        v = int(np.random.randint(5_000_000, 50_000_000))
        price = c

        if timeframe == '5min':
            dt = now - timedelta(minutes=(n - i) * 5)
            label = dt.strftime('%I:%M %p')
            hover_label = dt.strftime('%d %b %Y, %I:%M %p')
        elif timeframe == '1hr':
            dt = now - timedelta(hours=(n - i))
            label = dt.strftime('%d %b %I %p')
            hover_label = dt.strftime('%d %b %Y, %I:%M %p')
        elif timeframe in ('1day', '1yr'):
            dt = now - timedelta(days=(n - i))
            label = dt.strftime('%d %b %Y')
            hover_label = dt.strftime('%d %b %Y')
        else:
            dt = now - timedelta(weeks=(n - i))
            label = dt.strftime('%b %Y')
            hover_label = dt.strftime('%B %Y')

        dates.append(label)
        hover_dates.append(hover_label)
        opens.append(o)
        highs.append(h)
        lows.append(l)
        closes.append(c)
        volumes.append(v)

    return {
        'symbol': symbol,
        'display_name': config['display_name'],
        'timeframe': timeframe,
        'timeframe_label': tf['label'],
        'dates': dates,
        'hover_dates': hover_dates,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes,
        'data_points': len(dates),
        'date': now.strftime('%Y-%m-%d'),
        'data_source': 'simulated'
    }

def perform_pre_market_analysis():
    """Perform pre-market analysis at 8:45 AM"""
    logger.info("Performing pre-market analysis...")
    
    symbols = ['NIFTY_50', 'BANK_NIFTY', 'SENSEX']
    
    for symbol in symbols:
        try:
            # Get extended historical data for analysis
            config = INDIAN_MARKET_CONFIG[symbol]
            ticker = yf.Ticker(config['symbol'])
            historical_data = ticker.history(period="3mo", interval="1d")
            
            if not historical_data.empty:
                analysis = ai_analyzer.analyze_market_data(symbol, historical_data)
                pre_market_analysis[symbol] = analysis
                ai_predictions[symbol] = analysis  # Store for API access
                
                logger.info(f"Pre-market analysis completed for {symbol}: {analysis['prediction']} with {analysis['confidence']}% confidence")
            
        except Exception as e:
            logger.error(f"Error in pre-market analysis for {symbol}: {e}")
    
    # Broadcast to connected clients
    socketio.emit('pre_market_analysis_complete', {
        'predictions': pre_market_analysis,
        'timestamp': datetime.now(INDIAN_TIMEZONE).isoformat()
    })

def schedule_pre_market_analysis():
    """Schedule pre-market analysis"""
    schedule.every().day.at("08:45").do(perform_pre_market_analysis)
    
    # Run scheduler in background
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    logger.info("Pre-market analysis scheduler started for 8:45 AM daily")

    # Start background monitoring of active price alerts
    def monitor_price_alerts():
        logger.info("Starting background price alert monitor...")
        while True:
            try:
                active_alerts = user_db.get_active_alerts()
                for alert in active_alerts:
                    alert_id = alert['id']
                    user_id = alert['user_id']
                    symbol = alert['symbol']
                    threshold = alert['price_threshold']
                    condition = alert['condition']
                    username = alert['username']

                    # Fetch current market data (uses cache if fresh)
                    mdata = get_current_market_data(symbol)
                    if not mdata:
                        continue

                    current_price = mdata['price']
                    triggered = False
                    if condition == 'ABOVE' and current_price >= threshold:
                        triggered = True
                    elif condition == 'BELOW' and current_price <= threshold:
                        triggered = True

                    if triggered:
                        logger.info(f"Triggering alert {alert_id} for {username}: {symbol} {condition} {threshold} (current: {current_price})")
                        if user_db.mark_alert_triggered(alert_id):
                            # Broadcast alert via socketio
                            socketio.emit('alert_triggered', {
                                'alert_id': alert_id,
                                'user_id': user_id,
                                'username': username,
                                'symbol': symbol,
                                'price_threshold': threshold,
                                'condition': condition,
                                'current_price': current_price,
                                'message': f"Price alert triggered: {symbol} has gone {condition.lower()} {threshold} (Current: ₹{current_price:,.2f})"
                            })
            except Exception as e:
                logger.error(f"Error in price alert monitor: {e}")
            time.sleep(30)  # Check every 30 seconds

    alert_thread = threading.Thread(target=monitor_price_alerts, daemon=True)
    alert_thread.start()
    logger.info("Background price alert monitor thread started")

# ══════════════════════════════════════════════════════════════
# SECURITY MIDDLEWARE — Headers, Rate Limiting, Input Validation
# ══════════════════════════════════════════════════════════════

@app.after_request
def add_security_headers(response):
    """Add security headers to every response."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    # CSP: allow inline styles/scripts (needed for template), CDN resources, and data: URIs for favicon
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://unpkg.com https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data: https:; "
        "connect-src 'self' ws: wss:; "
    )
    return response


@app.before_request
def check_rate_limit():
    """Rate-limit API requests to prevent abuse."""
    if request.path.startswith('/api/'):
        client_ip = request.remote_addr or '127.0.0.1'
        if not rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for {client_ip} on {request.path}")
            return jsonify({
                'error': 'Rate limit exceeded. Please wait before making more requests.',
                'retry_after': RATE_LIMIT_WINDOW
            }), 429


def validate_symbol(symbol: str, allow_stocks: bool = False) -> Optional[str]:
    """Validate and sanitize symbol input. Returns error message or None if valid."""
    if not symbol or not isinstance(symbol, str):
        return 'Symbol is required'
    symbol = symbol.upper().strip()
    valid_set = VALID_INDEX_SYMBOLS
    if allow_stocks:
        valid_set = VALID_INDEX_SYMBOLS | set(INDIAN_STOCKS_CONFIG.keys()) if 'INDIAN_STOCKS_CONFIG' in globals() else VALID_INDEX_SYMBOLS
    if symbol not in valid_set:
        return f'Invalid symbol: {symbol}'
    return None




