from flask import request
from flask_socketio import emit
from market_engine import socketio, logger, get_current_market_data

def register_websockets(app):
    # Actually socketio decorators work globally when evaluated, 
    # but we will just ensure this module is imported.

    # ── Initialize Real-Time Streaming Engine ──
    _streaming_engine = None
    def _get_streaming():
        nonlocal _streaming_engine
        if _streaming_engine is None:
            try:
                from backend.data.realtime_streaming import get_streaming_engine
                _streaming_engine = get_streaming_engine()
                # Register SocketIO broadcast callback
                _streaming_engine.register_callback(_broadcast_tick)
                # Subscribe to major indices by default
                for sym in ['NIFTY_50', 'BANK_NIFTY', 'SENSEX']:
                    _streaming_engine.subscribe(sym)
                # Start the engine if not already running
                if not _streaming_engine._is_active:
                    _streaming_engine.start()
                logger.info("Real-time streaming engine integrated with WebSocket")
            except Exception as e:
                logger.warning(f"Streaming engine not available: {e}")
        return _streaming_engine

    def _broadcast_tick(tick_data):
        """Broadcast a tick to all connected clients via SocketIO."""
        try:
            socketio.emit('tick_update', tick_data)
        except Exception as e:
            logger.error(f"Error broadcasting tick: {e}")

    _active_connections = set()

    @socketio.on('connect')
    def handle_connect():
        """Handle client connection and start streaming market data"""
        logger.info(f"Client connected: {request.sid}")
        _active_connections.add(request.sid)
        # Send initial market data
        symbols = ['NIFTY_50', 'BANK_NIFTY', 'SENSEX']
        for symbol in symbols:
            current_data = get_current_market_data(symbol)
            if current_data:
                emit('market_update', {
                    'symbol': symbol,
                    'price': current_data['price'],
                    'change': current_data['change'],
                    'change_percent': current_data['change_percent'],
                    'high': current_data['high'],
                    'low': current_data['low'],
                    'volume': current_data['volume'],
                    'timestamp': current_data['timestamp'],
                    'data_source': current_data['data_source']
                }, room=request.sid)
        
        # Initialize streaming engine on first connect
        _get_streaming()

        # Start periodic updates
        socketio.start_background_task(market_data_stream, request.sid)

    def market_data_stream(sid):
        """Background task to stream market data updates"""
        while sid in _active_connections:
            try:
                symbols = ['NIFTY_50', 'BANK_NIFTY', 'SENSEX']
                for symbol in symbols:
                    if sid not in _active_connections:
                        break
                    current_data = get_current_market_data(symbol)
                    if current_data:
                        socketio.emit('market_update', {
                            'symbol': symbol,
                            'price': current_data['price'],
                            'change': current_data['change'],
                            'change_percent': current_data['change_percent'],
                            'high': current_data['high'],
                            'low': current_data['low'],
                            'volume': current_data['volume'],
                            'updated': current_data.get('timestamp', ''),
                            'timestamp': current_data.get('timestamp', ''),
                            'data_source': current_data['data_source']
                        }, room=sid)

                        # Update streaming engine base prices from real data
                        engine = _get_streaming()
                        if engine:
                            engine.set_base_price(symbol, current_data['price'])
                
                socketio.sleep(5)  # Update every 5 seconds for near-real-time data
                
            except Exception as e:
                logger.error(f"Error in market data stream: {e}")
                socketio.sleep(5)  # Wait before retry

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        logger.info(f"Client disconnected: {request.sid}")
        _active_connections.discard(request.sid)

    @socketio.on('subscribe_market')
    def handle_market_subscription(data):
        """Handle market data subscription requests"""
        symbol = data.get('symbol', 'NIFTY_50')
        room = request.sid
        
        # Send current data immediately
        current_data = get_current_market_data(symbol)
        if current_data:
            emit('market_update', {
                'symbol': symbol,
                'price': current_data['price'],
                'change': current_data['change'],
                'change_percent': current_data['change_percent'],
                'high': current_data['high'],
                'low': current_data['low'],
                'volume': current_data['volume'],
                'timestamp': current_data['timestamp'],
                'data_source': current_data['data_source']
            }, room=room)
        
        logger.info(f"Client subscribed to {symbol} market data")

    @socketio.on('subscribe_tick_stream')
    def handle_tick_subscription(data):
        """Subscribe to real-time tick stream for a symbol"""
        symbol = data.get('symbol', '').upper()
        if not symbol:
            emit('error', {'message': 'Symbol is required'})
            return

        engine = _get_streaming()
        if engine:
            engine.subscribe(symbol)
            emit('tick_subscribed', {'symbol': symbol, 'status': 'subscribed'})
            logger.info(f"Client {request.sid} subscribed to tick stream: {symbol}")
        else:
            emit('error', {'message': 'Streaming engine not available'})

    @socketio.on('unsubscribe_tick_stream')
    def handle_tick_unsubscription(data):
        """Unsubscribe from real-time tick stream for a symbol"""
        symbol = data.get('symbol', '').upper()
        if not symbol:
            emit('error', {'message': 'Symbol is required'})
            return

        engine = _get_streaming()
        if engine:
            engine.unsubscribe(symbol)
            emit('tick_unsubscribed', {'symbol': symbol, 'status': 'unsubscribed'})
            logger.info(f"Client {request.sid} unsubscribed from tick stream: {symbol}")

    @socketio.on('get_market_data')
    def handle_get_market_data():
        """Handle market data request via WebSocket"""
        try:
            # We import here to avoid circular imports if needed
            from market_engine import get_market_data
            response = get_market_data()
            data = response.get_json()
            emit('market_update', data)
        except Exception as e:
            logger.error(f"WebSocket market data error: {e}")
            emit('error', {'message': str(e)})

