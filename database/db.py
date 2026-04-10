import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'expense_tracker.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            category    TEXT    NOT NULL,
            amount      REAL    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    # Only seed if no users exist
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    conn.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        ('Alice Demo', 'alice@example.com', 'hashed_password_placeholder'),
    )
    user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    expenses = [
        (user_id, 'Food',          450.00,  '2026-04-01', 'Lunch at cafe'),
        (user_id, 'Travel',       1200.00,  '2026-04-03', 'Cab to airport'),
        (user_id, 'Bills',        3500.00,  '2026-04-05', 'Electricity bill'),
        (user_id, 'Food',          320.00,  '2026-04-06', 'Grocery shopping'),
        (user_id, 'Entertainment', 899.00,  '2026-04-07', 'Netflix + Spotify'),
        (user_id, 'Travel',        650.00,  '2026-04-08', 'Metro card recharge'),
        (user_id, 'Health',       1500.00,  '2026-04-09', 'Pharmacy'),
        (user_id, 'Shopping',     2200.00,  '2026-04-10', 'New shoes'),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, category, amount, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )

    conn.commit()
    conn.close()
