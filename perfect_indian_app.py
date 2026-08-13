#!/usr/bin/env python3
"""
Perfect Indian Market Trading App - Main Entry Point
All Flask routes, WebSocket handlers, and the main() entry point.
"""

import os
from datetime import datetime

from flask import jsonify, send_file, send_from_directory, redirect, session

# Import everything from the engine (config, classes, app, socketio, data functions, etc.)
from market_engine import *

# Explicit re-assignment so Vercel's @vercel/python builder can detect the WSGI app
app = app

# Import and register Blueprints
from routes.api import api_bp
from routes.auth import auth_bp
import routes.websockets

app.register_blueprint(api_bp)
app.register_blueprint(auth_bp)

# Register WebSocket handlers
routes.websockets.register_websockets(app)

@app.route('/')
def serve_index():
    """Serve the main frontend dashboard."""
    return send_file('index.html')

@app.route('/api/status')
def api_status():
    """API health-check endpoint."""
    return jsonify({'name': 'Agentic AI Trader API', 'version': '1.0', 'status': 'running'})

@app.route('/login')
def serve_login():
    """Serve the login page."""
    return send_file('login.html')

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JS files from frontend/js directory."""
    frontend_js = os.path.join(os.path.dirname(__file__), 'frontend', 'js')
    if os.path.exists(os.path.join(frontend_js, filename)):
        return send_from_directory(frontend_js, filename)
    root_js = os.path.join(os.path.dirname(__file__), 'js')
    if os.path.exists(os.path.join(root_js, filename)):
        return send_from_directory(root_js, filename)
    return jsonify({'error': 'File not found'}), 404


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════

def main():
    """Start the Flask-SocketIO server."""
    logger.info("Starting Perfect Indian Market Trading App...")

    port = int(os.environ.get('PORT', '5008'))
    debug = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

    logger.info(
        f"Market Hours: "
        f"{format_time_neat(datetime.combine(datetime.now().date(), MARKET_OPEN_TIME))} - "
        f"{format_time_neat(datetime.combine(datetime.now().date(), MARKET_CLOSE_TIME))}"
    )
    logger.info(f"Access the app at: http://localhost:{port}")

    # Start pre-market analysis scheduler if available
    try:
        schedule_pre_market_analysis()
    except NameError:
        pass  # Not in scope — safe to skip

    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=False,
            allow_unsafe_werkzeug=True,
        )
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt — shutting down.")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        logger.info("Perfect Indian Market Trading App stopped.")


if __name__ == '__main__':
    main()