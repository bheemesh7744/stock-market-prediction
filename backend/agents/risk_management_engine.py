"""
Risk Management Engine
=======================
Production-grade risk management module that enforces strict,
non-AI safety checks before any trade is executed.

Checks:
  1. Balance/Margin Check — Is there enough cash?
  2. Position Sizing — Max 2% of portfolio per trade
  3. Daily Loss Limit — 5% daily loss circuit breaker
  4. Max Drawdown Kill Switch — 10% total drawdown halts everything
  5. Max Open Positions — Limit concurrent stock positions
  6. Consecutive Loss Guard — Cooldown after 3 consecutive losses
  7. Quantity Adjustment — Auto-reduce quantity to comply with limits

Every trade MUST pass through validate_trade() before execution.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════════
# RISK DECISION — Output of every validation
# ══════════════════════════════════════════════════════════════

@dataclass
class RiskDecision:
    """Result of a trade risk validation."""
    approved: bool
    reason: str
    adjusted_quantity: int
    risk_score: float              # 0.0 (safe) to 1.0 (maximum risk)
    checks_passed: List[str] = field(default_factory=list)
    checks_failed: List[str] = field(default_factory=list)
    brokerage_cost: float = 0.0
    total_trade_cost: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            'approved': self.approved,
            'reason': self.reason,
            'adjusted_quantity': self.adjusted_quantity,
            'risk_score': round(self.risk_score, 4),
            'checks_passed': self.checks_passed,
            'checks_failed': self.checks_failed,
            'brokerage_cost': round(self.brokerage_cost, 2),
            'total_trade_cost': round(self.total_trade_cost, 2),
            'total_checks': len(self.checks_passed) + len(self.checks_failed),
            'pass_rate': round(len(self.checks_passed) / max(1, len(self.checks_passed) + len(self.checks_failed)) * 100, 1)
        }


# ══════════════════════════════════════════════════════════════
# RISK MANAGEMENT ENGINE
# ══════════════════════════════════════════════════════════════

class RiskManagementEngine:
    """
    Production-grade Risk Management Engine.
    
    Enforces strict financial safety checks independent of AI decisions.
    Every proposed trade must pass through validate_trade() before execution.
    
    Usage:
        engine = RiskManagementEngine()
        decision = engine.validate_trade(
            user_id=1, symbol='RELIANCE', quantity=10, price=2850.0,
            transaction_type='BUY', portfolio_value=1000000.0,
            cash_available=500000.0, current_holdings={'TCS': 5, 'INFY': 10},
            todays_pnl=-20000.0, consecutive_losses=2
        )
        if decision.approved:
            execute_trade(...)
        else:
            print(f"REJECTED: {decision.reason}")
    """

    def __init__(
        self,
        max_position_pct: float = 0.02,
        daily_loss_limit_pct: float = 0.05,
        max_drawdown_pct: float = 0.10,
        max_open_positions: int = 5,
        max_consecutive_losses: int = 3,
        cooldown_minutes: int = 30,
        brokerage_fee_pct: float = 0.0003
    ):
        self.max_position_pct = max_position_pct
        self.daily_loss_limit_pct = daily_loss_limit_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.max_open_positions = max_open_positions
        self.max_consecutive_losses = max_consecutive_losses
        self.cooldown_minutes = cooldown_minutes
        self.brokerage_fee_pct = brokerage_fee_pct

        # Internal state
        self._risk_events: List[Dict[str, Any]] = []
        self._cooldown_until: Optional[datetime] = None
        self._initial_portfolio_values: Dict[int, float] = {}  # user_id -> initial value

        logger.info(
            f"RiskManagementEngine initialized: "
            f"max_position={max_position_pct*100}%, "
            f"daily_loss_limit={daily_loss_limit_pct*100}%, "
            f"max_drawdown={max_drawdown_pct*100}%, "
            f"max_positions={max_open_positions}, "
            f"max_consecutive_losses={max_consecutive_losses}"
        )

    def validate_trade(
        self,
        user_id: int,
        symbol: str,
        quantity: int,
        price: float,
        transaction_type: str,
        portfolio_value: float,
        cash_available: float,
        current_holdings: Dict[str, int],
        todays_pnl: float = 0.0,
        consecutive_losses: int = 0
    ) -> RiskDecision:
        """
        Validate a proposed trade against ALL risk management rules.
        
        Args:
            user_id: User performing the trade
            symbol: Stock symbol (e.g., 'RELIANCE')
            quantity: Number of shares to trade
            price: Price per share
            transaction_type: 'BUY' or 'SELL'
            portfolio_value: Total current portfolio value (cash + holdings)
            cash_available: Available cash balance
            current_holdings: Dict of {symbol: quantity} for open positions
            todays_pnl: Today's realized + unrealized P&L
            consecutive_losses: Number of consecutive losing trades
            
        Returns:
            RiskDecision with approval status and detailed results
        """
        checks_passed = []
        checks_failed = []
        adjusted_quantity = quantity
        risk_score = 0.0
        trade_cost = quantity * price
        brokerage = trade_cost * self.brokerage_fee_pct

        transaction_type = transaction_type.upper().strip()

        # Store initial portfolio value for drawdown calculation
        if user_id not in self._initial_portfolio_values:
            self._initial_portfolio_values[user_id] = portfolio_value

        # ── CHECK 1: Balance Check ──
        if transaction_type == 'BUY':
            total_cost = trade_cost + brokerage
            if cash_available >= total_cost:
                checks_passed.append(f"Balance Check: ₹{cash_available:,.2f} available >= ₹{total_cost:,.2f} required")
            else:
                checks_failed.append(f"Balance Check FAILED: ₹{cash_available:,.2f} available < ₹{total_cost:,.2f} required")
                risk_score += 0.3
        else:
            # For SELL, check if user owns the shares
            owned = current_holdings.get(symbol, 0)
            if owned >= quantity:
                checks_passed.append(f"Holdings Check: Owns {owned} shares >= {quantity} to sell")
            else:
                checks_failed.append(f"Holdings Check FAILED: Owns {owned} shares < {quantity} to sell")
                risk_score += 0.3

        # ── CHECK 2: Position Sizing ──
        max_trade_value = portfolio_value * self.max_position_pct
        if trade_cost <= max_trade_value:
            checks_passed.append(f"Position Sizing: ₹{trade_cost:,.2f} <= {self.max_position_pct*100}% limit (₹{max_trade_value:,.2f})")
        else:
            # Auto-adjust quantity down
            adjusted_quantity = max(1, int(max_trade_value / price))
            adjusted_cost = adjusted_quantity * price
            checks_failed.append(
                f"Position Sizing ADJUSTED: ₹{trade_cost:,.2f} exceeded {self.max_position_pct*100}% limit "
                f"(₹{max_trade_value:,.2f}). Reduced quantity from {quantity} to {adjusted_quantity}"
            )
            trade_cost = adjusted_cost
            brokerage = trade_cost * self.brokerage_fee_pct
            risk_score += 0.15

        # ── CHECK 3: Daily Loss Limit (Circuit Breaker) ──
        daily_loss_threshold = portfolio_value * self.daily_loss_limit_pct
        if todays_pnl >= 0 or abs(todays_pnl) < daily_loss_threshold:
            checks_passed.append(
                f"Daily Loss Limit: Today's P&L ₹{todays_pnl:,.2f} within "
                f"{self.daily_loss_limit_pct*100}% limit (₹{daily_loss_threshold:,.2f})"
            )
        else:
            if transaction_type == 'BUY':
                checks_failed.append(
                    f"CIRCUIT BREAKER: Daily loss ₹{abs(todays_pnl):,.2f} exceeds "
                    f"{self.daily_loss_limit_pct*100}% limit (₹{daily_loss_threshold:,.2f}). "
                    f"No new BUY orders allowed today."
                )
                risk_score += 0.25
            else:
                checks_passed.append("Daily Loss Limit: SELL orders allowed even during circuit breaker")

        # ── CHECK 4: Max Drawdown Kill Switch ──
        initial_value = self._initial_portfolio_values.get(user_id, portfolio_value)
        current_drawdown_pct = (initial_value - portfolio_value) / initial_value if initial_value > 0 else 0
        if current_drawdown_pct <= self.max_drawdown_pct:
            checks_passed.append(
                f"Drawdown Check: {current_drawdown_pct*100:.2f}% drawdown <= "
                f"{self.max_drawdown_pct*100}% kill switch threshold"
            )
        else:
            checks_failed.append(
                f"KILL SWITCH ACTIVATED: Portfolio drawdown {current_drawdown_pct*100:.2f}% "
                f"exceeds {self.max_drawdown_pct*100}% maximum. ALL trading halted."
            )
            risk_score += 0.3

        # ── CHECK 5: Max Open Positions ──
        if transaction_type == 'BUY':
            current_position_count = len([s for s, q in current_holdings.items() if q > 0])
            is_new_position = symbol not in current_holdings or current_holdings.get(symbol, 0) == 0
            if not is_new_position or current_position_count < self.max_open_positions:
                checks_passed.append(
                    f"Position Limit: {current_position_count}/{self.max_open_positions} positions used"
                )
            else:
                checks_failed.append(
                    f"Position Limit EXCEEDED: Already holding {current_position_count} positions "
                    f"(max {self.max_open_positions}). Close a position before opening a new one."
                )
                risk_score += 0.1
        else:
            checks_passed.append("Position Limit: N/A for SELL orders")

        # ── CHECK 6: Consecutive Loss Guard ──
        if transaction_type == 'BUY':
            if consecutive_losses < self.max_consecutive_losses:
                checks_passed.append(
                    f"Consecutive Loss Guard: {consecutive_losses}/{self.max_consecutive_losses} losses"
                )
            else:
                # Check if cooldown has expired
                now = datetime.now()
                if self._cooldown_until and now < self._cooldown_until:
                    remaining = (self._cooldown_until - now).seconds // 60
                    checks_failed.append(
                        f"COOLDOWN ACTIVE: {consecutive_losses} consecutive losses reached. "
                        f"Trading paused for {remaining} more minutes."
                    )
                    risk_score += 0.15
                else:
                    # Start cooldown
                    self._cooldown_until = now + timedelta(minutes=self.cooldown_minutes)
                    checks_failed.append(
                        f"COOLDOWN TRIGGERED: {consecutive_losses} consecutive losses. "
                        f"BUY orders paused for {self.cooldown_minutes} minutes."
                    )
                    risk_score += 0.15
        else:
            checks_passed.append("Consecutive Loss Guard: N/A for SELL orders")

        # ── FINAL DECISION ──
        risk_score = min(1.0, risk_score)
        approved = len(checks_failed) == 0

        if approved:
            reason = f"Trade APPROVED: {transaction_type} {adjusted_quantity} {symbol} @ ₹{price:,.2f}"
        else:
            primary_failure = checks_failed[0].split(':')[0] if checks_failed else 'Unknown'
            reason = f"Trade REJECTED ({primary_failure}): {checks_failed[0]}" if checks_failed else "Trade REJECTED"

        decision = RiskDecision(
            approved=approved,
            reason=reason,
            adjusted_quantity=adjusted_quantity,
            risk_score=risk_score,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            brokerage_cost=round(brokerage, 2),
            total_trade_cost=round(trade_cost + brokerage, 2)
        )

        # Log the risk event
        self.log_risk_event(
            'TRADE_VALIDATION',
            {
                'user_id': user_id,
                'symbol': symbol,
                'quantity': quantity,
                'adjusted_quantity': adjusted_quantity,
                'price': price,
                'transaction_type': transaction_type,
                'approved': approved,
                'risk_score': risk_score,
                'checks_passed': len(checks_passed),
                'checks_failed': len(checks_failed),
                'reason': reason
            }
        )

        logger.info(f"Risk validation for {transaction_type} {quantity} {symbol}: {'APPROVED' if approved else 'REJECTED'} (score: {risk_score:.2f})")

        return decision

    def calculate_position_size(
        self,
        portfolio_value: float,
        price: float,
        risk_per_trade_pct: Optional[float] = None
    ) -> int:
        """
        Calculate the maximum safe position size for a trade.
        
        Args:
            portfolio_value: Total portfolio value
            price: Price per share
            risk_per_trade_pct: Override for max position percentage
            
        Returns:
            Maximum number of shares to buy
        """
        pct = risk_per_trade_pct or self.max_position_pct
        max_value = portfolio_value * pct
        max_quantity = int(max_value / price) if price > 0 else 0
        return max(0, max_quantity)



    def get_risk_dashboard(
        self,
        user_id: int,
        portfolio_value: float,
        cash: float,
        holdings_count: int,
        todays_pnl: float,
        consecutive_losses: int
    ) -> Dict[str, Any]:
        """
        Get a comprehensive risk status dashboard.
        
        Returns a JSON-friendly dict showing all risk metrics and limits.
        """
        initial_value = self._initial_portfolio_values.get(user_id, portfolio_value)
        drawdown_pct = ((initial_value - portfolio_value) / initial_value * 100) if initial_value > 0 else 0
        daily_loss_limit = portfolio_value * self.daily_loss_limit_pct
        invested_value = portfolio_value - cash

        # Circuit breaker check
        circuit_breaker_active = abs(todays_pnl) > daily_loss_limit and todays_pnl < 0

        # Kill switch check
        kill_switch_active = drawdown_pct > (self.max_drawdown_pct * 100)

        # Cooldown check
        cooldown_active = False
        if self._cooldown_until:
            cooldown_active = datetime.now() < self._cooldown_until

        # Determine risk level
        risk_score = 0.0
        if drawdown_pct > self.max_drawdown_pct * 100 * 0.8:
            risk_score += 0.4
        elif drawdown_pct > self.max_drawdown_pct * 100 * 0.5:
            risk_score += 0.2

        if circuit_breaker_active:
            risk_score += 0.3
        if consecutive_losses >= self.max_consecutive_losses:
            risk_score += 0.2
        if holdings_count >= self.max_open_positions:
            risk_score += 0.1

        risk_score = min(1.0, risk_score)

        if risk_score >= 0.7:
            risk_level = 'CRITICAL'
        elif risk_score >= 0.5:
            risk_level = 'HIGH'
        elif risk_score >= 0.25:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'

        return {
            'user_id': user_id,
            'portfolio_value': round(portfolio_value, 2),
            'cash_available': round(cash, 2),
            'invested_value': round(invested_value, 2),
            'initial_portfolio_value': round(initial_value, 2),

            'daily_pnl': round(todays_pnl, 2),
            'daily_pnl_percent': round((todays_pnl / portfolio_value * 100) if portfolio_value > 0 else 0, 2),
            'daily_loss_limit': round(daily_loss_limit, 2),
            'daily_loss_limit_pct': self.daily_loss_limit_pct * 100,

            'drawdown_percent': round(max(0, drawdown_pct), 2),
            'max_allowed_drawdown_pct': self.max_drawdown_pct * 100,

            'positions_used': holdings_count,
            'max_positions': self.max_open_positions,

            'consecutive_losses': consecutive_losses,
            'max_consecutive_losses': self.max_consecutive_losses,

            'max_position_size_pct': self.max_position_pct * 100,
            'brokerage_fee_pct': self.brokerage_fee_pct * 100,

            'circuit_breaker_active': circuit_breaker_active,
            'kill_switch_active': kill_switch_active,
            'cooldown_active': cooldown_active,
            'cooldown_until': self._cooldown_until.isoformat() if self._cooldown_until else None,

            'risk_level': risk_level,
            'risk_score': round(risk_score, 4),

            'recent_risk_events': self._risk_events[-10:],
            'total_risk_events': len(self._risk_events),

            'timestamp': datetime.now().isoformat(),
            'engine_config': {
                'max_position_pct': self.max_position_pct,
                'daily_loss_limit_pct': self.daily_loss_limit_pct,
                'max_drawdown_pct': self.max_drawdown_pct,
                'max_open_positions': self.max_open_positions,
                'max_consecutive_losses': self.max_consecutive_losses,
                'cooldown_minutes': self.cooldown_minutes,
                'brokerage_fee_pct': self.brokerage_fee_pct
            }
        }

    def log_risk_event(self, event_type: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Log a risk event for audit trail."""
        event = {
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self._risk_events.append(event)

        # Keep only last 1000 events in memory
        if len(self._risk_events) > 1000:
            self._risk_events = self._risk_events[-1000:]

        logger.info(f"Risk event logged: {event_type}")
        return event




# ══════════════════════════════════════════════════════════════
# MODULE-LEVEL SINGLETON & HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

risk_engine = RiskManagementEngine()


def validate_trade(
    user_id: int,
    symbol: str,
    quantity: int,
    price: float,
    transaction_type: str,
    portfolio_value: float,
    cash_available: float,
    current_holdings: Dict[str, int],
    todays_pnl: float = 0.0,
    consecutive_losses: int = 0
) -> RiskDecision:
    """Validate a trade through the global risk engine."""
    return risk_engine.validate_trade(
        user_id, symbol, quantity, price, transaction_type,
        portfolio_value, cash_available, current_holdings,
        todays_pnl, consecutive_losses
    )


def get_risk_dashboard(
    user_id: int,
    portfolio_value: float,
    cash: float,
    holdings_count: int,
    todays_pnl: float = 0.0,
    consecutive_losses: int = 0
) -> Dict[str, Any]:
    """Get the risk dashboard from the global risk engine."""
    return risk_engine.get_risk_dashboard(
        user_id, portfolio_value, cash, holdings_count,
        todays_pnl, consecutive_losses
    )


def calculate_position_size(portfolio_value: float, price: float) -> int:
    """Calculate max safe position size using the global risk engine."""
    return risk_engine.calculate_position_size(portfolio_value, price)
