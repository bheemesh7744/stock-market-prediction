#!/usr/bin/env python3
"""
Perfect Indian Market Trading App - Main Entry Point
All Flask routes, WebSocket handlers, and the main() entry point.
"""

import os
from datetime import datetime

# Flask imports — only what is actually used here
from flask import render_template_string, redirect, url_for, session

# Import everything from the engine (config, classes, app, socketio, data functions, etc.)
from market_engine import *

# Import HTML frontend templates
from html_template import HTML_TEMPLATE, LOGIN_TEMPLATE

# Import and register Blueprints
from routes.api import api_bp
from routes.auth import auth_bp
import routes.websockets

app.register_blueprint(api_bp)
app.register_blueprint(auth_bp)

# Register WebSocket handlers
routes.websockets.register_websockets(app)


# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════

def _get_market_data_dict():
    """Fetch live market data for all symbols; falls back to simulated data. Never raises."""
    symbols = ['NIFTY_50', 'BANK_NIFTY', 'SENSEX']
    latest_data = {}
    for symbol in symbols:
        try:
            current_data = get_current_market_data(symbol)
            if current_data:
                latest_data[symbol] = current_data
            else:
                latest_data[symbol] = generate_simulated_market_data(symbol)
        except Exception as e:
            logger.warning(f"Market data failed for {symbol}: {e}")
            try:
                latest_data[symbol] = generate_simulated_market_data(symbol)
            except Exception as sim_err:
                logger.error(f"Simulated data also failed for {symbol}: {sim_err}")
    return latest_data


def _get_initial_page_context():
    """Build template context for the index page. Never raises."""
    try:
        market_data = _get_market_data_dict()
    except Exception as e:
        logger.error(f"Failed to get initial market data: {e}")
        market_data = {}

    try:
        session_data = get_market_session()
        status_display = (
            'Market Open' if session_data.get('status') == 'open' else 'Market Closed'
        )
    except Exception:
        status_display = 'Market Status'

    now = datetime.now(INDIAN_TIMEZONE)
    time_str = now.strftime('%I:%M %p')

    # Auth state from Flask session
    from flask import session as flask_session
    is_logged_in = 'user_id' in flask_session
    logged_in_username = flask_session.get('username', '')
    logged_in_user_id = flask_session.get('user_id', '')

    # CSRF token generation
    from routes.api import ensure_csrf_token
    csrf_token = ensure_csrf_token()

    return {
        'initial_market_data': market_data,
        'initial_status': status_display,
        'initial_time': time_str,
        'indian_stocks_config': INDIAN_STOCKS_CONFIG,
        'is_logged_in': is_logged_in,
        'username': logged_in_username,
        'user_id': logged_in_user_id,
        'csrf_token': csrf_token,
    }


# ══════════════════════════════════════════════════════════════
# PAGE ROUTES
# ══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    """
    Main trading app page.
    Server-renders initial market data so the page always shows data on first load,
    even before WebSocket or API calls complete on the client.
    """
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    ctx = _get_initial_page_context()
    return render_template_string(HTML_TEMPLATE, **ctx)


@app.route('/login')
def login_page():
    """Render the standalone sign-in and register landing page."""
    if 'user_id' in session:
        return redirect(url_for('index'))
    from routes.api import ensure_csrf_token
    return render_template_string(LOGIN_TEMPLATE, csrf_token=ensure_csrf_token())





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