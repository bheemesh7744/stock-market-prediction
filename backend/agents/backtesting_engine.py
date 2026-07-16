"""
Backtesting Engine
==================
Historical strategy replay framework that tests trading strategies
against real past market data. Downloads data from yfinance, replays
each trading day through the strategy logic, simulates paper trades,
and calculates comprehensive performance metrics.

Supported Strategies:
  - RSI_MACD: Buy when oversold + MACD bullish crossover
  - BOLLINGER_BANDS: Buy at lower band, sell at upper band
  - MOVING_AVERAGE_CROSSOVER: Golden cross / death cross (20/50 SMA)

Metrics Calculated:
  - Total Return, Annualized Return
  - Sharpe Ratio, Max Drawdown
  - Win Rate, Profit Factor
  - Complete trade log + equity curve for charting
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional

import yfinance as yf
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Import stock configuration (lazy import to avoid circular dependency)
_STOCK_CONFIG = None

def _get_stock_config():
    """Lazy import of INDIAN_STOCKS_CONFIG to avoid circular imports."""
    global _STOCK_CONFIG
    if _STOCK_CONFIG is None:
        try:
            from market_engine import INDIAN_STOCKS_CONFIG
            _STOCK_CONFIG = INDIAN_STOCKS_CONFIG
        except ImportError:
            logger.warning("Could not import INDIAN_STOCKS_CONFIG, using fallback")
            _STOCK_CONFIG = {}
    return _STOCK_CONFIG


# ══════════════════════════════════════════════════════════════
# BACKTEST RESULT — Output of every backtest run
# ══════════════════════════════════════════════════════════════

@dataclass
class BacktestResult:
    """Complete results of a backtest run."""
    symbol: str
    strategy: str
    period: str
    start_date: str
    end_date: str
    initial_capital: float
    final_capital: float
    total_return_pct: float
    annualized_return_pct: float
    sharpe_ratio: float
    max_drawdown_pct: float
    win_rate_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    profit_factor: float
    avg_trade_return_pct: float
    avg_holding_days: float
    brokerage_paid: float
    trade_log: List[Dict[str, Any]] = field(default_factory=list)
    equity_curve: List[Dict[str, Any]] = field(default_factory=list)
    monthly_returns: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            'symbol': self.symbol,
            'strategy': self.strategy,
            'period': self.period,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'initial_capital': round(self.initial_capital, 2),
            'final_capital': round(self.final_capital, 2),
            'total_return_pct': round(self.total_return_pct, 2),
            'annualized_return_pct': round(self.annualized_return_pct, 2),
            'sharpe_ratio': round(self.sharpe_ratio, 4),
            'max_drawdown_pct': round(self.max_drawdown_pct, 2),
            'win_rate_pct': round(self.win_rate_pct, 2),
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'profit_factor': round(self.profit_factor, 2),
            'avg_trade_return_pct': round(self.avg_trade_return_pct, 2),
            'avg_holding_days': round(self.avg_holding_days, 1),
            'brokerage_paid': round(self.brokerage_paid, 2),
            'trade_log': self.trade_log,
            'equity_curve': self.equity_curve,
            'monthly_returns': self.monthly_returns,
            'net_profit': round(self.final_capital - self.initial_capital, 2),
            'roi_multiple': round(self.final_capital / self.initial_capital, 4) if self.initial_capital > 0 else 0
        }


# ══════════════════════════════════════════════════════════════
# BACKTESTING ENGINE
# ══════════════════════════════════════════════════════════════

VALID_PERIODS = {'6mo', '1y', '2y', '3y', '5y'}
VALID_STRATEGIES = {'RSI_MACD', 'BOLLINGER_BANDS', 'MOVING_AVERAGE_CROSSOVER'}


class BacktestingEngine:
    """
    Historical Backtesting Engine.
    
    Replays your trading strategy on past data and calculates how it
    would have performed with real market prices, accounting for
    brokerage fees and slippage.
    
    Usage:
        engine = BacktestingEngine()
        result = engine.run_backtest('RELIANCE', '1y', 'RSI_MACD')
        print(f"Return: {result.total_return_pct}%")
        print(f"Sharpe: {result.sharpe_ratio}")
        print(f"Max Drawdown: {result.max_drawdown_pct}%")
    """

    def __init__(
        self,
        initial_capital: float = 1000000.0,
        brokerage_pct: float = 0.0003,
        slippage_pct: float = 0.0005
    ):
        self.initial_capital = initial_capital
        self.brokerage_pct = brokerage_pct
        self.slippage_pct = slippage_pct

        logger.info(
            f"BacktestingEngine initialized: capital=₹{initial_capital:,.0f}, "
            f"brokerage={brokerage_pct*100}%, slippage={slippage_pct*100}%"
        )

    def run_backtest(
        self,
        symbol: str,
        period: str = '1y',
        strategy: str = 'RSI_MACD'
    ) -> BacktestResult:
        """
        Run a complete backtest for a given symbol, period, and strategy.
        
        Args:
            symbol: Stock symbol (e.g., 'RELIANCE', 'TCS', 'INFY')
            period: Backtest period ('6mo', '1y', '2y', '3y', '5y')
            strategy: Strategy name ('RSI_MACD', 'BOLLINGER_BANDS', 'MOVING_AVERAGE_CROSSOVER')
            
        Returns:
            BacktestResult with all metrics and trade log
        """
        symbol = symbol.upper().strip()
        strategy = strategy.upper().strip()

        if period not in VALID_PERIODS:
            raise ValueError(f"Invalid period '{period}'. Use: {', '.join(VALID_PERIODS)}")
        if strategy not in VALID_STRATEGIES:
            raise ValueError(f"Invalid strategy '{strategy}'. Use: {', '.join(VALID_STRATEGIES)}")

        logger.info(f"Starting backtest: {symbol} | {strategy} | {period}")

        # ── Step 1: Download historical data ──
        yf_symbol = self._resolve_yfinance_symbol(symbol)
        logger.info(f"Downloading data for {yf_symbol} (period={period})...")

        ticker = yf.Ticker(yf_symbol)
        df = ticker.history(period=period, interval='1d')

        if df.empty or len(df) < 60:
            raise ValueError(f"Insufficient data for {symbol}. Got {len(df)} days, need at least 60.")

        logger.info(f"Downloaded {len(df)} trading days for {symbol}")

        # ── Step 2: Calculate technical indicators ──
        df = self._prepare_dataframe(df)

        # ── Step 3: Replay strategy ──
        trade_log, equity_curve = self._replay_strategy(df, symbol, strategy)

        # ── Step 4: Calculate metrics ──
        start_date = df.index[0].strftime('%Y-%m-%d')
        end_date = df.index[-1].strftime('%Y-%m-%d')
        final_capital = equity_curve[-1]['portfolio_value'] if equity_curve else self.initial_capital

        result = self._build_result(
            symbol, strategy, period, start_date, end_date,
            final_capital, trade_log, equity_curve, df
        )

        logger.info(
            f"Backtest complete: {symbol} | Return: {result.total_return_pct:.2f}% | "
            f"Sharpe: {result.sharpe_ratio:.2f} | Drawdown: {result.max_drawdown_pct:.2f}% | "
            f"Trades: {result.total_trades}"
        )

        return result

    def _resolve_yfinance_symbol(self, symbol: str) -> str:
        """Resolve app symbol to yfinance symbol."""
        config = _get_stock_config()
        if symbol in config:
            return config[symbol]['symbol']
        # Fallback: assume NSE
        if not symbol.endswith('.NS') and not symbol.startswith('^'):
            return f"{symbol}.NS"
        return symbol

    def _prepare_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add all technical indicator columns to the dataframe."""
        df = df.copy()

        # ── RSI (14-period) ──
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # ── MACD (12, 26, 9) ──
        ema12 = df['Close'].ewm(span=12, adjust=False).mean()
        ema26 = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']

        # ── Simple Moving Averages ──
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()

        # ── Bollinger Bands (20-period, 2 std dev) ──
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)

        # Fill NaN values (pandas 2.x compatible)
        df = df.bfill()
        df = df.ffill()

        return df

    def _replay_strategy(
        self,
        df: pd.DataFrame,
        symbol: str,
        strategy: str
    ) -> tuple:
        """Replay the strategy day-by-day and simulate trades."""
        cash = self.initial_capital
        shares = 0
        total_brokerage = 0.0
        trade_log = []
        equity_curve = []
        buy_price = 0.0
        buy_date = None

        # Strategy function mapping
        strategy_fn = {
            'RSI_MACD': self._strategy_rsi_macd,
            'BOLLINGER_BANDS': self._strategy_bollinger_bands,
            'MOVING_AVERAGE_CROSSOVER': self._strategy_ma_crossover
        }.get(strategy, self._strategy_rsi_macd)

        # Start from index 50 to ensure all indicators are calculated
        start_idx = min(50, len(df) - 1)

        for i in range(start_idx, len(df)):
            close_price = float(df['Close'].iloc[i])
            date_str = df.index[i].strftime('%Y-%m-%d')
            portfolio_value = cash + (shares * close_price)

            # Get strategy signal
            signal = strategy_fn(df, i)

            if signal == 'BUY' and shares == 0 and cash > close_price:
                # Apply slippage (buy slightly higher)
                exec_price = close_price * (1 + self.slippage_pct)
                # Calculate quantity (invest ~90% of cash to keep some buffer)
                max_invest = cash * 0.90
                quantity = int(max_invest / exec_price)

                if quantity > 0:
                    trade_cost = quantity * exec_price
                    brokerage = trade_cost * self.brokerage_pct
                    cash -= (trade_cost + brokerage)
                    shares = quantity
                    total_brokerage += brokerage
                    buy_price = exec_price
                    buy_date = df.index[i]

                    trade_log.append({
                        'date': date_str,
                        'action': 'BUY',
                        'price': round(exec_price, 2),
                        'quantity': quantity,
                        'trade_value': round(trade_cost, 2),
                        'brokerage': round(brokerage, 2),
                        'pnl': 0,
                        'portfolio_value': round(cash + shares * close_price, 2)
                    })

            elif signal == 'SELL' and shares > 0:
                # Apply slippage (sell slightly lower)
                exec_price = close_price * (1 - self.slippage_pct)
                trade_value = shares * exec_price
                brokerage = trade_value * self.brokerage_pct
                pnl = (exec_price - buy_price) * shares - brokerage
                cash += (trade_value - brokerage)
                total_brokerage += brokerage

                holding_days = 0
                if buy_date is not None:
                    holding_days = (df.index[i] - buy_date).days

                trade_log.append({
                    'date': date_str,
                    'action': 'SELL',
                    'price': round(exec_price, 2),
                    'quantity': shares,
                    'trade_value': round(trade_value, 2),
                    'brokerage': round(brokerage, 2),
                    'pnl': round(pnl, 2),
                    'portfolio_value': round(cash, 2),
                    'holding_days': holding_days
                })

                shares = 0
                buy_price = 0.0
                buy_date = None

            # Record equity curve
            portfolio_value = cash + (shares * close_price)
            peak = max(e['portfolio_value'] for e in equity_curve) if equity_curve else self.initial_capital
            peak = max(peak, self.initial_capital)
            drawdown = ((peak - portfolio_value) / peak * 100) if peak > 0 else 0

            equity_curve.append({
                'date': date_str,
                'portfolio_value': round(portfolio_value, 2),
                'drawdown_pct': round(max(0, drawdown), 2)
            })

        return trade_log, equity_curve

    # ══════════════════════════════════════════════════════════════
    # TRADING STRATEGIES
    # ══════════════════════════════════════════════════════════════

    def _strategy_rsi_macd(self, df: pd.DataFrame, index: int) -> str:
        """
        RSI + MACD Strategy.
        BUY: RSI < 30 (oversold) AND MACD crosses above signal line
        SELL: RSI > 70 (overbought) AND MACD crosses below signal line
        """
        try:
            rsi = float(df['RSI'].iloc[index])
            macd = float(df['MACD'].iloc[index])
            macd_prev = float(df['MACD'].iloc[index - 1])
            signal = float(df['MACD_Signal'].iloc[index])
            signal_prev = float(df['MACD_Signal'].iloc[index - 1])

            # MACD crossover detection
            macd_crosses_above = macd > signal and macd_prev <= signal_prev
            macd_crosses_below = macd < signal and macd_prev >= signal_prev

            if rsi < 30 and macd_crosses_above:
                return 'BUY'
            elif rsi > 70 and macd_crosses_below:
                return 'SELL'
            # Additional: sell if RSI goes extremely overbought
            elif rsi > 80:
                return 'SELL'
            return 'HOLD'
        except Exception:
            return 'HOLD'

    def _strategy_bollinger_bands(self, df: pd.DataFrame, index: int) -> str:
        """
        Bollinger Bands Strategy.
        BUY: Price touches/crosses below lower band
        SELL: Price touches/crosses above upper band
        """
        try:
            close = float(df['Close'].iloc[index])
            bb_lower = float(df['BB_Lower'].iloc[index])
            bb_upper = float(df['BB_Upper'].iloc[index])

            if close <= bb_lower:
                return 'BUY'
            elif close >= bb_upper:
                return 'SELL'
            return 'HOLD'
        except Exception:
            return 'HOLD'

    def _strategy_ma_crossover(self, df: pd.DataFrame, index: int) -> str:
        """
        Moving Average Crossover Strategy.
        BUY: 20-day SMA crosses above 50-day SMA (Golden Cross)
        SELL: 20-day SMA crosses below 50-day SMA (Death Cross)
        """
        try:
            sma20 = float(df['SMA_20'].iloc[index])
            sma50 = float(df['SMA_50'].iloc[index])
            sma20_prev = float(df['SMA_20'].iloc[index - 1])
            sma50_prev = float(df['SMA_50'].iloc[index - 1])

            # Golden Cross
            if sma20 > sma50 and sma20_prev <= sma50_prev:
                return 'BUY'
            # Death Cross
            elif sma20 < sma50 and sma20_prev >= sma50_prev:
                return 'SELL'
            return 'HOLD'
        except Exception:
            return 'HOLD'

    # ══════════════════════════════════════════════════════════════
    # METRICS CALCULATION
    # ══════════════════════════════════════════════════════════════

    def _build_result(
        self,
        symbol: str,
        strategy: str,
        period: str,
        start_date: str,
        end_date: str,
        final_capital: float,
        trade_log: List[Dict],
        equity_curve: List[Dict],
        df: pd.DataFrame
    ) -> BacktestResult:
        """Build the complete BacktestResult with all metrics."""

        total_return_pct = ((final_capital - self.initial_capital) / self.initial_capital) * 100

        # Annualized return
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
            years = max(0.01, (end_dt - start_dt).days / 365.25)
            annualized = ((final_capital / self.initial_capital) ** (1 / years) - 1) * 100
        except Exception:
            annualized = total_return_pct
            years = 1

        # Trade analysis
        sell_trades = [t for t in trade_log if t['action'] == 'SELL']
        total_trades = len(sell_trades)
        winning_trades = len([t for t in sell_trades if t.get('pnl', 0) > 0])
        losing_trades = len([t for t in sell_trades if t.get('pnl', 0) <= 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        # Profit factor
        gross_profit = sum(t['pnl'] for t in sell_trades if t.get('pnl', 0) > 0)
        gross_loss = abs(sum(t['pnl'] for t in sell_trades if t.get('pnl', 0) < 0))
        profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else (float('inf') if gross_profit > 0 else 0)

        # Average trade return
        trade_returns = [t.get('pnl', 0) for t in sell_trades]
        avg_trade_return = (sum(trade_returns) / len(trade_returns)) if trade_returns else 0
        avg_trade_return_pct = (avg_trade_return / self.initial_capital * 100) if self.initial_capital > 0 else 0

        # Average holding days
        holding_days = [t.get('holding_days', 0) for t in sell_trades if 'holding_days' in t]
        avg_holding = (sum(holding_days) / len(holding_days)) if holding_days else 0

        # Max drawdown
        max_drawdown = max((e['drawdown_pct'] for e in equity_curve), default=0)

        # Sharpe ratio
        sharpe = self._calculate_sharpe(equity_curve)

        # Total brokerage
        total_brokerage = sum(t.get('brokerage', 0) for t in trade_log)

        # Monthly returns
        monthly_returns = self._calculate_monthly_returns(equity_curve)

        return BacktestResult(
            symbol=symbol,
            strategy=strategy,
            period=period,
            start_date=start_date,
            end_date=end_date,
            initial_capital=self.initial_capital,
            final_capital=final_capital,
            total_return_pct=total_return_pct,
            annualized_return_pct=annualized,
            sharpe_ratio=sharpe,
            max_drawdown_pct=max_drawdown,
            win_rate_pct=win_rate,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            profit_factor=profit_factor if profit_factor != float('inf') else 999.99,
            avg_trade_return_pct=avg_trade_return_pct,
            avg_holding_days=avg_holding,
            brokerage_paid=total_brokerage,
            trade_log=trade_log,
            equity_curve=equity_curve,
            monthly_returns=monthly_returns
        )

    def _calculate_sharpe(self, equity_curve: List[Dict], risk_free_rate: float = 0.06) -> float:
        """Calculate annualized Sharpe ratio from equity curve."""
        try:
            if len(equity_curve) < 10:
                return 0.0

            values = [e['portfolio_value'] for e in equity_curve]
            returns = []
            for i in range(1, len(values)):
                if values[i - 1] > 0:
                    returns.append((values[i] - values[i - 1]) / values[i - 1])

            if len(returns) < 2:
                return 0.0

            avg_return = sum(returns) / len(returns)
            std_return = math.sqrt(sum((r - avg_return) ** 2 for r in returns) / (len(returns) - 1))

            if std_return == 0:
                return 0.0

            # Annualize (252 trading days)
            daily_risk_free = risk_free_rate / 252
            sharpe = ((avg_return - daily_risk_free) / std_return) * math.sqrt(252)

            return sharpe
        except Exception:
            return 0.0

    def _calculate_monthly_returns(self, equity_curve: List[Dict]) -> List[Dict]:
        """Calculate monthly returns from equity curve."""
        try:
            if not equity_curve:
                return []

            monthly = {}
            for entry in equity_curve:
                month_key = entry['date'][:7]  # YYYY-MM
                monthly[month_key] = entry['portfolio_value']

            result = []
            months = sorted(monthly.keys())
            for i in range(1, len(months)):
                prev_val = monthly[months[i - 1]]
                curr_val = monthly[months[i]]
                ret_pct = ((curr_val - prev_val) / prev_val * 100) if prev_val > 0 else 0
                result.append({
                    'month': months[i],
                    'return_pct': round(ret_pct, 2),
                    'portfolio_value': round(curr_val, 2)
                })

            return result
        except Exception:
            return []

    @staticmethod
    def get_available_strategies() -> List[Dict[str, str]]:
        """Get list of available backtesting strategies."""
        return [
            {
                'name': 'RSI_MACD',
                'display_name': 'RSI + MACD Strategy',
                'description': 'Buys when RSI indicates oversold (<30) and MACD shows bullish crossover. '
                               'Sells when RSI indicates overbought (>70) and MACD shows bearish crossover.',
                'risk_level': 'Medium',
                'best_for': 'Trending markets with clear momentum shifts'
            },
            {
                'name': 'BOLLINGER_BANDS',
                'display_name': 'Bollinger Bands Strategy',
                'description': 'Buys when price touches the lower Bollinger Band (oversold). '
                               'Sells when price touches the upper Bollinger Band (overbought).',
                'risk_level': 'Low-Medium',
                'best_for': 'Range-bound / sideways markets'
            },
            {
                'name': 'MOVING_AVERAGE_CROSSOVER',
                'display_name': 'Moving Average Crossover (Golden/Death Cross)',
                'description': 'Buys on Golden Cross (20-SMA crosses above 50-SMA). '
                               'Sells on Death Cross (20-SMA crosses below 50-SMA).',
                'risk_level': 'Low',
                'best_for': 'Long-term trend following'
            }
        ]


# ══════════════════════════════════════════════════════════════
# MODULE-LEVEL SINGLETON & HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

backtesting_engine = BacktestingEngine()


def run_backtest(
    symbol: str,
    period: str = '1y',
    strategy: str = 'RSI_MACD'
) -> BacktestResult:
    """Run a backtest using the global engine."""
    return backtesting_engine.run_backtest(symbol, period, strategy)


def get_strategies() -> List[Dict[str, str]]:
    """Get available strategies."""
    return BacktestingEngine.get_available_strategies()
