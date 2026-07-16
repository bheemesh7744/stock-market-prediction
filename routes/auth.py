#!/usr/bin/env python3
"""
Authentication Routes — Register, Login, Logout, Session Status
Uses Flask sessions for state and UserDBManager for credential storage.
"""

from flask import Blueprint, request, jsonify, session
from market_engine import user_db, logger
from routes.api import csrf_protect

auth_bp = Blueprint('auth', __name__)


def _get_current_user_id():
    """Return the logged-in user_id from session, or None."""
    return session.get('user_id')


def _get_current_username():
    """Return the logged-in username from session, or None."""
    return session.get('username')


# ══════════════════════════════════════════════════════════════
# REGISTER
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/api/auth/register', methods=['POST'])
@csrf_protect
def register():
    """Create a new user account.
    
    Expects JSON: { username, email, password }
    Constraints (enforced by UserDBManager):
      - Username: 3-20 chars, alphanumeric + underscore
      - Email: valid format
      - Password: min 8 characters
    """
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    result = user_db.create_user(username, email, password)

    if result['success']:
        # Auto-login after registration
        session.permanent = True
        session['user_id'] = result['user_id']
        session['username'] = result['username']
        logger.info(f"User registered and logged in: {result['username']}")
        return jsonify({
            'success': True,
            'user_id': result['user_id'],
            'username': result['username'],
            'message': 'Account created successfully!'
        })
    else:
        return jsonify({'success': False, 'message': result['message']}), 400


# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/api/auth/login', methods=['POST'])
@csrf_protect
def login():
    """Authenticate an existing user.
    
    Expects JSON: { username, password }
    `username` field accepts either username or email.
    """
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    result = user_db.verify_user(username, password)

    if result['success']:
        session.permanent = True
        session['user_id'] = result['user_id']
        session['username'] = result['username']
        logger.info(f"User logged in: {result['username']}")
        return jsonify({
            'success': True,
            'user_id': result['user_id'],
            'username': result['username'],
            'message': f"Welcome back, {result['username']}!"
        })
    else:
        return jsonify({'success': False, 'message': result['message']}), 401


# ══════════════════════════════════════════════════════════════
# LOGOUT
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/api/auth/logout', methods=['POST'])
@csrf_protect
def logout():
    """Clear the user session."""
    username = session.get('username', 'Unknown')
    session.clear()
    logger.info(f"User logged out: {username}")
    return jsonify({'success': True, 'message': 'Logged out successfully'})


# ══════════════════════════════════════════════════════════════
# SESSION STATUS
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/api/auth/status')
def auth_status():
    """Check current authentication state."""
    user_id = _get_current_user_id()
    if user_id:
        return jsonify({
            'logged_in': True,
            'user_id': user_id,
            'username': _get_current_username()
        })
    return jsonify({'logged_in': False})
