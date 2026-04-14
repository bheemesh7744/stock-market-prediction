"""
Market Agent - Processes real-time market data and calculates technical indicators
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import sys
import os

logger = logging.getLogger(__name__)

class MarketAgent:
    """Agent for processing real-time market data and technical analysis"""
    
    def __init__(self):
        self.last_prices = {}
        self.indicators_cache = {}
        self.cache_timeout = 30  # Cache indicators for 30 seconds
    
    def process_market_data(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming market data and update technical indicators"""
        try:
            # Import here to avoid circular import
            from perfect_indian_app import calculate_technical_indicators
            
            current_price = market_data.get('price', 0)
            
            # Update price history
            if symbol not in self.last_prices:
                self.last_prices[symbol] = []
            
            self.last_prices[symbol].append(current_price)
            
            # Keep only last 20 prices for calculations
            if len(self.last_prices[symbol]) > 20:
                self.last_prices[symbol] = self.last_prices[symbol][-20:]
            
            # Calculate technical indicators
            indicators = calculate_technical_indicators(symbol)
            
            # Cache indicators
            self.indicators_cache[symbol] = {
                'data': indicators,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Market agent processed data for {symbol}: ₹{current_price}")
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'indicators': indicators,
                'price_history': self.last_prices[symbol][-10:],  # Last 10 prices
                'processed_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in market agent processing {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': str(e),
                'processed_at': datetime.now().isoformat()
            }
    
    def get_cached_indicators(self, symbol: str) -> Dict[str, Any]:
        """Get cached technical indicators for a symbol"""
        if symbol in self.indicators_cache:
            cache_entry = self.indicators_cache[symbol]
            
            # Check if cache is still valid
            from datetime import datetime
            cache_time = datetime.fromisoformat(cache_entry['timestamp'])
            current_time = datetime.now()
            
            if (current_time - cache_time).total_seconds() < self.cache_timeout:
                return cache_entry['data']
        
        return {}
    
    def get_market_summary(self, symbols: List[str]) -> Dict[str, Any]:
        """Generate market summary for multiple symbols"""
        try:
            summary = {}
            
            for symbol in symbols:
                indicators = self.get_cached_indicators(symbol)
                if indicators:
                    summary[symbol] = {
                        'symbol': symbol,
                        'trend': indicators.get('market_trend', 'Unknown'),
                        'volatility': indicators.get('volatility_percent', 0),
                        'rsi': indicators.get('rsi', 50),
                        'sentiment': indicators.get('sentiment_score', 0),
                        'last_update': indicators.get('last_updated', datetime.now().isoformat())
                    }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating market summary: {e}")
            return {}
    
    def detect_market_anomalies(self, symbol: str) -> Dict[str, Any]:
        """Detect market anomalies and unusual patterns"""
        try:
            indicators = self.get_cached_indicators(symbol)
            if not indicators:
                return {'symbol': symbol, 'anomalies': []}
            
            anomalies = []
            
            # Detect unusual volatility
            volatility = indicators.get('volatility_percent', 0)
            if volatility > 3.0:  # High volatility threshold
                anomalies.append({
                    'type': 'high_volatility',
                    'value': volatility,
                    'description': f'Unusually high volatility detected: {volatility:.2f}%'
                })
            
            # Detect RSI extremes
            rsi = indicators.get('rsi', 50)
            if rsi > 80:  # Overbought extreme
                anomalies.append({
                    'type': 'extreme_overbought',
                    'value': rsi,
                    'description': f'Extreme overbought condition: RSI {rsi:.1f}'
                })
            elif rsi < 20:  # Oversold extreme
                anomalies.append({
                    'type': 'extreme_oversold',
                    'value': rsi,
                    'description': f'Extreme oversold condition: RSI {rsi:.1f}'
                })
            
            return {
                'symbol': symbol,
                'anomalies': anomalies,
                'detection_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error detecting anomalies for {symbol}: {e}")
            return {'symbol': symbol, 'error': str(e)}

# Global market agent instance
market_agent = MarketAgent()

def process_market_tick(symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single market tick"""
    return market_agent.process_market_data(symbol, market_data)

def get_market_analysis(symbols: List[str]) -> Dict[str, Any]:
    """Get comprehensive market analysis"""
    return market_agent.get_market_summary(symbols)

def detect_anomalies(symbol: str) -> Dict[str, Any]:
    """Detect market anomalies"""
    return market_agent.detect_market_anomalies(symbol)
