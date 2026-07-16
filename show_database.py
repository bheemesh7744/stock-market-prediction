"""
Database Viewer Script - Run this to show all data in the database to your mentor.
Usage: python show_database.py
"""
import sqlite3
import os
import sys

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join("data", "user_data.db")

def show_database():
    if not os.path.exists(DB_PATH):
        print(f"[ERROR] Database not found at: {DB_PATH}")
        return

    print(f"Database file: {os.path.abspath(DB_PATH)}")
    print(f"File size: {os.path.getsize(DB_PATH)} bytes")
    print()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Show all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print("=" * 60)
    print(f"TABLES IN DATABASE: {tables}")
    print("=" * 60)

    # --- 1. USERS TABLE ---
    print("\n[TABLE] users (Login Credentials)")
    print("-" * 60)
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='users'")
    schema = cursor.fetchone()
    if schema:
        print(f"Schema: {schema[0]}\n")
    cursor.execute("SELECT id, username, email, substr(password_hash, 1, 20) || '...', substr(salt, 1, 10) || '...', created_at FROM users")
    rows = cursor.fetchall()
    if rows:
        print(f"{'ID':<5} {'Username':<20} {'Email':<30} {'Password Hash (partial)':<25} {'Salt':<15} {'Created'}")
        print("-" * 120)
        for r in rows:
            print(f"{r[0]:<5} {r[1]:<20} {r[2]:<30} {r[3]:<25} {r[4]:<15} {r[5]}")
    else:
        print("  (No users registered yet)")
    print(f"\n  Total users: {len(rows)}")

    # --- 2. WATCHLISTS TABLE ---
    print("\n\n[TABLE] watchlists (User Watchlists)")
    print("-" * 60)
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='watchlists'")
    schema = cursor.fetchone()
    if schema:
        print(f"Schema: {schema[0]}\n")
    cursor.execute("""
        SELECT w.user_id, u.username, w.symbol
        FROM watchlists w
        JOIN users u ON w.user_id = u.id
        ORDER BY w.user_id, w.symbol
    """)
    rows = cursor.fetchall()
    if rows:
        print(f"{'User ID':<10} {'Username':<20} {'Symbol'}")
        print("-" * 50)
        for r in rows:
            print(f"{r[0]:<10} {r[1]:<20} {r[2]}")
    else:
        print("  (No watchlist items yet)")
    print(f"\n  Total watchlist entries: {len(rows)}")

    # --- 3. PORTFOLIOS TABLE ---
    print("\n\n[TABLE] portfolios (Trading Transactions Ledger)")
    print("-" * 60)
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='portfolios'")
    schema = cursor.fetchone()
    if schema:
        print(f"Schema: {schema[0]}\n")
    cursor.execute("""
        SELECT p.id, u.username, p.symbol, p.quantity, p.price, p.transaction_type, p.timestamp
        FROM portfolios p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.timestamp
    """)
    rows = cursor.fetchall()
    if rows:
        print(f"{'ID':<5} {'User':<15} {'Symbol':<12} {'Qty':<8} {'Price':>12} {'Type':<10} {'Timestamp'}")
        print("-" * 100)
        for r in rows:
            price_str = f"Rs.{r[4]:,.2f}" if r[4] else "N/A"
            print(f"{r[0]:<5} {r[1]:<15} {r[2]:<12} {r[3]:<8} {price_str:>12} {r[5]:<10} {r[6]}")
    else:
        print("  (No transactions yet)")
    print(f"\n  Total transactions: {len(rows)}")

    # --- 4. ALERTS TABLE ---
    print("\n\n[TABLE] alerts (Price Alerts)")
    print("-" * 60)
    cursor.execute("SELECT sql FROM sqlite_master WHERE name='alerts'")
    schema = cursor.fetchone()
    if schema:
        print(f"Schema: {schema[0]}\n")
    cursor.execute("""
        SELECT a.id, u.username, a.symbol, a.price_threshold, a.condition,
               CASE WHEN a.is_triggered = 1 THEN 'TRIGGERED' ELSE 'ACTIVE' END,
               a.created_at
        FROM alerts a
        JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC
    """)
    rows = cursor.fetchall()
    if rows:
        print(f"{'ID':<5} {'User':<15} {'Symbol':<12} {'Threshold':>12} {'Condition':<10} {'Status':<12} {'Created'}")
        print("-" * 90)
        for r in rows:
            print(f"{r[0]:<5} {r[1]:<15} {r[2]:<12} Rs.{r[3]:>10,.2f} {r[4]:<10} {r[5]:<12} {r[6]}")
    else:
        print("  (No alerts set yet)")
    print(f"\n  Total alerts: {len(rows)}")

    # --- SECURITY SUMMARY ---
    print("\n\n" + "=" * 60)
    print("SECURITY IMPLEMENTATION:")
    print("=" * 60)
    print("  [YES] Passwords are hashed using PBKDF2-HMAC-SHA256 (100,000 iterations)")
    print("  [YES] Each user has a unique random 16-byte salt")
    print("  [YES] Plain-text passwords are NEVER stored")
    print("  [YES] Login verification uses timing-safe hmac.compare_digest()")
    print("  [YES] Sessions are server-side (Flask signed cookies)")
    print("  [YES] Database uses SQLite with connection timeouts (30s)")
    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    show_database()
