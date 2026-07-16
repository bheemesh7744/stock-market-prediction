"""
FULL INTEGRATION TEST
=====================
Tests all 3 new modules + existing app for proper integration.
Run: python test_full_integration.py
"""
import sys
import os
import time
import traceback

sys.path.insert(0, '.')
sys.stdout.reconfigure(encoding='utf-8')

PASS = 0
FAIL = 0
WARN = 0

def test(name, func):
    global PASS, FAIL
    try:
        result = func()
        if result:
            print(f"  [PASS] {name}")
            PASS += 1
        else:
            print(f"  [FAIL] {name} — returned False")
            FAIL += 1
    except Exception as e:
        print(f"  [FAIL] {name} — {e}")
        traceback.print_exc()
        FAIL += 1

def warn(name, msg):
    global WARN
    print(f"  [WARN] {name} — {msg}")
    WARN += 1

print("=" * 70)
print("  FULL INTEGRATION TEST — Agentic AI Trader")
print("=" * 70)

# ══════════════════════════════════════════════════════════════
# SECTION 1: IMPORT TESTS
# ══════════════════════════════════════════════════════════════
print("\n[SECTION 1] IMPORT TESTS")
print("-" * 50)

def test_import_streaming():
    from backend.data.realtime_streaming import (
        RealtimeStreamingEngine, TickDataBuffer,
        get_streaming_engine, get_streaming_status,
        start_streaming, stop_streaming, streaming_engine
    )
    return True

def test_import_risk():
    from backend.agents.risk_management_engine import (
        RiskManagementEngine, RiskDecision,
        risk_engine, validate_trade,
        get_risk_dashboard, calculate_position_size
    )
    return True

def test_import_backtest():
    from backend.agents.backtesting_engine import (
        BacktestingEngine, BacktestResult,
        backtesting_engine, run_backtest, get_strategies
    )
    return True

def test_import_existing_modules():
    from market_engine import (
        app, socketio, ai_analyzer, ThreadSafeCache,
        RateLimiter, get_market_session, calculate_technical_indicators,
        INDIAN_STOCKS_CONFIG, INDIAN_MARKET_CONFIG
    )
    return True

def test_import_routes():
    from routes.api import api_bp
    from routes.auth import auth_bp
    import routes.websockets
    return True

def test_import_backend():
    from backend.data.user_db_manager import UserDBManager
    from backend.agents.risk_agent import RiskAgent
    from backend.agents.analysis_agent import generate_ai_analysis
    return True

test("Import: Real-Time Streaming Engine", test_import_streaming)
test("Import: Risk Management Engine", test_import_risk)
test("Import: Backtesting Engine", test_import_backtest)
test("Import: Existing market_engine module", test_import_existing_modules)
test("Import: Route blueprints (api, auth, websockets)", test_import_routes)
test("Import: Backend agents & data managers", test_import_backend)

# ══════════════════════════════════════════════════════════════
# SECTION 2: STREAMING ENGINE FUNCTIONAL TESTS
# ══════════════════════════════════════════════════════════════
print("\n[SECTION 2] REAL-TIME STREAMING ENGINE TESTS")
print("-" * 50)

def test_streaming_init():
    from backend.data.realtime_streaming import RealtimeStreamingEngine
    engine = RealtimeStreamingEngine()
    assert engine._is_active == False
    assert engine._total_ticks_generated == 0
    return True

def test_streaming_subscribe():
    from backend.data.realtime_streaming import RealtimeStreamingEngine
    engine = RealtimeStreamingEngine()
    engine.subscribe('RELIANCE')
    engine.subscribe('TCS')
    assert 'RELIANCE' in engine._subscribed_symbols
    assert 'TCS' in engine._subscribed_symbols
    engine.unsubscribe('TCS')
    assert 'TCS' not in engine._subscribed_symbols
    return True

def test_streaming_start_stop():
    from backend.data.realtime_streaming import RealtimeStreamingEngine
    engine = RealtimeStreamingEngine()
    engine.subscribe('NIFTY_50')
    engine.start()
    assert engine._is_active == True
    time.sleep(3)  # Let a few ticks generate
    ticks = engine.get_tick_buffer('NIFTY_50', 10)
    engine.stop()
    assert engine._is_active == False
    assert len(ticks) > 0, f"Expected ticks, got {len(ticks)}"
    return True

def test_streaming_tick_structure():
    from backend.data.realtime_streaming import RealtimeStreamingEngine
    engine = RealtimeStreamingEngine()
    engine.subscribe('RELIANCE')
    engine.start()
    time.sleep(3)
    ticks = engine.get_tick_buffer('RELIANCE', 5)
    engine.stop()
    assert len(ticks) > 0, "No ticks generated"
    tick = ticks[0]
    required_fields = ['tick_id', 'symbol', 'price', 'change', 'change_percent',
                       'bid', 'ask', 'spread', 'volume', 'timestamp', 'data_source']
    for f in required_fields:
        assert f in tick, f"Missing field: {f}"
    assert tick['price'] > 0
    assert tick['bid'] < tick['ask']
    return True

def test_streaming_status():
    from backend.data.realtime_streaming import get_streaming_status
    status = get_streaming_status()
    required_fields = ['is_active', 'connected_subscribers', 'symbols_streaming',
                       'tick_rate_per_second', 'total_ticks_generated', 'engine_type']
    for f in required_fields:
        assert f in status, f"Missing status field: {f}"
    assert status['engine_type'] == 'simulated_tick_stream'
    return True

def test_tick_buffer():
    from backend.data.realtime_streaming import TickDataBuffer
    buf = TickDataBuffer(max_ticks=5)
    buf.add_tick('TEST', {'price': 100})
    buf.add_tick('TEST', {'price': 101})
    buf.add_tick('TEST', {'price': 102})
    assert buf.get_tick_count('TEST') == 3
    assert len(buf.get_recent('TEST', 2)) == 2
    assert buf.get_recent('TEST', 2)[0]['price'] == 101
    # Test overflow
    for i in range(10):
        buf.add_tick('TEST', {'price': 200 + i})
    assert buf.get_tick_count('TEST') == 5  # max_ticks=5
    buf.clear('TEST')
    assert buf.get_tick_count('TEST') == 0
    return True

test("Streaming: Initialization", test_streaming_init)
test("Streaming: Subscribe/Unsubscribe", test_streaming_subscribe)
test("Streaming: Start/Stop + Tick Generation", test_streaming_start_stop)
test("Streaming: Tick Data Structure Validation", test_streaming_tick_structure)
test("Streaming: Status Dashboard", test_streaming_status)
test("Streaming: TickDataBuffer Circular Buffer", test_tick_buffer)

# ══════════════════════════════════════════════════════════════
# SECTION 3: RISK MANAGEMENT ENGINE FUNCTIONAL TESTS
# ══════════════════════════════════════════════════════════════
print("\n[SECTION 3] RISK MANAGEMENT ENGINE TESTS")
print("-" * 50)

def test_risk_init():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    assert engine.max_position_pct == 0.02
    assert engine.daily_loss_limit_pct == 0.05
    assert engine.max_drawdown_pct == 0.10
    assert engine.max_open_positions == 5
    return True

def test_risk_valid_buy():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    decision = engine.validate_trade(
        user_id=1, symbol='RELIANCE', quantity=5, price=2850.0,
        transaction_type='BUY', portfolio_value=1000000.0,
        cash_available=500000.0, current_holdings={'TCS': 10},
        todays_pnl=0.0, consecutive_losses=0
    )
    assert decision.approved == True, f"Should be approved: {decision.reason}"
    assert len(decision.checks_passed) >= 5
    assert len(decision.checks_failed) == 0
    return True

def test_risk_insufficient_balance():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    decision = engine.validate_trade(
        user_id=1, symbol='RELIANCE', quantity=100, price=2850.0,
        transaction_type='BUY', portfolio_value=1000000.0,
        cash_available=1000.0,  # Only Rs.1000 cash
        current_holdings={},
        todays_pnl=0.0, consecutive_losses=0
    )
    assert decision.approved == False, "Should be rejected — insufficient balance"
    assert any('Balance Check FAILED' in c for c in decision.checks_failed)
    return True

def test_risk_position_sizing_adjustment():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    # 100 shares * Rs.2850 = Rs.285,000 which is 28.5% of Rs.1M (exceeds 2% limit)
    decision = engine.validate_trade(
        user_id=1, symbol='RELIANCE', quantity=100, price=2850.0,
        transaction_type='BUY', portfolio_value=1000000.0,
        cash_available=500000.0, current_holdings={},
        todays_pnl=0.0, consecutive_losses=0
    )
    assert decision.adjusted_quantity < 100, f"Should be adjusted down from 100, got {decision.adjusted_quantity}"
    assert decision.adjusted_quantity == 7, f"Expected 7 (2% of 1M / 2850), got {decision.adjusted_quantity}"
    return True

def test_risk_daily_loss_circuit_breaker():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    decision = engine.validate_trade(
        user_id=2, symbol='INFY', quantity=5, price=1500.0,
        transaction_type='BUY', portfolio_value=1000000.0,
        cash_available=500000.0, current_holdings={},
        todays_pnl=-60000.0,  # Lost Rs.60K today (6% > 5% limit)
        consecutive_losses=0
    )
    assert decision.approved == False, "Should be rejected — circuit breaker"
    assert any('CIRCUIT BREAKER' in c for c in decision.checks_failed)
    return True

def test_risk_max_positions():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine(max_open_positions=3)
    decision = engine.validate_trade(
        user_id=3, symbol='WIPRO', quantity=5, price=480.0,
        transaction_type='BUY', portfolio_value=1000000.0,
        cash_available=500000.0,
        current_holdings={'RELIANCE': 10, 'TCS': 5, 'INFY': 8},  # Already 3 positions
        todays_pnl=0.0, consecutive_losses=0
    )
    assert decision.approved == False, "Should be rejected — max positions"
    assert any('Position Limit EXCEEDED' in c for c in decision.checks_failed)
    return True

def test_risk_consecutive_losses():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    decision = engine.validate_trade(
        user_id=4, symbol='SBIN', quantity=5, price=780.0,
        transaction_type='BUY', portfolio_value=1000000.0,
        cash_available=500000.0, current_holdings={},
        todays_pnl=0.0, consecutive_losses=5  # 5 losses (> 3 limit)
    )
    assert decision.approved == False, "Should be rejected — consecutive losses"
    assert any('COOLDOWN' in c for c in decision.checks_failed)
    return True

def test_risk_sell_always_allowed():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    # Even with circuit breaker active, SELL should be allowed
    decision = engine.validate_trade(
        user_id=5, symbol='RELIANCE', quantity=5, price=2850.0,
        transaction_type='SELL', portfolio_value=1000000.0,
        cash_available=500000.0,
        current_holdings={'RELIANCE': 10},
        todays_pnl=-60000.0,  # Circuit breaker territory
        consecutive_losses=5   # Consecutive loss territory
    )
    assert decision.approved == True, f"SELL should always be allowed: {decision.reason}"
    return True

def test_risk_position_size_calculator():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine(max_position_pct=0.02)
    qty = engine.calculate_position_size(1000000.0, 2850.0)
    assert qty == 7, f"Expected 7 (floor of 20000/2850), got {qty}"
    qty2 = engine.calculate_position_size(1000000.0, 100.0)
    assert qty2 == 200, f"Expected 200 (floor of 20000/100), got {qty2}"
    return True

def test_risk_dashboard():
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    dashboard = engine.get_risk_dashboard(
        user_id=1, portfolio_value=950000.0, cash=300000.0,
        holdings_count=3, todays_pnl=-15000.0, consecutive_losses=1
    )
    required = ['portfolio_value', 'cash_available', 'risk_level', 'risk_score',
                'circuit_breaker_active', 'kill_switch_active', 'positions_used',
                'max_positions', 'daily_pnl', 'engine_config']
    for f in required:
        assert f in dashboard, f"Missing dashboard field: {f}"
    assert dashboard['risk_level'] in ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')
    return True

def test_risk_decision_to_dict():
    from backend.agents.risk_management_engine import RiskDecision
    d = RiskDecision(
        approved=True, reason="Test", adjusted_quantity=5,
        risk_score=0.15, checks_passed=["A", "B"], checks_failed=[]
    )
    result = d.to_dict()
    assert result['approved'] == True
    assert result['pass_rate'] == 100.0
    assert result['total_checks'] == 2
    return True

test("Risk: Initialization & Defaults", test_risk_init)
test("Risk: Valid BUY Approved", test_risk_valid_buy)
test("Risk: Insufficient Balance Rejected", test_risk_insufficient_balance)
test("Risk: Position Sizing Auto-Adjustment", test_risk_position_sizing_adjustment)
test("Risk: Daily Loss Circuit Breaker", test_risk_daily_loss_circuit_breaker)
test("Risk: Max Open Positions Limit", test_risk_max_positions)
test("Risk: Consecutive Loss Guard", test_risk_consecutive_losses)
test("Risk: SELL Always Allowed (Even During Circuit Breaker)", test_risk_sell_always_allowed)
test("Risk: Position Size Calculator", test_risk_position_size_calculator)
test("Risk: Dashboard Structure", test_risk_dashboard)
test("Risk: RiskDecision.to_dict()", test_risk_decision_to_dict)

# ══════════════════════════════════════════════════════════════
# SECTION 4: BACKTESTING ENGINE FUNCTIONAL TESTS
# ══════════════════════════════════════════════════════════════
print("\n[SECTION 4] BACKTESTING ENGINE TESTS")
print("-" * 50)

def test_backtest_init():
    from backend.agents.backtesting_engine import BacktestingEngine
    engine = BacktestingEngine()
    assert engine.initial_capital == 1000000.0
    assert engine.brokerage_pct == 0.0003
    assert engine.slippage_pct == 0.0005
    return True

def test_backtest_strategies_list():
    from backend.agents.backtesting_engine import BacktestingEngine
    strategies = BacktestingEngine.get_available_strategies()
    assert len(strategies) == 3
    names = [s['name'] for s in strategies]
    assert 'RSI_MACD' in names
    assert 'BOLLINGER_BANDS' in names
    assert 'MOVING_AVERAGE_CROSSOVER' in names
    for s in strategies:
        assert 'description' in s
        assert 'risk_level' in s
    return True

def test_backtest_invalid_period():
    from backend.agents.backtesting_engine import BacktestingEngine
    engine = BacktestingEngine()
    try:
        engine.run_backtest('RELIANCE', '10y', 'RSI_MACD')
        return False  # Should have raised
    except ValueError as e:
        assert 'Invalid period' in str(e)
        return True

def test_backtest_invalid_strategy():
    from backend.agents.backtesting_engine import BacktestingEngine
    engine = BacktestingEngine()
    try:
        engine.run_backtest('RELIANCE', '1y', 'RANDOM_STRATEGY')
        return False
    except ValueError as e:
        assert 'Invalid strategy' in str(e)
        return True

def test_backtest_run_bollinger():
    from backend.agents.backtesting_engine import BacktestingEngine
    engine = BacktestingEngine()
    result = engine.run_backtest('RELIANCE', '1y', 'BOLLINGER_BANDS')
    assert result.symbol == 'RELIANCE'
    assert result.strategy == 'BOLLINGER_BANDS'
    assert result.period == '1y'
    assert result.initial_capital == 1000000.0
    assert len(result.equity_curve) > 0
    assert result.start_date < result.end_date
    # Verify equity curve structure
    ec = result.equity_curve[0]
    assert 'date' in ec
    assert 'portfolio_value' in ec
    assert 'drawdown_pct' in ec
    return True

def test_backtest_run_ma_crossover():
    from backend.agents.backtesting_engine import BacktestingEngine
    engine = BacktestingEngine()
    result = engine.run_backtest('TCS', '1y', 'MOVING_AVERAGE_CROSSOVER')
    assert result.symbol == 'TCS'
    assert result.strategy == 'MOVING_AVERAGE_CROSSOVER'
    assert len(result.equity_curve) > 0
    return True

def test_backtest_result_to_dict():
    from backend.agents.backtesting_engine import BacktestingEngine
    engine = BacktestingEngine()
    result = engine.run_backtest('INFY', '6mo', 'RSI_MACD')
    d = result.to_dict()
    required = ['symbol', 'strategy', 'period', 'initial_capital', 'final_capital',
                'total_return_pct', 'sharpe_ratio', 'max_drawdown_pct', 'win_rate_pct',
                'total_trades', 'trade_log', 'equity_curve', 'net_profit', 'roi_multiple']
    for f in required:
        assert f in d, f"Missing result field: {f}"
    return True

def test_backtest_symbol_resolution():
    from backend.agents.backtesting_engine import BacktestingEngine
    engine = BacktestingEngine()
    # Test that it resolves INDIAN_STOCKS_CONFIG symbols
    yf_sym = engine._resolve_yfinance_symbol('RELIANCE')
    assert yf_sym == 'RELIANCE.NS', f"Expected RELIANCE.NS, got {yf_sym}"
    yf_sym2 = engine._resolve_yfinance_symbol('HDFCBANK')
    assert yf_sym2 == 'HDFCBANK.NS', f"Expected HDFCBANK.NS, got {yf_sym2}"
    return True

test("Backtest: Initialization & Defaults", test_backtest_init)
test("Backtest: Strategies List (3 strategies)", test_backtest_strategies_list)
test("Backtest: Invalid Period Rejection", test_backtest_invalid_period)
test("Backtest: Invalid Strategy Rejection", test_backtest_invalid_strategy)
print("  [....] Backtest: Running RELIANCE 1yr BOLLINGER_BANDS (downloading data)...")
test("Backtest: Run RELIANCE BOLLINGER_BANDS", test_backtest_run_bollinger)
print("  [....] Backtest: Running TCS 1yr MA_CROSSOVER (downloading data)...")
test("Backtest: Run TCS MOVING_AVERAGE_CROSSOVER", test_backtest_run_ma_crossover)
print("  [....] Backtest: Running INFY 6mo RSI_MACD (downloading data)...")
test("Backtest: Result to_dict() Structure", test_backtest_result_to_dict)
test("Backtest: Symbol Resolution (RELIANCE -> RELIANCE.NS)", test_backtest_symbol_resolution)

# ══════════════════════════════════════════════════════════════
# SECTION 5: FLASK APP INTEGRATION TESTS
# ══════════════════════════════════════════════════════════════
print("\n[SECTION 5] FLASK APP INTEGRATION TESTS")
print("-" * 50)

def test_flask_app_creates():
    from market_engine import app
    assert app is not None
    return True

def test_flask_routes_registered():
    from perfect_indian_app import app
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    # Check new streaming endpoints
    assert '/api/streaming/status' in rules, "Missing /api/streaming/status"
    assert '/api/streaming/tick-buffer/<symbol>' in rules, "Missing /api/streaming/tick-buffer"
    # Check new risk endpoints
    assert '/api/risk/check' in rules, "Missing /api/risk/check"
    assert '/api/risk/status' in rules, "Missing /api/risk/status"
    assert '/api/risk/position-size' in rules, "Missing /api/risk/position-size"
    # Check new backtest endpoints
    assert '/api/backtest/run' in rules, "Missing /api/backtest/run"
    assert '/api/backtest/strategies' in rules, "Missing /api/backtest/strategies"
    return True

def test_flask_streaming_endpoint():
    from perfect_indian_app import app
    with app.test_client() as client:
        resp = client.get('/api/streaming/status')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.get_json()
        assert 'is_active' in data
        assert 'engine_type' in data
    return True

def test_flask_backtest_strategies_endpoint():
    from perfect_indian_app import app
    with app.test_client() as client:
        resp = client.get('/api/backtest/strategies')
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.get_json()
        assert 'strategies' in data
        assert len(data['strategies']) == 3
        assert 'valid_periods' in data
        assert 'valid_symbols' in data
        assert len(data['valid_symbols']) >= 15  # 20 stocks configured
    return True

def test_flask_risk_check_no_auth():
    from perfect_indian_app import app
    with app.test_client() as client:
        resp = client.post('/api/risk/check', json={
            'symbol': 'RELIANCE', 'quantity': 5, 'price': 2850, 'transaction_type': 'BUY'
        })
        # Should return 401 since not logged in
        assert resp.status_code == 401, f"Expected 401 (no auth), got {resp.status_code}"
    return True

def test_flask_existing_health_endpoint():
    from perfect_indian_app import app
    with app.test_client() as client:
        resp = client.get('/api/health')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'healthy'
    return True

def test_flask_existing_market_status():
    from perfect_indian_app import app
    with app.test_client() as client:
        resp = client.get('/api/market-status')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'status' in data
        assert 'session' in data
    return True

def test_flask_backtest_run_endpoint():
    from perfect_indian_app import app
    with app.test_client() as client:
        resp = client.post('/api/backtest/run', json={
            'symbol': 'SBIN', 'period': '6mo', 'strategy': 'BOLLINGER_BANDS'
        })
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.data}"
        data = resp.get_json()
        assert data.get('success') == True
        assert 'results' in data
        results = data['results']
        assert results['symbol'] == 'SBIN'
        assert results['strategy'] == 'BOLLINGER_BANDS'
        assert 'equity_curve' in results
        assert 'total_return_pct' in results
    return True

test("Flask: App Creates Without Errors", test_flask_app_creates)
test("Flask: All 7 New Routes Registered", test_flask_routes_registered)
test("Flask: GET /api/streaming/status Returns 200", test_flask_streaming_endpoint)
test("Flask: GET /api/backtest/strategies Returns 200", test_flask_backtest_strategies_endpoint)
test("Flask: POST /api/risk/check Returns 401 Without Login", test_flask_risk_check_no_auth)
test("Flask: GET /api/health Still Works (Existing)", test_flask_existing_health_endpoint)
test("Flask: GET /api/market-status Still Works (Existing)", test_flask_existing_market_status)
print("  [....] Flask: Running backtest via API endpoint (downloading data)...")
test("Flask: POST /api/backtest/run Returns Results", test_flask_backtest_run_endpoint)

# ══════════════════════════════════════════════════════════════
# SECTION 6: CROSS-MODULE INTEGRATION TESTS
# ══════════════════════════════════════════════════════════════
print("\n[SECTION 6] CROSS-MODULE INTEGRATION TESTS")
print("-" * 50)

def test_streaming_with_market_engine_prices():
    """Test that streaming engine can use market_engine's stock config"""
    from backend.data.realtime_streaming import RealtimeStreamingEngine
    from market_engine import INDIAN_STOCKS_CONFIG
    engine = RealtimeStreamingEngine()
    # Subscribe to all stocks from config
    for symbol in list(INDIAN_STOCKS_CONFIG.keys())[:5]:
        engine.subscribe(symbol)
    assert len(engine._subscribed_symbols) == 5
    return True

def test_risk_with_user_db():
    """Test risk engine works with user_db portfolio data structure"""
    from backend.agents.risk_management_engine import RiskManagementEngine
    engine = RiskManagementEngine()
    # Simulate the data structure from user_db.get_holdings()
    mock_holdings = [
        {'symbol': 'RELIANCE', 'qty': 10, 'avg_price': 2800, 'total_cost': 28000},
        {'symbol': 'TCS', 'qty': 5, 'avg_price': 3900, 'total_cost': 19500},
    ]
    cash = 952500.0
    current_holdings = {h['symbol']: h['qty'] for h in mock_holdings}
    portfolio_value = cash + sum(h['total_cost'] for h in mock_holdings)
    
    decision = engine.validate_trade(
        user_id=99, symbol='INFY', quantity=10, price=1480.0,
        transaction_type='BUY', portfolio_value=portfolio_value,
        cash_available=cash, current_holdings=current_holdings
    )
    assert isinstance(decision.approved, bool)
    assert decision.adjusted_quantity > 0
    return True

def test_backtest_with_stock_config():
    """Test backtesting resolves symbols from INDIAN_STOCKS_CONFIG"""
    from backend.agents.backtesting_engine import BacktestingEngine
    from market_engine import INDIAN_STOCKS_CONFIG
    engine = BacktestingEngine()
    # Verify all stocks can be resolved
    for symbol in list(INDIAN_STOCKS_CONFIG.keys())[:5]:
        yf_sym = engine._resolve_yfinance_symbol(symbol)
        assert yf_sym.endswith('.NS'), f"{symbol} should resolve to .NS, got {yf_sym}"
    return True

def test_database_exists():
    """Test that SQLite database is accessible"""
    import sqlite3
    db_path = os.path.join('data', 'user_data.db')
    assert os.path.exists(db_path), f"Database not found at {db_path}"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    conn.close()
    assert 'users' in tables
    assert 'portfolios' in tables
    assert 'watchlists' in tables
    assert 'alerts' in tables
    return True

test("Integration: Streaming Engine + Stock Config", test_streaming_with_market_engine_prices)
test("Integration: Risk Engine + User DB Structure", test_risk_with_user_db)
test("Integration: Backtesting + Stock Config Resolution", test_backtest_with_stock_config)
test("Integration: SQLite Database Exists & Tables OK", test_database_exists)

# ══════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
total = PASS + FAIL
print(f"  RESULTS: {PASS}/{total} PASSED, {FAIL}/{total} FAILED, {WARN} WARNINGS")
if FAIL == 0:
    print("  STATUS: ALL TESTS PASSED ✓")
else:
    print(f"  STATUS: {FAIL} TEST(S) FAILED ✗")
print("=" * 70)

sys.exit(0 if FAIL == 0 else 1)
