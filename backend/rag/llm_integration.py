"""
LLM Integration Module for RAG System
Handles communication with language models for generating responses
"""

import os
import json
import logging
from typing import Dict, Any, Optional
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMIntegration:
    """Handles LLM communication for generating trading responses"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize LLM integration
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
            model: LLM model to use
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
        # Fallback to mock responses if no API key
        self.use_mock = not self.api_key
        
        if self.use_mock:
            logger.warning("No OpenAI API key found. Using mock responses.")
        else:
            logger.info("LLM integration initialized with OpenAI API")
    
    def generate_response(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Generate response from LLM
        
        Args:
            prompt: The RAG-enhanced prompt
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary containing response and metadata
        """
        if self.use_mock:
            return self._generate_mock_response(prompt)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional trading assistant with expertise in technical analysis, risk management, and market psychology. Provide accurate, helpful, and responsible trading advice."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result['choices'][0]['message']['content']
                
                return {
                    'success': True,
                    'response': message,
                    'model': self.model,
                    'tokens_used': result['usage']['total_tokens'] if 'usage' in result else None,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f"API Error: {response.status_code}",
                    'fallback_response': self._generate_mock_response(prompt)['response']
                }
                
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_response': self._generate_mock_response(prompt)['response']
            }
    
    def _generate_mock_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate mock response when API is not available
        
        Args:
            prompt: The user prompt
            
        Returns:
            Dictionary containing mock response
        """
        # Extract key topics from prompt for better mock responses
        prompt_lower = prompt.lower()
        
        if 'risk management' in prompt_lower or 'stop loss' in prompt_lower:
            response = """Based on the trading documents, here are key risk management strategies:

🛡️ **Position Sizing**: Never risk more than 1-2% of your total trading capital on a single trade. This ensures you can survive multiple losing trades.

📊 **Stop Loss Orders**: Always use stop losses to limit potential losses. Place them below recent swing lows for long positions and above recent swing highs for short positions.

⚖️ **Risk-Reward Ratio**: Aim for minimum 1:2 risk-to-reward ratio. This means your potential profit should be at least twice your potential loss.

📈 **Portfolio Diversification**: Don't concentrate all capital in one sector. Trade multiple uncorrelated instruments to spread risk.

🔄 **Maximum Drawdown Control**: Set maximum acceptable drawdown (typically 20% of account) and take breaks when reached.

Remember: Professional traders focus on preserving capital first, then generating consistent returns."""
            
        elif 'rsi' in prompt_lower or 'technical' in prompt_lower or 'indicator' in prompt_lower:
            response = """Based on technical analysis documentation, here's how to use indicators effectively:

📊 **RSI (Relative Strength Index)**:
- Range: 0-100
- Overbought: RSI > 70 (consider selling/shorting)
- Oversold: RSI < 30 (consider buying/covering)
- Best for ranging markets, less reliable in strong trends
- Look for divergences between price and RSI for reversal signals

📈 **Moving Averages**:
- Use 20-day EMA for short-term trend
- Use 50-day SMA for medium-term trend  
- Use 200-day SMA for long-term trend
- Golden cross (50 above 200) = bullish signal
- Death cross (50 below 200) = bearish signal

🔄 **MACD**:
- Signal line crossovers indicate momentum changes
- Histogram shows momentum strength
- Combine with trend analysis for better signals

💡 **Pro Tips**:
- Use multiple indicators for confirmation
- Adjust parameters for your timeframe
- No indicator is 100% accurate - always use risk management"""
            
        elif 'trading strategy' in prompt_lower or 'day trading' in prompt_lower or 'swing trading' in prompt_lower:
            response = """Based on comprehensive trading strategy documentation:

🎯 **Day Trading Strategies**:
- **Scalping**: Small profits from many trades (1-5 min timeframe)
- **Momentum Trading**: Capture strong price moves (5-15 min timeframe)
- Requires high volume, tight spreads, and strict discipline

📊 **Swing Trading Strategies**:
- **Trend Following**: Use moving averages, trade pullbacks (4H-daily timeframe)
- **Mean Reversion**: Profit from price returning to average (daily timeframe)
- Risk-reward ratio of 1:3 or better recommended

🔄 **Position Trading**:
- **Breakout Trading**: Capture major price moves (daily-weekly timeframe)
- **Value Investing**: Long-term based on fundamentals (monthly timeframe)

⚡ **Key Success Factors**:
1. **Strategy Selection**: Choose based on your personality and time availability
2. **Backtesting**: Test strategies historically before live trading
3. **Risk Management**: Never risk more than 1-2% per trade
4. **Psychology**: Maintain emotional discipline and stick to your plan

Remember: No strategy works all the time. The key is consistency and proper risk management."""
            
        elif 'psychology' in prompt_lower or 'fear' in prompt_lower or 'greed' in prompt_lower:
            response = """Based on market psychology research:

🧠 **Common Psychological Biases**:
- **Confirmation Bias**: Seeking info that confirms existing beliefs
- **Loss Aversion**: Pain of losses is 2x stronger than pleasure of gains
- **Overconfidence**: Overestimating your abilities
- **Herd Mentality**: Following the crowd without analysis

🎭 **Fear and Greed Cycle**:
- **Fear Phase**: Panic selling, prices below fundamentals (buying opportunity)
- **Greed Phase**: Chasing prices irrationally, excessive optimism (warning sign)
- **Neutral Phase**: Balanced sentiment, rational decision-making

🛡️ **Psychological Risk Management**:
1. **Self-Awareness**: Recognize emotional states before trading
2. **Routine**: Use pre-trade checklists and consistent processes
3. **Breaks**: Take breaks during emotional periods or after losses
4. **Journaling**: Track decisions and emotional triggers

💪 **Building Resilience**:
- Accept losses as part of trading
- Focus on process, not individual outcomes
- Practice mindfulness and stress management
- Maintain work-life balance

Remember: The most successful traders aren't those who feel no fear, but those who act despite their fear using well-defined plans."""
            
        else:
            response = """Based on my analysis of trading strategy documents, I can help you with:

📚 **Key Trading Areas**:
- **Risk Management**: Position sizing, stop losses, portfolio diversification
- **Technical Analysis**: RSI, MACD, Moving Averages, Bollinger Bands
- **Trading Strategies**: Day trading, swing trading, position trading
- **Market Psychology**: Behavioral finance, emotional discipline

🎯 **For Specific Help**, ask me about:
- "What are the best risk management strategies?"
- "How do I use RSI indicator for trading?"
- "What is momentum trading strategy?"
- "How should I handle fear and greed in trading?"

⚡ **Quick Tips**:
1. Always use stop losses (1-2% risk per trade maximum)
2. Aim for 1:2 or better risk-reward ratio
3. Trade with the dominant trend
4. Keep a trading journal
5. Never trade emotionally

📖 **My Knowledge Base**: I have access to comprehensive trading documents covering risk management, technical indicators, trading strategies, and market psychology.

What specific aspect of trading would you like to explore in detail?"""
        
        return {
            'success': True,
            'response': response,
            'model': 'mock',
            'tokens_used': None,
            'timestamp': datetime.now().isoformat(),
            'note': 'This is a mock response. Configure OpenAI API key for real responses.'
        }

# Global LLM instance
llm_instance = None

def get_llm_instance() -> LLMIntegration:
    """Get or create the global LLM instance"""
    global llm_instance
    if llm_instance is None:
        llm_instance = LLMIntegration()
    return llm_instance
