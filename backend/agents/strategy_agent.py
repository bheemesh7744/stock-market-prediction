"""
Strategy Agent - Determines possible trading strategies based on market analysis
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logger = logging.getLogger(__name__)

class StrategyAgent:
    """Agent for determining trading strategies based on technical and market analysis"""
    
    def __init__(self):
        self.strategy_weights = {
            'trend': 0.3,
            'momentum': 0.25,
            'volatility': 0.2,
            'volume': 0.15,
            'support_resistance': 0.1
        }
    
    def analyze_strategy_opportunities(self, symbol: str, indicators: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trading strategy opportunities based on indicators and market data"""
        try:
            strategies = []
            
            # Trend Following Strategy
            trend_strategy = self._analyze_trend_strategy(indicators, market_data)
            if trend_strategy['score'] > 0.6:
                strategies.append(trend_strategy)
            
            # Mean Reversion Strategy
            mean_reversion_strategy = self._analyze_mean_reversion_strategy(indicators, market_data)
            if mean_reversion_strategy['score'] > 0.6:
                strategies.append(mean_reversion_strategy)
            
            # Breakout Strategy
            breakout_strategy = self._analyze_breakout_strategy(indicators, market_data)
            if breakout_strategy['score'] > 0.6:
                strategies.append(breakout_strategy)
            
            # Momentum Strategy
            momentum_strategy = self._analyze_momentum_strategy(indicators, market_data)
            if momentum_strategy['score'] > 0.6:
                strategies.append(momentum_strategy)
            
            # Select best strategy
            best_strategy = max(strategies, key=lambda x: x['score']) if strategies else self._get_default_strategy()
            
            logger.info(f"Strategy agent analyzed {len(strategies)} opportunities for {symbol}")
            
            return {
                'symbol': symbol,
                'best_strategy': best_strategy,
                'all_strategies': strategies,
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in strategy analysis for {symbol}: {e}")
            return {
                'symbol': symbol,
                'error': str(e),
                'best_strategy': self._get_default_strategy(),
                'all_strategies': [],
                'analysis_time': datetime.now().isoformat()
            }
    
    def _analyze_trend_strategy(self, indicators: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trend following strategy"""
        try:
            score = 0
            reasoning = []
            
            # Check trend strength
            trend_strength = indicators.get('trend_strength', 0.5)
            if trend_strength > 0.7:
                score += 0.4
                reasoning.append(f"Strong trend detected: {trend_strength:.2f}")
            elif trend_strength > 0.6:
                score += 0.2
                reasoning.append(f"Moderate trend: {trend_strength:.2f}")
            
            # Check MACD
            macd = indicators.get('macd', {})
            macd_line = macd.get('macd_line', 0)
            signal_line = macd.get('signal_line', 0)
            
            if macd_line > signal_line:
                score += 0.3
                reasoning.append("MACD bullish signal")
            elif macd_line < signal_line:
                score -= 0.2
                reasoning.append("MACD bearish signal")
            
            # Check price momentum
            change_percent = market_data.get('change_percent', 0)
            if abs(change_percent) > 0.5:
                score += 0.3
                reasoning.append(f"Price momentum: {change_percent:.2f}%")
            
            return {
                'type': 'trend_following',
                'score': max(0, min(1, score)),
                'direction': 'bullish' if macd_line > signal_line else 'bearish',
                'reasoning': reasoning,
                'entry_conditions': [
                    'Price above/below moving averages',
                    'MACD confirmation',
                    'Volume support'
                ],
                'exit_conditions': [
                    'Trend reversal signals',
                    'MACD cross',
                    'Volume exhaustion'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in trend strategy analysis: {e}")
            return {'type': 'trend_following', 'score': 0, 'error': str(e)}
    
    def _analyze_mean_reversion_strategy(self, indicators: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mean reversion strategy"""
        try:
            score = 0
            reasoning = []
            
            # Check RSI for overbought/oversold
            rsi = indicators.get('rsi', 50)
            current_price = market_data.get('price', 0)
            
            if rsi > 70:
                score += 0.4
                reasoning.append(f"Overbought condition: RSI {rsi:.1f}")
            elif rsi < 30:
                score += 0.4
                reasoning.append(f"Oversold condition: RSI {rsi:.1f}")
            
            # Check support/resistance levels
            support_level = indicators.get('support_level', 0)
            resistance_level = indicators.get('resistance_level', 0)
            
            if current_price > 0:
                distance_to_support = (current_price - support_level) / current_price
                distance_to_resistance = (resistance_level - current_price) / current_price
                
                if distance_to_support < 0.02:  # Within 2% of support
                    score += 0.3
                    reasoning.append("Near support level")
                elif distance_to_resistance < 0.02:  # Within 2% of resistance
                    score += 0.3
                    reasoning.append("Near resistance level")
            
            # Check volatility for mean reversion opportunities
            volatility = indicators.get('volatility_percent', 0)
            if volatility > 1.5:  # High volatility
                score += 0.3
                reasoning.append(f"High volatility: {volatility:.2f}%")
            
            return {
                'type': 'mean_reversion',
                'score': max(0, min(1, score)),
                'direction': 'neutral',
                'reasoning': reasoning,
                'entry_conditions': [
                    'RSI overbought/oversold',
                    'Near support/resistance levels',
                    'High volatility'
                ],
                'exit_conditions': [
                    'RSI returns to neutral (40-60)',
                    'Price moves away from levels',
                    'Volatility decreases'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in mean reversion strategy analysis: {e}")
            return {'type': 'mean_reversion', 'score': 0, 'error': str(e)}
    
    def _analyze_breakout_strategy(self, indicators: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze breakout strategy"""
        try:
            score = 0
            reasoning = []
            
            current_price = market_data.get('price', 0)
            resistance_level = indicators.get('resistance_level', 0)
            support_level = indicators.get('support_level', 0)
            
            # Check for breakout above resistance
            if current_price > resistance_level * 1.01:  # 1% above resistance
                score += 0.5
                reasoning.append(f"Breakout above resistance: ₹{resistance_level:.2f}")
            
            # Check for breakdown below support
            elif current_price < support_level * 0.99:  # 1% below support
                score += 0.5
                reasoning.append(f"Breakdown below support: ₹{support_level:.2f}")
            
            # Check volume for breakout confirmation
            volume = market_data.get('volume', 0)
            if volume > 0:  # Volume data available
                score += 0.3
                reasoning.append("Volume confirmation needed")
            
            # Check volatility increase
            volatility = indicators.get('volatility_percent', 0)
            if volatility > 1.0:
                score += 0.2
                reasoning.append(f"Increased volatility: {volatility:.2f}%")
            
            return {
                'type': 'breakout',
                'score': max(0, min(1, score)),
                'direction': 'bullish' if current_price > resistance_level else 'bearish',
                'reasoning': reasoning,
                'entry_conditions': [
                    'Price breaks support/resistance',
                    'Volume confirmation',
                    'Volatility increase'
                ],
                'exit_conditions': [
                    'Price returns to range',
                    'Volume exhaustion',
                    'Target reached'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in breakout strategy analysis: {e}")
            return {'type': 'breakout', 'score': 0, 'error': str(e)}
    
    def _analyze_momentum_strategy(self, indicators: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze momentum strategy"""
        try:
            score = 0
            reasoning = []
            
            # Check price momentum
            change_percent = market_data.get('change_percent', 0)
            if abs(change_percent) > 1.0:
                score += 0.4
                reasoning.append(f"Strong price momentum: {change_percent:.2f}%")
            
            # Check RSI momentum
            rsi = indicators.get('rsi', 50)
            if 40 < rsi < 60:  # Neutral RSI with momentum
                score += 0.3
                reasoning.append(f"RSI momentum: {rsi:.1f}")
            
            # Check MACD momentum
            macd = indicators.get('macd', {})
            histogram = macd.get('histogram', 0)
            
            if abs(histogram) > 0.1:
                score += 0.3
                reasoning.append(f"MACD momentum: {histogram:.2f}")
            
            return {
                'type': 'momentum',
                'score': max(0, min(1, score)),
                'direction': 'neutral',
                'reasoning': reasoning,
                'entry_conditions': [
                    'Strong price momentum',
                    'Neutral RSI',
                    'MACD confirmation'
                ],
                'exit_conditions': [
                    'Momentum slows',
                    'RSI reaches extremes',
                    'MACD divergence'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in momentum strategy analysis: {e}")
            return {'type': 'momentum', 'score': 0, 'error': str(e)}
    
    def _get_default_strategy(self) -> Dict[str, Any]:
        """Get default strategy when no strong signals"""
        return {
            'type': 'hold',
            'score': 0.5,
            'direction': 'neutral',
            'reasoning': ['No clear trading signals detected'],
            'entry_conditions': ['Wait for clear signals'],
            'exit_conditions': ['No position to exit']
        }
    
    def get_strategy_recommendations(self, symbol: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Get specific trading recommendations based on strategy analysis"""
        try:
            best_strategy = analysis_result.get('best_strategy', {})
            strategy_type = best_strategy.get('type', 'hold')
            strategy_score = best_strategy.get('score', 0.5)
            direction = best_strategy.get('direction', 'neutral')
            
            # Convert strategy to option recommendation
            if strategy_type == 'hold' or strategy_score < 0.6:
                recommendation = 'HOLD'
                option_side = 'HOLD'
            elif direction == 'bullish':
                recommendation = 'BUY CALL'
                option_side = 'CALL'
            elif direction == 'bearish':
                recommendation = 'BUY PUT'
                option_side = 'PUT'
            else:
                recommendation = 'HOLD'
                option_side = 'HOLD'
            
            return {
                'symbol': symbol,
                'strategy_type': strategy_type,
                'recommendation': recommendation,
                'option_side': option_side,
                'confidence': strategy_score,
                'reasoning': best_strategy.get('reasoning', []),
                'entry_conditions': best_strategy.get('entry_conditions', []),
                'exit_conditions': best_strategy.get('exit_conditions', []),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating strategy recommendations: {e}")
            return {
                'symbol': symbol,
                'strategy_type': 'hold',
                'recommendation': 'HOLD',
                'option_side': 'HOLD',
                'confidence': 0.5,
                'error': str(e)
            }

# Global strategy agent instance
strategy_agent = StrategyAgent()

def analyze_trading_strategies(symbol: str, indicators: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze trading strategies for a symbol"""
    return strategy_agent.analyze_strategy_opportunities(symbol, indicators, market_data)

def get_strategy_recommendation(symbol: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """Get strategy recommendation"""
    return strategy_agent.get_strategy_recommendations(symbol, analysis_result)
