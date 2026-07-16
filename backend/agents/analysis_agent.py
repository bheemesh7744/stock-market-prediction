"""
Analysis Agent - Combines all information and produces final AI analysis
"""

import logging
from typing import Dict, Any, List
from datetime import datetime
import sys
import os

logger = logging.getLogger(__name__)

# Import Deep Learning Agent
try:
    from backend.agents.deep_learning_agent import generate_deep_predictions
    DEEP_LEARNING_AVAILABLE = True
    logger.info("Deep learning agent imported successfully")
except ImportError as e:
    DEEP_LEARNING_AVAILABLE = False
    logger.warning(f"Deep learning agent not available: {e}")

class AnalysisAgent:
    """Agent for combining market, strategy, and risk analysis with RAG knowledge"""
    
    def __init__(self):
        self.analysis_cache = {}
        self.cache_timeout = 60  # Cache analysis for 60 seconds
    
    def generate_comprehensive_analysis(self, symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive AI analysis combining all agents and RAG"""
        try:
            logger.info(f"Analysis agent generating comprehensive analysis for {symbol}")
            
            # Import here to avoid circular imports
            from backend.agents.market_agent import market_agent
            from backend.agents.strategy_agent import strategy_agent
            from backend.agents.risk_agent import risk_agent
            
            # Step 1: Get market analysis
            market_analysis = market_agent.process_market_data(symbol, market_data)
            indicators = market_analysis.get('indicators', {})
            
            # Step 2: Get strategy analysis
            strategy_analysis = strategy_agent.analyze_strategy_opportunities(symbol, indicators, market_data)
            
            # Step 3: Get risk analysis
            risk_analysis = risk_agent.calculate_risk_metrics(symbol, market_data, indicators)
            
            # Step 4: Get RAG-enhanced insights
            rag_insights = self._get_rag_insights(symbol, market_data, indicators)
            
            # Step 5: Get Deep Learning predictions
            deep_learning_insights = self._get_deep_learning_insights(symbol, market_data, indicators)
            
            # Step 5b: Get News Sentiment analysis
            try:
                from market_engine import fetch_news_and_sentiment
                news_analysis = fetch_news_and_sentiment(symbol)
            except Exception as ne:
                logger.error(f"Error importing or fetching news in AnalysisAgent: {ne}")
                news_analysis = {'articles': [], 'news_sentiment_score': 0.0, 'news_sentiment_label': 'Neutral'}

            # Step 6: Generate final analysis
            final_analysis = self._generate_final_analysis(
                symbol, market_data, market_analysis, strategy_analysis, risk_analysis, rag_insights, deep_learning_insights, news_analysis
            )
            
            # Cache the analysis
            self.analysis_cache[symbol] = {
                'data': final_analysis,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Analysis agent completed comprehensive analysis for {symbol}")
            
            return final_analysis
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis for {symbol}: {e}")
            return self._get_fallback_analysis(symbol, market_data, str(e))
    
    def _get_deep_learning_insights(self, symbol: str, market_data: Dict[str, Any], indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Get Deep Learning-enhanced trading insights"""
        try:
            # Skip deep learning for fast mode - return lightweight insights
            if hasattr(self, '_fast_mode') and self._fast_mode:
                return {
                    'dl_enabled': False,
                    'insights': 'Fast mode - deep learning skipped for speed',
                    'predictions': {},
                    'success': True,
                    'fast_mode': True
                }
            
            if not DEEP_LEARNING_AVAILABLE:
                return {
                    'dl_enabled': False,
                    'insights': 'Deep learning models not available',
                    'predictions': {},
                    'success': False
                }
            
            logger.info(f"Getting deep learning insights for {symbol}")
            
            # Generate deep learning predictions
            dl_predictions = generate_deep_predictions(symbol, market_data)
            
            if 'error' in dl_predictions:
                return {
                    'dl_enabled': True,
                    'insights': 'Deep learning prediction failed',
                    'predictions': {},
                    'success': False,
                    'error': dl_predictions.get('error', 'Unknown error')
                }
            
            # Create enhanced deep learning insights
            dl_insights = {
                'dl_enabled': True,
                'insights': f"Quantitative Ensemble Prediction: {dl_predictions.get('predicted_change_percent', 0):.2f}% change expected (based on real data)",
                'predictions': dl_predictions,
                'success': True,
                'model_type': dl_predictions.get('prediction_type', 'unknown'),
                'confidence': dl_predictions.get('confidence_score', 0.5),
                'accuracy': dl_predictions.get('model_performance', {}).get('accuracy', 0.0)
            }
            
            logger.info(f"Quantitative ensemble prediction for {symbol}: {dl_predictions.get('predicted_change_percent', 0):.2f}% change expected")
            return dl_insights
            
        except Exception as e:
            logger.error(f"Error getting deep learning insights: {e}")
            return {
                'dl_enabled': False,
                'insights': f'Deep learning system error: {str(e)}',
                'predictions': {},
                'error': str(e)
            }

    def _get_rag_insights(self, symbol: str, market_data: Dict[str, Any], indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Get RAG-enhanced trading insights"""
        try:
            # Import here to avoid circular import
            try:
                from market_engine import RAG_AVAILABLE, process_trading_question_cached
            except ImportError:
                RAG_AVAILABLE = False
            
            if not RAG_AVAILABLE:
                return {
                    'rag_enabled': False,
                    'insights': 'RAG system not available',
                    'sources': [],
                    'context_used': ''
                }
            
            # Create enhanced context with all available data
            context = {
                'symbol': symbol,
                'current_price': market_data.get('price'),
                'change': market_data.get('change'),
                'change_percent': market_data.get('change_percent'),
                'volume': market_data.get('volume'),
                'market_trend': indicators.get('market_trend', 'Unknown'),
                'rsi': indicators.get('rsi', 50),
                'volatility': indicators.get('volatility_percent', 0),
                'support_level': indicators.get('support_level', 0),
                'resistance_level': indicators.get('resistance_level', 0),
                'sentiment': indicators.get('sentiment_score', 0),
                'trend_strength': indicators.get('trend_strength', 0.5),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Generate comprehensive RAG query
            question = f"""
            You are a professional Indian stock market analyst.
            
            Live Market Data:
            - Symbol: {symbol}
            - Current Price: ₹{market_data.get('price', 0)}
            - Daily Change: {market_data.get('change_percent', 0):.2f}%
            - Volume: {market_data.get('volume', 0)}
            
            Technical Indicators:
            - Market Trend: {indicators.get('market_trend', 'Unknown')}
            - RSI (14): {indicators.get('rsi', 50):.1f}
            - Volatility: {indicators.get('volatility_percent', 0):.2f}%
            - Support Level: ₹{indicators.get('support_level', 0):.2f}
            - Resistance Level: ₹{indicators.get('resistance_level', 0):.2f}
            - Market Sentiment: {indicators.get('sentiment_score', 0):.2f}
            - Trend Strength: {indicators.get('trend_strength', 0.5):.2f}
            
            Trading Knowledge (RAG retrieved):
            [Will be retrieved from documents]
            
            Generate a professional market analysis and trading suggestion.
            """
            
            # Process with cached RAG
            rag_result = process_trading_question_cached(question, context)
            
            if rag_result['success']:
                return {
                    'rag_enabled': True,
                    'insights': rag_result['answer'],
                    'sources': rag_result['sources'],
                    'context_used': rag_result['context_used'],
                    'success': True
                }
            else:
                return {
                    'rag_enabled': True,
                    'insights': 'RAG retrieval failed',
                    'sources': [],
                    'context_used': '',
                    'success': False,
                    'error': rag_result.get('error', 'Unknown error')
                }
                
        except Exception as e:
            logger.error(f"Error getting RAG insights: {e}")
            return {
                'rag_enabled': False,
                'insights': f'RAG system error: {str(e)}',
                'sources': [],
                'context_used': '',
                'error': str(e)
            }
    
    def _generate_final_analysis(self, symbol: str, market_data: Dict[str, Any], 
                               market_analysis: Dict[str, Any], strategy_analysis: Dict[str, Any], 
                               risk_analysis: Dict[str, Any], rag_insights: Dict[str, Any], 
                               deep_learning_insights: Dict[str, Any], news_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate final comprehensive analysis"""
        try:
            # Import here to avoid circular imports
            from backend.agents.strategy_agent import strategy_agent
            
            # Extract key information
            indicators = market_analysis.get('indicators', {})
            best_strategy = strategy_analysis.get('best_strategy', {})
            strategy_recommendation = strategy_agent.get_strategy_recommendations(symbol, strategy_analysis)
            risk_metrics = risk_analysis
            
            # Generate AI trading suggestion
            ai_suggestion = self._generate_ai_trading_suggestion(
                strategy_recommendation, risk_metrics, indicators, news_analysis
            )
            
            # Create comprehensive analysis
            final_analysis = {
                'symbol': symbol,
                'display_name': symbol.replace('_', ' '),
                'analysis_timestamp': datetime.now().isoformat(),
                
                # Market Data
                'market_data': market_data,
                
                # Technical Indicators
                'technical_indicators': indicators,
                
                # Strategy Analysis
                'strategy_analysis': {
                    'best_strategy': best_strategy,
                    'recommendation': strategy_recommendation,
                    'all_strategies': strategy_analysis.get('all_strategies', [])
                },
                
                # Risk Analysis
                'risk_analysis': risk_metrics,
                
                # RAG Insights
                'rag_insights': rag_insights,
                'rag_enhanced': rag_insights.get('rag_enabled', False),
                
                # Deep Learning Insights
                'deep_learning_insights': deep_learning_insights,
                'dl_enhanced': deep_learning_insights.get('dl_enabled', False),
                'dl_predictions': deep_learning_insights.get('predictions', {}),
                
                # News Sentiment analysis
                'news_analysis': news_analysis,
                
                # AI Trading Suggestion
                'ai_trading_suggestion': ai_suggestion,
                
                # Enhanced Predictions
                'predictions': self._generate_enhanced_predictions(symbol, market_data, indicators),
                
                # Market Intelligence
                'market_intelligence': {
                    'trend_strength': indicators.get('trend_strength', 0.5),
                    'sentiment_score': indicators.get('sentiment_score', 0),
                    'volatility_level': self._get_volatility_level(indicators.get('volatility_percent', 0)),
                    'support_resistance': {
                        'support': indicators.get('support_level', 0),
                        'resistance': indicators.get('resistance_level', 0),
                        'current_position': self._get_position_relative_to_levels(
                            market_data.get('price', 0),
                            indicators.get('support_level', 0),
                            indicators.get('resistance_level', 0)
                        )
                    }
                },
                
                # Confidence Score
                'confidence_score': min(
                    ai_suggestion.get('confidence', 0.5),
                    best_strategy.get('score', 0.5),
                    0.95  # Cap at 95%
                ),
                
                # Key Points Summary
                'key_points': self._extract_key_points(indicators, best_strategy, risk_metrics),
                
                # Risk Factors
                'risk_factors': risk_metrics.get('risk_factors', []),
                
                # Trading Signals
                'trading_signals': self._generate_trading_signals(indicators, best_strategy, risk_metrics)
            }
            
            # Append news summary points to key points if present
            if news_analysis and news_analysis.get('articles'):
                label = news_analysis.get('news_sentiment_label', 'Neutral')
                score = news_analysis.get('news_sentiment_score', 0.0)
                final_analysis['key_points'].append(f"News Sentiment: {label} ({score:+.2f})")
                
            return final_analysis
            
        except Exception as e:
            logger.error(f"Error generating final analysis: {e}")
            return self._get_fallback_analysis(symbol, market_data, str(e))
    
    def _generate_ai_trading_suggestion(self, strategy_recommendation: Dict[str, Any], 
                                       risk_metrics: Dict[str, Any], indicators: Dict[str, Any],
                                       news_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate AI trading suggestion"""
        try:
            base_recommendation = strategy_recommendation.get('recommendation', 'HOLD')
            base_confidence = strategy_recommendation.get('confidence', 0.5)
            risk_confidence = risk_metrics.get('confidence_score', 0.5)
            
            # Adjust recommendation based on risk
            if risk_metrics.get('risk_level') in ['Very High', 'High']:
                if base_recommendation in ['BUY CALL', 'BUY PUT']:
                    base_recommendation = 'HOLD'
                    base_confidence *= 0.7
            
            # Factor in News Sentiment
            reasoning = list(strategy_recommendation.get('reasoning', []))
            if news_analysis and news_analysis.get('articles'):
                news_score = news_analysis.get('news_sentiment_score', 0.0)
                news_label = news_analysis.get('news_sentiment_label', 'Neutral')
                
                reasoning.append(f"Market news sentiment is {news_label} (average score: {news_score:+.2f})")
                
                # If news is bearish, lower buy call confidence and boost put/hold
                if news_score < -0.1:
                    if base_recommendation == 'BUY CALL':
                        base_confidence *= (1.0 + news_score * 0.5)
                        if base_confidence < 0.5:
                            base_recommendation = 'HOLD'
                            reasoning.append("Downgraded BUY CALL recommendation to HOLD due to negative news catalyst")
                    elif base_recommendation == 'BUY PUT':
                        base_confidence = min(0.95, base_confidence * 1.25)
                        reasoning.append("Strengthened BUY PUT confidence due to bearish news flow")
                    elif base_recommendation == 'HOLD':
                        base_confidence = min(0.95, base_confidence * 1.1)
                
                # If news is bullish, boost call confidence and lower put/hold
                elif news_score > 0.1:
                    if base_recommendation == 'BUY CALL':
                        base_confidence = min(0.95, base_confidence * 1.25)
                        reasoning.append("Strengthened BUY CALL confidence due to bullish news flow")
                    elif base_recommendation == 'BUY PUT':
                        base_confidence *= (1.0 - news_score * 0.5)
                        if base_confidence < 0.5:
                            base_recommendation = 'HOLD'
                            reasoning.append("Downgraded BUY PUT recommendation to HOLD due to positive news catalyst")
                    elif base_recommendation == 'HOLD':
                        base_confidence = min(0.95, base_confidence * 1.1)

            # Final confidence (weighted average)
            final_confidence = (base_confidence * 0.6 + risk_confidence * 0.4)
            
            return {
                'suggestion': base_recommendation,
                'option_side': base_recommendation.split()[-1] if ' ' in base_recommendation else base_recommendation,
                'confidence': final_confidence,
                'reasoning': reasoning,
                'entry_conditions': strategy_recommendation.get('entry_conditions', []),
                'exit_conditions': strategy_recommendation.get('exit_conditions', []),
                'risk_adjusted': risk_metrics.get('risk_level') in ['Very High', 'High'] or (news_analysis and abs(news_analysis.get('news_sentiment_score', 0)) > 0.1),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating AI trading suggestion: {e}")
            return {
                'suggestion': 'HOLD',
                'option_side': 'HOLD',
                'confidence': 0.5,
                'error': str(e)
            }
    
    def _generate_enhanced_predictions(self, symbol: str, market_data: Dict[str, Any], indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced intraday predictions"""
        try:
            # Import the enhanced predictions function from the main app
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            from routes.api import generate_enhanced_predictions
            
            return generate_enhanced_predictions(symbol, market_data)
        except Exception as e:
            logger.error(f"Error generating enhanced predictions in analysis agent: {e}")
            return {
                'recommendation': 'HOLD',
                'option_side': 'HOLD',
                'probabilities': {'increase': 33.3, 'decrease': 33.3, 'sideways': 33.4},
                'targets': {'end_of_day_up': 0, 'end_of_day_down': 0, 'current_price': market_data.get('price', 0)},
                'confidence': 0.5
            }

    def _get_volatility_level(self, volatility_percent: float) -> str:
        """Categorize volatility level"""
        if volatility_percent > 2.5:
            return "Very High"
        elif volatility_percent > 1.5:
            return "High"
        elif volatility_percent > 0.8:
            return "Medium"
        else:
            return "Low"
    
    def _get_position_relative_to_levels(self, current_price: float, support: float, resistance: float) -> str:
        """Determine position relative to support/resistance"""
        if current_price <= 0 or support <= 0 or resistance <= 0:
            return "Unknown"
        
        # Calculate distances
        support_distance = (current_price - support) / current_price
        resistance_distance = (resistance - current_price) / current_price
        
        if support_distance < 0.02:  # Within 2% of support
            return "Near Support"
        elif resistance_distance < 0.02:  # Within 2% of resistance
            return "Near Resistance"
        elif support_distance < resistance_distance:
            return "Closer to Support"
        else:
            return "Closer to Resistance"
    
    def _extract_key_points(self, indicators: Dict[str, Any], strategy: Dict[str, Any], risk: Dict[str, Any]) -> List[str]:
        """Extract key points from analysis"""
        key_points = []
        
        # Trend information
        trend = indicators.get('market_trend', 'Unknown')
        key_points.append(f"Market Trend: {trend}")
        
        # Support/Resistance
        support = indicators.get('support_level', 0)
        resistance = indicators.get('resistance_level', 0)
        if support > 0 and resistance > 0:
            key_points.append(f"Support: ₹{support:.2f}, Resistance: ₹{resistance:.2f}")
        
        # Volatility
        volatility = indicators.get('volatility_percent', 0)
        key_points.append(f"Volatility: {volatility:.2f}% ({self._get_volatility_level(volatility)})")
        
        # Strategy
        strategy_type = strategy.get('type', 'Unknown')
        strategy_score = strategy.get('score', 0)
        key_points.append(f"Best Strategy: {strategy_type} (Score: {strategy_score:.2f})")
        
        # Risk Level
        risk_level = risk.get('risk_level', 'Unknown')
        key_points.append(f"Risk Level: {risk_level}")
        
        return key_points
    
    def _generate_trading_signals(self, indicators: Dict[str, Any], strategy: Dict[str, Any], risk: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate trading signals"""
        signals = []
        
        # RSI signals
        rsi = indicators.get('rsi', 50)
        if rsi > 70:
            signals.append({
                'type': 'RSI',
                'signal': 'Overbought',
                'strength': 'Strong',
                'action': 'Consider SELL'
            })
        elif rsi < 30:
            signals.append({
                'type': 'RSI',
                'signal': 'Oversold',
                'strength': 'Strong',
                'action': 'Consider BUY'
            })
        
        # MACD signals
        macd = indicators.get('macd', {})
        macd_line = macd.get('macd_line', 0)
        signal_line = macd.get('signal_line', 0)
        
        if macd_line > signal_line:
            signals.append({
                'type': 'MACD',
                'signal': 'Bullish',
                'strength': 'Moderate',
                'action': 'Consider BUY'
            })
        elif macd_line < signal_line:
            signals.append({
                'type': 'MACD',
                'signal': 'Bearish',
                'strength': 'Moderate',
                'action': 'Consider SELL'
            })
        
        # Trend signals
        trend_strength = indicators.get('trend_strength', 0.5)
        if trend_strength > 0.7:
            signals.append({
                'type': 'Trend',
                'signal': 'Strong Trend',
                'strength': 'Strong',
                'action': 'Follow Trend'
            })
        
        return signals
    
    def _get_fallback_analysis(self, symbol: str, market_data: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Get fallback analysis when errors occur"""
        return {
            'symbol': symbol,
            'display_name': symbol.replace('_', ' '),
            'analysis_timestamp': datetime.now().isoformat(),
            'market_data': market_data,
            'error': error,
            'ai_trading_suggestion': {
                'suggestion': 'HOLD',
                'option_side': 'HOLD',
                'confidence': 0.3,
                'reasoning': ['Analysis error occurred', 'Recommendation: Wait for better data']
            },
            'rag_enhanced': False,
            'confidence_score': 0.3
        }
    
    def get_cached_analysis(self, symbol: str) -> Dict[str, Any]:
        """Get cached analysis if available"""
        if symbol in self.analysis_cache:
            cache_entry = self.analysis_cache[symbol]
            cache_time = datetime.fromisoformat(cache_entry['timestamp'])
            current_time = datetime.now()
            
            if (current_time - cache_time).total_seconds() < self.cache_timeout:
                return cache_entry['data']
        
        return {}

# Global analysis agent instance
analysis_agent = AnalysisAgent()

def generate_ai_analysis(symbol: str, market_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive AI analysis"""
    return analysis_agent.generate_comprehensive_analysis(symbol, market_data)


