"""
User Database Manager - Manages user authentication, watchlists, portfolios, and alerts
Stores all user persistent data in data/user_data.db (isolated from market caches)
Uses robust connection handling with timeouts and auto-rollback to prevent locking.
"""

import os
import sqlite3
import hashlib
import hmac
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger(__name__)

class UserDBManager:
    """Manager for user profile, authentication, watchlist, portfolio, and alerts database"""
    
    def __init__(self, db_dir: str = None):
        if db_dir is None:
            # Use absolute path based on this file's location: backend/data/user_data.db
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.db_dir = base_dir / "data"
        else:
            self.db_dir = Path(db_dir)
            
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.db_dir / "user_data.db"
        self._init_database()
        
    def _get_conn(self):
        """Helper to get a database connection with a 30-second timeout to prevent locking"""
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=5000")
        except Exception as e:
            logger.warning(f"Failed to set PRAGMAs on sqlite connection: {e}")
        return conn
        
    def _init_database(self):
        """Initialize database schemas"""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            
            # 1. Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # 2. Watchlists table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS watchlists (
                    user_id INTEGER NOT NULL,
                    symbol TEXT NOT NULL,
                    PRIMARY KEY (user_id, symbol),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # 3. Portfolios table (ledger)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS portfolios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    symbol TEXT,
                    quantity INTEGER,
                    price REAL,
                    transaction_type TEXT NOT NULL, -- 'BUY', 'SELL', 'DEPOSIT'
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            # 4. Alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    symbol TEXT NOT NULL,
                    price_threshold REAL NOT NULL,
                    condition TEXT NOT NULL, -- 'ABOVE', 'BELOW'
                    is_triggered INTEGER DEFAULT 0, -- 0=Active, 1=Triggered
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            logger.info("User database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing user database: {e}")
            conn.rollback()
        finally:
            conn.close()

    # ══════════════════════════════════════════════════════════════
    # AUTHENTICATION
    # ══════════════════════════════════════════════════════════════

    def _hash_password(self, password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """Hash password using PBKDF2 with SHA-256 and a random salt"""
        if not salt:
            salt = os.urandom(16).hex()
        
        pw_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        return pw_hash, salt

    def create_user(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Register a new user and initialize their virtual balance with 10 Lakhs INR"""
        username = username.strip()
        email = email.strip().lower()
        
        if not username or not email or not password:
            return {'success': False, 'message': 'All fields are required'}
            
        import re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {'success': False, 'message': 'Invalid email format'}
            
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
            return {'success': False, 'message': 'Username must be 3-20 characters long and contain only letters, numbers, and underscores'}
            
        if len(password) < 8:
            return {'success': False, 'message': 'Password must be at least 8 characters'}
            
        pw_hash, salt = self._hash_password(password)
        now = datetime.utcnow().isoformat()
        
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            
            # Insert user
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, salt, created_at) VALUES (?, ?, ?, ?, ?)",
                (username, email, pw_hash, salt, now)
            )
            user_id = cursor.lastrowid
            
            # Deposit default virtual capital (10 Lakhs INR)
            cursor.execute(
                "INSERT INTO portfolios (user_id, symbol, quantity, price, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, 'CASH', 1, 1000000.0, 'DEPOSIT', now)
            )
            
            conn.commit()
            logger.info(f"Registered new user: {username} (ID: {user_id})")
            return {'success': True, 'user_id': user_id, 'username': username}
            
        except sqlite3.IntegrityError as e:
            conn.rollback()
            msg = str(e).lower()
            if 'username' in msg:
                return {'success': False, 'message': 'Username already exists. Please choose another.'}
            elif 'email' in msg:
                return {'success': False, 'message': 'Email is already registered'}
            return {'success': False, 'message': 'User already exists'}
        except Exception as e:
            conn.rollback()
            logger.error(f"Error creating user {username}: {e}")
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()

    def verify_user(self, username_or_email: str, password: str) -> Dict[str, Any]:
        """Authenticate user credentials"""
        val = username_or_email.strip()
        
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            # Query by username or email
            cursor.execute(
                "SELECT id, username, password_hash, salt FROM users WHERE username = ? OR email = ?",
                (val, val.lower())
            )
            row = cursor.fetchone()
            
            if not row:
                return {'success': False, 'message': 'Invalid username or password'}
                
            user_id, username, stored_hash, salt = row
            check_hash, _ = self._hash_password(password, salt)
            
            if hmac.compare_digest(stored_hash, check_hash):
                return {'success': True, 'user_id': user_id, 'username': username}
            else:
                return {'success': False, 'message': 'Invalid username or password'}
        except Exception as e:
            logger.error(f"Error verifying credentials: {e}")
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()

    # ══════════════════════════════════════════════════════════════
    # WATCHLIST MANAGEMENT
    # ══════════════════════════════════════════════════════════════

    def get_watchlist(self, user_id: int) -> List[str]:
        """Retrieve user's watchlist symbols"""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT symbol FROM watchlists WHERE user_id = ? ORDER BY symbol ASC", (user_id,))
            rows = cursor.fetchall()
            return [r[0] for r in rows]
        except Exception as e:
            logger.error(f"Error fetching watchlist for user {user_id}: {e}")
            return []
        finally:
            conn.close()

    def add_to_watchlist(self, user_id: int, symbol: str) -> Dict[str, Any]:
        """Add symbol to user's watchlist"""
        symbol = symbol.strip().upper()
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO watchlists (user_id, symbol) VALUES (?, ?)", (user_id, symbol))
            conn.commit()
            return {'success': True}
        except Exception as e:
            conn.rollback()
            logger.error(f"Error adding to watchlist: {e}")
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()

    def remove_from_watchlist(self, user_id: int, symbol: str) -> Dict[str, Any]:
        """Remove symbol from user's watchlist"""
        symbol = symbol.strip().upper()
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM watchlists WHERE user_id = ? AND symbol = ?", (user_id, symbol))
            conn.commit()
            return {'success': True}
        except Exception as e:
            conn.rollback()
            logger.error(f"Error removing from watchlist: {e}")
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()



    def get_holdings(self, user_id: int) -> Dict[str, Any]:
        """Aggregate transaction ledger to calculate holdings, cash, and performance indicators"""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            
            # Fetch all ledger items
            cursor.execute("""
                SELECT symbol, quantity, price, transaction_type 
                FROM portfolios WHERE user_id = ? 
                ORDER BY timestamp ASC
            """, (user_id,))
            rows = cursor.fetchall()
            
            cash = 0.0
            holdings = {}
            
            for symbol, qty, price, tx_type in rows:
                if tx_type == 'DEPOSIT':
                    cash += price
                elif tx_type == 'BUY':
                    cash -= (qty * price)
                    if symbol not in holdings:
                        holdings[symbol] = {'qty': 0, 'total_cost': 0.0}
                    holdings[symbol]['qty'] += qty
                    holdings[symbol]['total_cost'] += (qty * price)
                elif tx_type == 'SELL':
                    cash += (qty * price)
                    if symbol in holdings:
                        avg_cost = holdings[symbol]['total_cost'] / holdings[symbol]['qty']
                        holdings[symbol]['qty'] -= qty
                        holdings[symbol]['total_cost'] = holdings[symbol]['qty'] * avg_cost
                        if holdings[symbol]['qty'] <= 0:
                            del holdings[symbol]
                            
            formatted_holdings = []
            for sym, data in holdings.items():
                if data['qty'] > 0:
                    avg_price = data['total_cost'] / data['qty']
                    formatted_holdings.append({
                        'symbol': sym,
                        'qty': data['qty'],
                        'avg_price': round(avg_price, 2),
                        'total_cost': round(data['total_cost'], 2)
                    })
                    
            return {
                'success': True,
                'cash': round(cash, 2),
                'holdings': formatted_holdings
            }
        except Exception as e:
            logger.error(f"Error generating holdings: {e}")
            return {'success': False, 'message': str(e)}
        finally:
            conn.close()

    def get_transaction_history(self, user_id: int) -> List[Dict[str, Any]]:
        """Retrieve all transaction history for a user."""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, symbol, quantity, price, transaction_type, timestamp 
                FROM portfolios WHERE user_id = ? 
                ORDER BY timestamp DESC
            """, (user_id,))
            rows = cursor.fetchall()
            return [{
                'id': r[0],
                'symbol': r[1],
                'quantity': r[2],
                'price': r[3],
                'transaction_type': r[4],
                'timestamp': r[5]
            } for r in rows]
        except Exception as e:
            logger.error(f"Error fetching transaction history: {e}")
            return []
        finally:
            conn.close()

    # ══════════════════════════════════════════════════════════════
    # PRICE ALERTS
    # ══════════════════════════════════════════════════════════════


    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Fetch all untriggered alerts across all users (for background websocket processor)"""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.user_id, a.symbol, a.price_threshold, a.condition, u.username
                FROM alerts a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_triggered = 0
            """)
            rows = cursor.fetchall()
            return [{
                'id': r[0],
                'user_id': r[1],
                'symbol': r[2],
                'price_threshold': r[3],
                'condition': r[4],
                'username': r[5]
            } for r in rows]
        except Exception as e:
            logger.error(f"Error fetching active alerts: {e}")
            return []
        finally:
            conn.close()

    def mark_alert_triggered(self, alert_id: int) -> bool:
        """Mark an alert as triggered to avoid duplicate alerts"""
        conn = self._get_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE alerts SET is_triggered = 1 WHERE id = ?", (alert_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Error triggering alert {alert_id}: {e}")
            return False
        finally:
            conn.close()
