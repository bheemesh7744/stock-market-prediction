"""
Historical Data Manager - Manages large historical Indian stock market data
Handles data collection, storage, and retrieval for deep learning models
"""

import pandas as pd
import numpy as np
import yfinance as yf
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import os
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class HistoricalDataManager:
    """Manager for historical Indian stock market data"""
    
    def __init__(self, data_dir: str = "data/historical"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        self.db_path = self.data_dir / "indian_market_data.db"
        self._init_database()
        
        # Symbol mappings
        self.symbol_mappings = {
            'NIFTY_50': '^NSEI',
            'BANK_NIFTY': '^NSEBANK', 
            'SENSEX': '^BSESN',
            'NIFTY_IT': '^CNXIT',
            'NIFTY_BANK': '^NSEBANK',
            'NIFTY_AUTO': '^CNXAUTO',
            'NIFTY_PHARMA': '^CNXPHARMA',
            'NIFTY_FMCG': '^CNXFMCG',
            'NIFTY_METAL': '^CNXMETAL',
            'NIFTY_OIL_GAS': '^CNXOILGAS'
        }
        
        # Cache for frequently accessed data
        self.cache = {}
        self.cache_timeout = 3600  # 1 hour cache
        
    def _init_database(self):
        """Initialize SQLite database for historical data"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_data (
                    symbol TEXT,
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    adjusted_close REAL,
                    created_at TEXT,
                    PRIMARY KEY (symbol, date)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS technical_indicators (
                    symbol TEXT,
                    date TEXT,
                    rsi_14 REAL,
                    macd REAL,
                    macd_signal REAL,
                    bollinger_upper REAL,
                    bollinger_lower REAL,
                    sma_20 REAL,
                    sma_50 REAL,
                    ema_12 REAL,
                    ema_26 REAL,
                    created_at TEXT,
                    PRIMARY KEY (symbol, date)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS market_sentiment (
                    symbol TEXT,
                    date TEXT,
                    sentiment_score REAL,
                    news_count INTEGER,
                    volatility REAL,
                    trend_strength REAL,
                    created_at TEXT,
                    PRIMARY KEY (symbol, date)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Historical database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def collect_historical_data(self, symbol: str, years: int = 5) -> Dict[str, Any]:
        """Collect historical data for a symbol"""
        try:
            logger.info(f"Collecting {years} years of historical data for {symbol}")
            
            # Check cache first
            cache_key = f"{symbol}_{years}y"
            if cache_key in self.cache:
                cache_time = self.cache[cache_key]['timestamp']
                if (datetime.now() - cache_time).total_seconds() < self.cache_timeout:
                    logger.info(f"Using cached data for {symbol}")
                    return self.cache[cache_key]['data']
            
            # Get yfinance symbol
            yf_symbol = self.symbol_mappings.get(symbol, symbol)
            
            # Download data
            ticker = yf.Ticker(yf_symbol)
            hist_data = ticker.history(period=f"{years}y")
            
            if hist_data.empty:
                return {'error': f'No data found for {symbol}'}
            
            # Process and store data
            processed_data = self._process_historical_data(hist_data, symbol)
            
            # Store in database
            self._store_historical_data(symbol, processed_data)
            
            # Calculate technical indicators
            technical_data = self._calculate_technical_indicators(processed_data)
            self._store_technical_indicators(symbol, technical_data)
            
            # Calculate market sentiment
            sentiment_data = self._calculate_market_sentiment(processed_data)
            self._store_market_sentiment(symbol, sentiment_data)
            
            # Create summary
            summary = {
                'symbol': symbol,
                'data_points': len(processed_data),
                'date_range': {
                    'start': processed_data.index[0].strftime('%Y-%m-%d'),
                    'end': processed_data.index[-1].strftime('%Y-%m-%d')
                },
                'statistics': self._calculate_statistics(processed_data),
                'data_quality': self._assess_data_quality(processed_data),
                'collected_at': datetime.now().isoformat(),
                'years_collected': years
            }
            
            # Cache the result
            self.cache[cache_key] = {
                'data': summary,
                'timestamp': datetime.now()
            }
            
            logger.info(f"Successfully collected {len(processed_data)} data points for {symbol}")
            return summary
            
        except Exception as e:
            logger.error(f"Error collecting historical data for {symbol}: {e}")
            return {'error': str(e)}
    
    def _process_historical_data(self, hist_data: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Process raw historical data"""
        try:
            # Clean and prepare data
            processed = hist_data.copy()
            
            # Reset index to make date a column
            processed.reset_index(inplace=True)
            
            # Rename columns
            processed.rename(columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high', 
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume',
                'Adj Close': 'adjusted_close'
            }, inplace=True)
            
            # Calculate additional features
            processed['returns'] = processed['close'].pct_change()
            processed['log_returns'] = np.log(processed['close'] / processed['close'].shift(1))
            processed['volatility_20d'] = processed['close'].rolling(20).std()
            processed['range'] = processed['high'] - processed['low']
            processed['typical_price'] = (processed['high'] + processed['low'] + processed['close']) / 3
            
            # Add time-based features
            processed['day_of_week'] = pd.to_datetime(processed['date']).dt.dayofweek
            processed['month'] = pd.to_datetime(processed['date']).dt.month
            processed['quarter'] = pd.to_datetime(processed['date']).dt.quarter
            processed['year'] = pd.to_datetime(processed['date']).dt.year
            
            # Drop NaN values
            processed.dropna(inplace=True)
            
            return processed
            
        except Exception as e:
            logger.error(f"Error processing historical data: {e}")
            return pd.DataFrame()
    
    def _calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        try:
            indicators = pd.DataFrame()
            indicators['date'] = data['date']
            
            # RSI
            indicators['rsi_14'] = self._calculate_rsi(data['close'], 14)
            
            # MACD
            macd, macd_signal = self._calculate_macd(data['close'])
            indicators['macd'] = macd
            indicators['macd_signal'] = macd_signal
            
            # Bollinger Bands
            bb_upper, bb_lower = self._calculate_bollinger_bands(data['close'])
            indicators['bollinger_upper'] = bb_upper
            indicators['bollinger_lower'] = bb_lower
            
            # Moving Averages
            indicators['sma_20'] = data['close'].rolling(20).mean()
            indicators['sma_50'] = data['close'].rolling(50).mean()
            indicators['ema_12'] = data['close'].ewm(span=12).mean()
            indicators['ema_26'] = data['close'].ewm(span=26).mean()
            
            # Additional indicators
            indicators['atr'] = self._calculate_atr(data)
            indicators['williams_r'] = self._calculate_williams_r(data)
            indicators['stochastic'] = self._calculate_stochastic(data)
            
            return indicators.dropna()
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return pd.DataFrame()
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD"""
        ema_fast = prices.ewm(span=fast).mean()
        ema_slow = prices.ewm(span=slow).mean()
        macd = ema_fast - ema_slow
        macd_signal = macd.ewm(span=signal).mean()
        return macd, macd_signal
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std_dev: int = 2) -> Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        ma = prices.rolling(period).mean()
        std = prices.rolling(period).std()
        upper_band = ma + (std * std_dev)
        lower_band = ma - (std * std_dev)
        return upper_band, lower_band
    
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high_low = data['high'] - data['low']
        high_close = np.abs(data['high'] - data['close'].shift())
        low_close = np.abs(data['low'] - data['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        atr = true_range.rolling(period).mean()
        return atr
    
    def _calculate_williams_r(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Williams %R"""
        highest_high = data['high'].rolling(period).max()
        lowest_low = data['low'].rolling(period).min()
        williams_r = ((highest_high - data['close']) / (highest_high - lowest_low)) * -100
        return williams_r
    
    def _calculate_stochastic(self, data: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.Series:
        """Calculate Stochastic Oscillator"""
        lowest_low = data['low'].rolling(k_period).min()
        highest_high = data['high'].rolling(k_period).max()
        k_percent = ((data['close'] - lowest_low) / (highest_high - lowest_low)) * 100
        d_percent = k_percent.rolling(d_period).mean()
        return d_percent
    
    def _calculate_market_sentiment(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate market sentiment indicators"""
        try:
            sentiment = pd.DataFrame()
            sentiment['date'] = data['date']
            
            # Sentiment score based on price action
            price_change = data['close'].pct_change()
            sentiment['sentiment_score'] = np.tanh(price_change * 10)  # Normalize to -1 to 1
            
            # News count (simulated - in production, this would come from news API)
            sentiment['news_count'] = np.random.poisson(5, len(data))
            
            # Volatility
            sentiment['volatility'] = data['close'].rolling(20).std()
            
            # Trend strength
            sentiment['trend_strength'] = abs(data['close'].rolling(50).mean().pct_change(20))
            
            return sentiment.dropna()
            
        except Exception as e:
            logger.error(f"Error calculating market sentiment: {e}")
            return pd.DataFrame()
    
    def _store_historical_data(self, symbol: str, data: pd.DataFrame):
        """Store historical data in database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            
            # Prepare data for insertion
            data_to_insert = data[['date', 'open', 'high', 'low', 'close', 'volume', 'adjusted_close']].copy()
            data_to_insert['symbol'] = symbol
            data_to_insert['created_at'] = datetime.now().isoformat()
            
            # Insert data
            data_to_insert.to_sql('daily_data', conn, if_exists='replace', index=False)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored {len(data)} historical data points for {symbol}")
            
        except Exception as e:
            logger.error(f"Error storing historical data: {e}")
    
    def _store_technical_indicators(self, symbol: str, indicators: pd.DataFrame):
        """Store technical indicators in database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            
            # Prepare data
            indicators_to_store = indicators.copy()
            indicators_to_store['symbol'] = symbol
            indicators_to_store['created_at'] = datetime.now().isoformat()
            
            # Store indicators
            indicators_to_store.to_sql('technical_indicators', conn, if_exists='replace', index=False)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored technical indicators for {symbol}")
            
        except Exception as e:
            logger.error(f"Error storing technical indicators: {e}")
    
    def _store_market_sentiment(self, symbol: str, sentiment: pd.DataFrame):
        """Store market sentiment in database"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            
            # Prepare data
            sentiment_to_store = sentiment.copy()
            sentiment_to_store['symbol'] = symbol
            sentiment_to_store['created_at'] = datetime.now().isoformat()
            
            # Store sentiment
            sentiment_to_store.to_sql('market_sentiment', conn, if_exists='replace', index=False)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored market sentiment for {symbol}")
            
        except Exception as e:
            logger.error(f"Error storing market sentiment: {e}")
    
    def _calculate_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic statistics for the data"""
        try:
            returns = data['returns'].dropna()
            
            stats = {
                'total_return': ((data['close'].iloc[-1] / data['close'].iloc[0]) - 1) * 100,
                'annualized_return': (data['close'].iloc[-1] / data['close'].iloc[0]) ** (252 / len(data)) - 1,
                'volatility': returns.std() * np.sqrt(252),
                'max_drawdown': self._calculate_max_drawdown(data['close']),
                'sharpe_ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0,
                'avg_daily_return': returns.mean(),
                'best_day': returns.max(),
                'worst_day': returns.min(),
                'positive_days': (returns > 0).sum(),
                'negative_days': (returns < 0).sum(),
                'avg_volume': data['volume'].mean(),
                'max_price': data['high'].max(),
                'min_price': data['low'].min()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}
    
    def _calculate_max_drawdown(self, prices: pd.Series) -> float:
        """Calculate maximum drawdown"""
        try:
            cumulative = (1 + prices.pct_change()).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            return drawdown.min()
        except:
            return 0
    
    def _assess_data_quality(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Assess the quality of the data"""
        try:
            quality = {
                'missing_values': data.isnull().sum().to_dict(),
                'duplicate_dates': data['date'].duplicated().sum(),
                'zero_volume_days': (data['volume'] == 0).sum(),
                'price_anomalies': self._detect_price_anomalies(data),
                'completeness': (1 - data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100,
                'data_frequency': 'Daily',
                'total_trading_days': len(data)
            }
            
            return quality
            
        except Exception as e:
            logger.error(f"Error assessing data quality: {e}")
            return {}
    
    def _detect_price_anomalies(self, data: pd.DataFrame) -> int:
        """Detect price anomalies"""
        try:
            price_changes = data['close'].pct_change().abs()
            threshold = price_changes.quantile(0.99)  # 99th percentile
            anomalies = (price_changes > threshold).sum()
            return anomalies
        except:
            return 0
    
    def get_training_data(self, symbol: str, lookback_days: int = 252) -> Dict[str, Any]:
        """Get training data for deep learning models"""
        try:
            conn = sqlite3.connect(str(self.db_path))
            
            # Get daily data
            daily_query = f"""
                SELECT * FROM daily_data 
                WHERE symbol = '{symbol}' 
                ORDER BY date DESC 
                LIMIT {lookback_days}
            """
            daily_data = pd.read_sql_query(daily_query, conn)
            
            # Get technical indicators
            indicators_query = f"""
                SELECT * FROM technical_indicators 
                WHERE symbol = '{symbol}' 
                ORDER BY date DESC 
                LIMIT {lookback_days}
            """
            indicators_data = pd.read_sql_query(indicators_query, conn)
            
            # Get market sentiment
            sentiment_query = f"""
                SELECT * FROM market_sentiment 
                WHERE symbol = '{symbol}' 
                ORDER BY date DESC 
                LIMIT {lookback_days}
            """
            sentiment_data = pd.read_sql_query(sentiment_query, conn)
            
            conn.close()
            
            # Combine data
            if not daily_data.empty:
                training_data = {
                    'daily_data': daily_data,
                    'technical_indicators': indicators_data,
                    'market_sentiment': sentiment_data,
                    'data_points': len(daily_data),
                    'features': self._prepare_features(daily_data, indicators_data, sentiment_data),
                    'symbol': symbol,
                    'extracted_at': datetime.now().isoformat()
                }
                
                return training_data
            else:
                return {'error': f'No training data found for {symbol}'}
                
        except Exception as e:
            logger.error(f"Error getting training data: {e}")
            return {'error': str(e)}
    
    def _prepare_features(self, daily_data: pd.DataFrame, indicators: pd.DataFrame, sentiment: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for deep learning"""
        try:
            # Merge all data
            features = daily_data.copy()
            
            if not indicators.empty:
                indicators = indicators.drop(columns=['symbol', 'created_at'], errors='ignore')
                features = pd.merge(features, indicators, on='date', how='left')
            
            if not sentiment.empty:
                sentiment = sentiment.drop(columns=['symbol', 'created_at'], errors='ignore')
                features = pd.merge(features, sentiment, on='date', how='left')
            
            # Sort by date
            features = features.sort_values('date')
            
            # Fill missing values
            features = features.fillna(method='ffill').fillna(method='bfill')
            
            return features
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return pd.DataFrame()
    
    def collect_all_symbols_data(self, years: int = 5) -> Dict[str, Any]:
        """Collect data for all major Indian indices"""
        try:
            logger.info(f"Collecting {years} years of data for all Indian indices")
            
            results = {}
            total_data_points = 0
            
            for symbol in self.symbol_mappings.keys():
                try:
                    result = self.collect_historical_data(symbol, years)
                    if 'error' not in result:
                        results[symbol] = result
                        total_data_points += result['data_points']
                        logger.info(f"Successfully collected data for {symbol}: {result['data_points']} points")
                    else:
                        logger.warning(f"Failed to collect data for {symbol}: {result['error']}")
                        
                except Exception as e:
                    logger.error(f"Error collecting data for {symbol}: {e}")
            
            summary = {
                'symbols_collected': list(results.keys()),
                'total_symbols': len(results),
                'total_data_points': total_data_points,
                'collection_summary': results,
                'collected_at': datetime.now().isoformat(),
                'years_collected': years,
                'database_path': str(self.db_path)
            }
            
            logger.info(f"Data collection completed: {len(results)} symbols, {total_data_points} total data points")
            return summary
            
        except Exception as e:
            logger.error(f"Error in bulk data collection: {e}")
            return {'error': str(e)}

# Global instance
historical_data_manager = HistoricalDataManager()

def collect_historical_data(symbol: str, years: int = 5) -> Dict[str, Any]:
    """Collect historical data for a symbol"""
    return historical_data_manager.collect_historical_data(symbol, years)

def get_training_data(symbol: str, lookback_days: int = 252) -> Dict[str, Any]:
    """Get training data for deep learning"""
    return historical_data_manager.get_training_data(symbol, lookback_days)
