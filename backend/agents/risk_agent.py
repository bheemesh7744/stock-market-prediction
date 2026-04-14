"""
Risk Agent - Calculates volatility, drawdown risk, and confidence scores
"""

import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import sys
import os
import math

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logger = logging.getLogger(__name__)

class RiskAgent:
    """Agent for calculating risk metrics and confidence scores"""
    
    def __init__(self):
        self.price_history = {}
        self.risk_metrics_cache = {}
        self.max_history_length = 50  # Keep last 50 price points
    
    def calculate_risk_metrics(self, symbol: str, market_data: Dict[str, Any], indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive risk metrics for a symbol"""
        try:
            current_price = market_data.get('price', 0)
            
            # Update price history
            if symbol not in self.price_history:
                self.price_history[symbol] = []
            
            self.price_history[symbol].append({
                'price': current_price,
                'timestamp': datetime.now(),
                'volume': market_data.get('volume', 0)
            })
            
            # Keep only recent history
            if len(self.price_history[symbol]) > self.max_history_length:
                self.price_history[symbol] = self.price_history[symbol][-self.max_history_length:]
            
            # Calculate risk metrics
            volatility = self._calculate_volatility(symbol)
            drawdown = self._calculate_drawdown(symbol)
            var = self._calculate_var(symbol)
            sharpe_ratio = self._calculate_sharpe_ratio(symbol)
            confidence_score = self._calculate_confidence_score(symbol, indicators)
            
            risk_metrics = {
                'symbol': symbol,
                'current_price': current_price,
                'volatility': volatility,
                'volatility_percent': (volatility / current_price * 100) if current_price > 0 else 0,
                'max_drawdown': drawdown['max_drawdown'],
                'current_drawdown': drawdown['current_drawdown'],
                'drawdown_percent': drawdown['drawdown_percent'],
                'var_95': var['var_95'],
                'var_99': var['var_99'],
                'sharpe_ratio': sharpe_ratio,
                'confidence_score': confidence_score,
                'risk_level': self._determine_risk_level(volatility, drawdown['max_drawdown']),
                'risk_factors': self._identify_risk_factors(symbol, indicators),
                'calculated_at': datetime.now().isoformat()
            }
            
            # Cache risk metrics
            self.risk_metrics_cache[symbol] = risk_metrics
            
            logger.info(f"Risk agent calculated metrics for {symbol}: Volatility {volatility:.2f}, Confidence {confidence_score:.2f}")
            
            return risk_metrics
            
        except Exception as e:
            logger.error(f"Error calculating risk metrics for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': str(e),
                'calculated_at': datetime.now().isoformat()
            }
    
    def _calculate_volatility(self, symbol: str) -> float:
        """Calculate price volatility using standard deviation"""
        try:
            if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
                return 0.0
            
            prices = [entry['price'] for entry in self.price_history[symbol]]
            
            # Calculate daily returns
            returns = []
            for i in range(1, len(prices)):
                if prices[i-1] > 0:
                    returns.append((prices[i] - prices[i-1]) / prices[i-1])
            
            if len(returns) < 2:
                return 0.0
            
            # Calculate standard deviation
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
            volatility = math.sqrt(variance)
            
            return volatility
            
        except Exception as e:
            logger.error(f"Error calculating volatility: {e}")
            return 0.0
    
    def _calculate_drawdown(self, symbol: str) -> Dict[str, Any]:
        """Calculate drawdown metrics"""
        try:
            if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
                return {
                    'max_drawdown': 0.0,
                    'current_drawdown': 0.0,
                    'drawdown_percent': 0.0
                }
            
            prices = [entry['price'] for entry in self.price_history[symbol]]
            
            # Find peak and trough
            peak = max(prices)
            current_price = prices[-1]
            
            # Calculate current drawdown
            current_drawdown = peak - current_price
            current_drawdown_percent = (current_drawdown / peak * 100) if peak > 0 else 0
            
            # Calculate maximum drawdown
            max_drawdown = 0.0
            running_peak = prices[0]
            
            for price in prices:
                if price > running_peak:
                    running_peak = price
                
                drawdown = running_peak - price
                if drawdown > max_drawdown:
                    max_drawdown = drawdown
            
            max_drawdown_percent = (max_drawdown / peak * 100) if peak > 0 else 0
            
            return {
                'max_drawdown': max_drawdown,
                'current_drawdown': current_drawdown,
                'drawdown_percent': current_drawdown_percent,
                'max_drawdown_percent': max_drawdown_percent
            }
            
        except Exception as e:
            logger.error(f"Error calculating drawdown: {e}")
            return {
                'max_drawdown': 0.0,
                'current_drawdown': 0.0,
                'drawdown_percent': 0.0
            }
    
    def _calculate_var(self, symbol: str, confidence_levels: List[float] = [0.95, 0.99]) -> Dict[str, float]:
        """Calculate Value at Risk (VaR)"""
        try:
            if symbol not in self.price_history or len(self.price_history[symbol]) < 10:
                return {'var_95': 0.0, 'var_99': 0.0}
            
            prices = [entry['price'] for entry in self.price_history[symbol]]
            
            # Calculate returns
            returns = []
            for i in range(1, len(prices)):
                if prices[i-1] > 0:
                    returns.append((prices[i] - prices[i-1]) / prices[i-1])
            
            if len(returns) < 5:
                return {'var_95': 0.0, 'var_99': 0.0}
            
            # Sort returns
            sorted_returns = sorted(returns)
            
            # Calculate VaR at different confidence levels
            var_results = {}
            for confidence in confidence_levels:
                var_index = int((1 - confidence) * len(sorted_returns))
                var_index = max(0, var_index)
                var = abs(sorted_returns[var_index])
                var_results[f'var_{int(confidence * 100)}'] = var
            
            return var_results
            
        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return {'var_95': 0.0, 'var_99': 0.0}
    
    def _calculate_sharpe_ratio(self, symbol: str, risk_free_rate: float = 0.06) -> float:
        """Calculate Sharpe ratio"""
        try:
            if symbol not in self.price_history or len(self.price_history[symbol]) < 2:
                return 0.0
            
            prices = [entry['price'] for entry in self.price_history[symbol]]
            
            # Calculate returns
            returns = []
            for i in range(1, len(prices)):
                if prices[i-1] > 0:
                    returns.append((prices[i] - prices[i-1]) / prices[i-1])
            
            if len(returns) < 2:
                return 0.0
            
            # Calculate average return and volatility
            avg_return = sum(returns) / len(returns)
            volatility = self._calculate_volatility(symbol)
            
            # Calculate Sharpe ratio (annualized)
            if volatility > 0:
                sharpe_ratio = (avg_return * 252 - risk_free_rate) / (volatility * math.sqrt(252))
            else:
                sharpe_ratio = 0.0
            
            return sharpe_ratio
            
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0.0
    
    def _calculate_confidence_score(self, symbol: str, indicators: Dict[str, Any]) -> float:
        """Calculate confidence score based on multiple factors"""
        try:
            confidence_factors = []
            
            # Volatility factor (lower volatility = higher confidence)
            volatility = indicators.get('volatility_percent', 0)
            volatility_confidence = max(0.3, 1.0 - (volatility / 5.0))  # Normalize to 0.3-1.0
            confidence_factors.append(volatility_confidence)
            
            # Trend strength factor
            trend_strength = indicators.get('trend_strength', 0.5)
            confidence_factors.append(trend_strength)
            
            # RSI factor (neutral RSI = higher confidence)
            rsi = indicators.get('rsi', 50)
            if 40 <= rsi <= 60:
                rsi_confidence = 0.8
            elif 30 <= rsi <= 70:
                rsi_confidence = 0.6
            else:
                rsi_confidence = 0.4
            confidence_factors.append(rsi_confidence)
            
            # MACD factor
            macd = indicators.get('macd', {})
            macd_line = macd.get('macd_line', 0)
            signal_line = macd.get('signal_line', 0)
            macd_strength = abs(macd_line - signal_line)
            macd_confidence = max(0.4, 1.0 - macd_strength)
            confidence_factors.append(macd_confidence)
            
            # Calculate weighted average
            weights = [0.3, 0.3, 0.2, 0.2]  # Volatility, Trend, RSI, MACD
            confidence = sum(f * w for f, w in zip(confidence_factors, weights))
            
            return max(0.1, min(1.0, confidence))  # Clamp between 0.1 and 1.0
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {e}")
            return 0.5
    
    def _determine_risk_level(self, volatility: float, max_drawdown: float) -> str:
        """Determine overall risk level"""
        try:
            volatility_score = min(3, int(volatility * 100 / 2))  # 0-3 based on volatility
            drawdown_score = min(3, int(max_drawdown / 100))  # 0-3 based on drawdown
            
            total_score = volatility_score + drawdown_score
            
            if total_score >= 5:
                return "Very High"
            elif total_score >= 3:
                return "High"
            elif total_score >= 2:
                return "Medium"
            else:
                return "Low"
                
        except Exception as e:
            logger.error(f"Error determining risk level: {e}")
            return "Unknown"
    
    def _identify_risk_factors(self, symbol: str, indicators: Dict[str, Any]) -> List[str]:
        """Identify specific risk factors"""
        try:
            risk_factors = []
            
            # High volatility
            volatility = indicators.get('volatility_percent', 0)
            if volatility > 2.0:
                risk_factors.append(f"High volatility: {volatility:.2f}%")
            
            # Extreme RSI
            rsi = indicators.get('rsi', 50)
            if rsi > 80:
                risk_factors.append(f"Extreme overbought: RSI {rsi:.1f}")
            elif rsi < 20:
                risk_factors.append(f"Extreme oversold: RSI {rsi:.1f}")
            
            # Negative sentiment
            sentiment = indicators.get('sentiment_score', 0)
            if sentiment < -0.5:
                risk_factors.append(f"Strong bearish sentiment: {sentiment:.2f}")
            
            # Low trend strength
            trend_strength = indicators.get('trend_strength', 0.5)
            if trend_strength < 0.3:
                risk_factors.append(f"Weak trend strength: {trend_strength:.2f}")
            
            # Check recent drawdown
            if symbol in self.risk_metrics_cache:
                current_drawdown = self.risk_metrics_cache[symbol].get('current_drawdown', 0)
                if current_drawdown > 500:  # More than 500 points drawdown
                    risk_factors.append(f"Significant drawdown: {current_drawdown:.2f}")
            
            return risk_factors
            
        except Exception as e:
            logger.error(f"Error identifying risk factors: {e}")
            return []
    
    def get_portfolio_risk_summary(self, symbols: List[str]) -> Dict[str, Any]:
        """Get portfolio-level risk summary"""
        try:
            portfolio_risk = {
                'symbols': [],
                'total_volatility': 0,
                'avg_confidence': 0,
                'risk_distribution': {'Low': 0, 'Medium': 0, 'High': 0, 'Very High': 0},
                'portfolio_var': 0,
                'calculated_at': datetime.now().isoformat()
            }
            
            for symbol in symbols:
                if symbol in self.risk_metrics_cache:
                    risk_data = self.risk_metrics_cache[symbol]
                    portfolio_risk['symbols'].append(symbol)
                    portfolio_risk['total_volatility'] += risk_data.get('volatility', 0)
                    portfolio_risk['avg_confidence'] += risk_data.get('confidence_score', 0)
                    
                    risk_level = risk_data.get('risk_level', 'Unknown')
                    if risk_level in portfolio_risk['risk_distribution']:
                        portfolio_risk['risk_distribution'][risk_level] += 1
            
            # Calculate averages
            if portfolio_risk['symbols']:
                portfolio_risk['avg_confidence'] /= len(portfolio_risk['symbols'])
            
            return portfolio_risk
            
        except Exception as e:
            logger.error(f"Error calculating portfolio risk summary: {e}")
            return {'error': str(e), 'calculated_at': datetime.now().isoformat()}

# Global risk agent instance
risk_agent = RiskAgent()

def calculate_risk_metrics(symbol: str, market_data: Dict[str, Any], indicators: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate risk metrics for a symbol"""
    return risk_agent.calculate_risk_metrics(symbol, market_data, indicators)

def get_portfolio_risk(symbols: List[str]) -> Dict[str, Any]:
    """Get portfolio risk summary"""
    return risk_agent.get_portfolio_risk_summary(symbols)
