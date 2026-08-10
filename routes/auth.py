#!/usr/bin/env python3
"""
Authentication Routes — Register, Login, Logout, Session Status
Uses JWT for state and UserDBManager for credential storage.
"""

import os
import jwt
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session, current_app
from market_engine import user_db, logger
from routes.api import csrf_protect

auth_bp = Blueprint('auth', __name__)

JWT_EXPIRY_HOURS = 720  # 30 days

def get_jwt_secret():
    return os.environ.get('JWT_SECRET', current_app.config.get('SECRET_KEY', 'dev-jwt-secret'))

def generate_jwt(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload, get_jwt_secret(), algorithm='HS256')

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
def register():
    """Create a new user account.
    
    Expects JSON: { username, email, password }
    """
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    result = user_db.create_user(username, email, password)

    if result['success']:
        token = generate_jwt(result['user_id'], result['username'])
        # Fallback for backward compatibility
        session.permanent = True
        session['user_id'] = result['user_id']
        session['username'] = result['username']
        logger.info(f"User registered and logged in: {result['username']}")
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': result['user_id'],
                'username': result['username']
            },
            'message': 'Account created successfully!'
        })
    else:
        return jsonify({'success': False, 'message': result['message']}), 400


# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate an existing user.
    
    Expects JSON: { username, password }
    """
    data = request.get_json(silent=True) or {}
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required'}), 400

    result = user_db.verify_user(username, password)

    if result['success']:
        token = generate_jwt(result['user_id'], result['username'])
        session.permanent = True
        session['user_id'] = result['user_id']
        session['username'] = result['username']
        logger.info(f"User logged in: {result['username']}")
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': result['user_id'],
                'username': result['username']
            },
            'message': f"Welcome back, {result['username']}!"
        })
    else:
        return jsonify({'success': False, 'message': result['message']}), 401


# ══════════════════════════════════════════════════════════════
# LOGOUT
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/api/auth/logout', methods=['POST'])
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
    """Check current authentication state via JWT or session."""
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, get_jwt_secret(), algorithms=['HS256'])
            return jsonify({
                'logged_in': True,
                'user_id': payload.get('user_id'),
                'username': payload.get('username')
            })
        except jwt.ExpiredSignatureError:
            return jsonify({'logged_in': False, 'message': 'Token expired'})
        except jwt.InvalidTokenError:
            return jsonify({'logged_in': False, 'message': 'Invalid token'})

    # Fallback to session
    user_id = _get_current_user_id()
    if user_id:
        return jsonify({
            'logged_in': True,
            'user_id': user_id,
            'username': _get_current_username()
        })
    return jsonify({'logged_in': False})
