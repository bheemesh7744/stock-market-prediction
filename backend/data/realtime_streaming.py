"""
Real-Time Data Streaming Engine
================================
Simulates real-time tick-data streaming for Indian stocks.
Uses yfinance baseline prices and adds realistic micro-fluctuations
to simulate live market tick data at 1-2 second intervals.

In a production environment, this would connect to a real broker
WebSocket (e.g., Zerodha Kite, TrueData, Alpaca) for millisecond-level
tick updates. This simulation demonstrates the architecture.
"""

import logging
import threading
import time
import random
import uuid
from collections import deque
from datetime import datetime
from typing import Dict, Any, Optional, List, Set

import pytz

logger = logging.getLogger(__name__)

# ══════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════

INDIAN_TIMEZONE = pytz.timezone('Asia/Kolkata')
MARKET_OPEN_TIME = datetime.strptime("09:15", "%H:%M").time()
MARKET_CLOSE_TIME = datetime.strptime("15:30", "%H:%M").time()

# Tick generation settings
TICK_INTERVAL_MARKET_HOURS = 2.0      # seconds between ticks during market hours (reduced for faster updates)
TICK_INTERVAL_OFF_HOURS = 30.0        # seconds between ticks during off-hours
MAX_TICKS_PER_SYMBOL = 500          # circular buffer size
PRICE_FLUCTUATION_PCT = 0.0001       # ±0.01% micro-fluctuation range
SPREAD_PCT = 0.0005                 # 0.05% bid-ask spread


# ══════════════════════════════════════════════════════════════
# TICK DATA BUFFER — Thread-safe circular buffer
# ══════════════════════════════════════════════════════════════

class TickDataBuffer:
    """Thread-safe circular buffer for storing recent tick data per symbol."""

    def __init__(self, max_ticks: int = MAX_TICKS_PER_SYMBOL):
        self._buffers: Dict[str, deque] = {}
        self._lock = threading.Lock()
        self._max_ticks = max_ticks

    def add_tick(self, symbol: str, tick_data: Dict[str, Any]) -> None:
        """Add a tick to the buffer for a given symbol."""
        with self._lock:
            if symbol not in self._buffers:
                self._buffers[symbol] = deque(maxlen=self._max_ticks)
            self._buffers[symbol].append(tick_data)

    def get_recent(self, symbol: str, count: int = 50) -> List[Dict[str, Any]]:
        """Get the most recent N ticks for a symbol."""
        with self._lock:
            if symbol not in self._buffers:
                return []
            buf = self._buffers[symbol]
            return list(buf)[-count:]

    def get_all(self, symbol: str) -> List[Dict[str, Any]]:
        """Get all ticks in the buffer for a symbol."""
        with self._lock:
            if symbol not in self._buffers:
                return []
            return list(self._buffers[symbol])

    def clear(self, symbol: str) -> None:
        """Clear all ticks for a symbol."""
        with self._lock:
            if symbol in self._buffers:
                self._buffers[symbol].clear()



    def get_tick_count(self, symbol: str) -> int:
        """Get number of ticks stored for a symbol."""
        with self._lock:
            return len(self._buffers.get(symbol, []))

    def get_total_ticks(self) -> int:
        """Get total number of ticks across all symbols."""
        with self._lock:
            return sum(len(buf) for buf in self._buffers.values())


# ══════════════════════════════════════════════════════════════
# REALTIME STREAMING ENGINE
# ══════════════════════════════════════════════════════════════

class RealtimeStreamingEngine:
    """
    Real-Time Data Streaming Engine.
    
    Simulates market tick data by taking yfinance baseline prices and
    adding realistic micro-fluctuations. Designed to be swapped with
    a real broker WebSocket in production.
    
    Usage:
        engine = RealtimeStreamingEngine()
        engine.subscribe('RELIANCE')
        engine.start()
        # ... ticks are now being generated ...
        ticks = engine.get_tick_buffer('RELIANCE')
        engine.stop()
    """

    def __init__(self):
        self._tick_buffer = TickDataBuffer()
        self._subscribed_symbols: Set[str] = set()
        self._base_prices: Dict[str, float] = {}
        self._last_prices: Dict[str, float] = {}
        self._is_active = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._start_time: Optional[float] = None
        self._total_ticks_generated = 0
        self._last_tick_time: Optional[str] = None
        self._tick_callbacks: List[callable] = []

        # Default base prices for major indices and stocks (fallback)
        self._default_prices = {
            'NIFTY_50': 24200.0,
            'BANK_NIFTY': 57950.0,
            'SENSEX': 77530.0,
            'RELIANCE': 1300.0,
            'TCS': 2085.0,
            'HDFCBANK': 825.0,
            'INFY': 1070.0,
            'ICICIBANK': 1400.0,
            'HINDUNILVR': 2165.0,
            'SBIN': 1030.0,
            'BHARTIARTL': 1910.0,
            'ITC': 285.0,
            'KOTAKBANK': 380.0,
            'LT': 3930.0,
            'AXISBANK': 1320.0,
            'BAJFINANCE': 1010.0,
            'MARUTI': 13920.0,
            'TATAMOTORS': 950.0,
            'TATASTEEL': 192.0,
            'SUNPHARMA': 1945.0,
            'ADANIENT': 3165.0,
            'WIPRO': 176.0,
            'POWERGRID': 283.0,
        }

        logger.info("RealtimeStreamingEngine initialized")

    def subscribe(self, symbol: str) -> None:
        """Subscribe to tick data for a symbol."""
        with self._lock:
            symbol = symbol.upper().strip()
            self._subscribed_symbols.add(symbol)
            if symbol not in self._last_prices:
                self._last_prices[symbol] = self._default_prices.get(symbol, 1000.0)
                self._base_prices[symbol] = self._last_prices[symbol]
            logger.info(f"Subscribed to tick stream: {symbol}")

    def unsubscribe(self, symbol: str) -> None:
        """Unsubscribe from tick data for a symbol."""
        with self._lock:
            symbol = symbol.upper().strip()
            self._subscribed_symbols.discard(symbol)
            logger.info(f"Unsubscribed from tick stream: {symbol}")

    def set_base_price(self, symbol: str, price: float) -> None:
        """Set the baseline price for a symbol (typically from yfinance)."""
        with self._lock:
            self._base_prices[symbol] = price
            # Always align last price with the new real price
            self._last_prices[symbol] = price

    def register_callback(self, callback: callable) -> None:
        """Register a callback function to be called on each new tick."""
        self._tick_callbacks.append(callback)

    def start(self) -> None:
        """Start the streaming engine in a background thread."""
        if self._is_active:
            logger.warning("Streaming engine is already running")
            return

        self._is_active = True
        self._start_time = time.time()
        self._thread = threading.Thread(target=self._stream_loop, daemon=True)
        self._thread.start()
        logger.info("Real-time streaming engine STARTED")

    def stop(self) -> None:
        """Stop the streaming engine."""
        self._is_active = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        logger.info("Real-time streaming engine STOPPED")

    def get_tick_buffer(self, symbol: str, count: int = 50) -> List[Dict[str, Any]]:
        """Get recent tick data for a symbol."""
        return self._tick_buffer.get_recent(symbol, count)



    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the streaming engine."""
        now = datetime.now(INDIAN_TIMEZONE)
        is_market_hours = self._is_market_hours(now)

        uptime = 0.0
        if self._start_time:
            uptime = time.time() - self._start_time

        # Calculate tick rate
        tick_rate = 0.0
        if uptime > 0:
            tick_rate = round(self._total_ticks_generated / uptime, 2)

        return {
            'is_active': self._is_active,
            'is_market_hours': is_market_hours,
            'connected_subscribers': len(self._subscribed_symbols),
            'symbols_streaming': sorted(list(self._subscribed_symbols)),
            'tick_rate_per_second': tick_rate,
            'total_ticks_generated': self._total_ticks_generated,
            'uptime_seconds': round(uptime, 1),
            'last_tick_time': self._last_tick_time,
            'tick_interval': TICK_INTERVAL_MARKET_HOURS if is_market_hours else TICK_INTERVAL_OFF_HOURS,
            'buffer_size_per_symbol': MAX_TICKS_PER_SYMBOL,
            'total_buffered_ticks': self._tick_buffer.get_total_ticks(),
            'current_time_ist': now.strftime('%Y-%m-%d %H:%M:%S IST'),
            'engine_type': 'simulated_tick_stream',
            'note': 'Production deployment would use Zerodha Kite / TrueData WebSocket'
        }

    def _is_market_hours(self, now: datetime) -> bool:
        """Check if current time is within Indian market hours."""
        current_time = now.time()
        today = now.date()
        # Weekend check
        if today.weekday() >= 5:
            return False
        return MARKET_OPEN_TIME <= current_time <= MARKET_CLOSE_TIME

    def _stream_loop(self) -> None:
        """Main streaming loop — runs in background thread."""
        logger.info("Streaming loop started")

        while self._is_active:
            try:
                now = datetime.now(INDIAN_TIMEZONE)
                is_market = self._is_market_hours(now)

                with self._lock:
                    symbols_to_stream = list(self._subscribed_symbols)

                for symbol in symbols_to_stream:
                    try:
                        tick = self._generate_tick(symbol, now, is_market)
                        self._tick_buffer.add_tick(symbol, tick)
                        self._total_ticks_generated += 1
                        self._last_tick_time = tick['timestamp']

                        # Notify callbacks (e.g., SocketIO broadcast)
                        for callback in self._tick_callbacks:
                            try:
                                callback(tick)
                            except Exception as cb_err:
                                logger.error(f"Tick callback error: {cb_err}")

                    except Exception as tick_err:
                        logger.error(f"Error generating tick for {symbol}: {tick_err}")

                # Sleep based on market hours
                interval = TICK_INTERVAL_MARKET_HOURS if is_market else TICK_INTERVAL_OFF_HOURS
                # Add slight randomness to avoid perfectly periodic ticks
                jitter = random.uniform(-0.2, 0.2) if is_market else 0
                time.sleep(max(0.5, interval + jitter))

            except Exception as loop_err:
                logger.error(f"Streaming loop error: {loop_err}")
                time.sleep(5)

        logger.info("Streaming loop ended")

    def _generate_tick(self, symbol: str, now: datetime, is_market: bool) -> Dict[str, Any]:
        """Generate a single simulated tick for a symbol."""
        base_price = self._base_prices.get(symbol, 1000.0)
        last_price = self._last_prices.get(symbol, base_price)

        # Generate micro-fluctuation
        if is_market:
            # During market hours: more volatile, realistic movement
            fluctuation_pct = random.gauss(0, PRICE_FLUCTUATION_PCT)
            # Slight mean-reversion towards base price
            reversion = (base_price - last_price) / base_price * 0.01
            fluctuation_pct += reversion
        else:
            # Off-hours: very small movements
            fluctuation_pct = random.gauss(0, PRICE_FLUCTUATION_PCT * 0.1)

        new_price = round(last_price * (1 + fluctuation_pct), 2)

        # Ensure price doesn't go negative or deviate too far from base
        new_price = max(new_price, base_price * 0.9)
        new_price = min(new_price, base_price * 1.1)

        # Calculate bid-ask spread
        spread = round(new_price * SPREAD_PCT, 2)
        bid = round(new_price - spread / 2, 2)
        ask = round(new_price + spread / 2, 2)

        # Calculate change from base
        change = round(new_price - base_price, 2)
        change_pct = round((change / base_price) * 100, 4) if base_price > 0 else 0

        # Simulate volume (higher during market hours)
        if is_market:
            volume = random.randint(1000, 50000)
        else:
            volume = random.randint(10, 500)

        # Update last price
        with self._lock:
            self._last_prices[symbol] = new_price

        tick = {
            'tick_id': str(uuid.uuid4())[:12],
            'symbol': symbol,
            'price': new_price,
            'change': change,
            'change_percent': change_pct,
            'bid': bid,
            'ask': ask,
            'spread': round(spread, 2),
            'volume': volume,
            'timestamp': now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'timestamp_epoch': time.time(),
            'is_market_hours': is_market,
            'data_source': 'realtime_tick_stream'
        }

        return tick


# ══════════════════════════════════════════════════════════════
# MODULE-LEVEL SINGLETON & HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

streaming_engine = RealtimeStreamingEngine()


def get_streaming_engine() -> RealtimeStreamingEngine:
    """Get the global streaming engine instance."""
    return streaming_engine


def get_streaming_status() -> Dict[str, Any]:
    """Get the current status of the streaming engine."""
    return streaming_engine.get_status()


def start_streaming(symbols: Optional[List[str]] = None) -> None:
    """Start streaming with optional initial symbol list."""
    if symbols:
        for s in symbols:
            streaming_engine.subscribe(s)
    streaming_engine.start()


def stop_streaming() -> None:
    """Stop the streaming engine."""
    streaming_engine.stop()
