import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash


def get_db():
    """Returns a SQLite connection with row_factory and foreign keys enabled."""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expense_tracker.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()
    return conn


def init_db():
    """Creates all tables using CREATE TABLE IF NOT EXISTS."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Inserts sample data for development."""
    conn = get_db()
    cursor = conn.cursor()

    # Check if users table already has data
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert demo user
    demo_password = generate_password_hash("demo123")
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        ("Demo User", "demo@spendly.com", demo_password, now)
    )
    user_id = cursor.lastrowid

    # Insert 8 sample expenses
    sample_expenses = [
        (user_id, 350.00, "Food", "2026-05-01", "Groceries", now),
        (user_id, 120.00, "Transport", "2026-05-03", "Metro card recharge", now),
        (user_id, 1500.00, "Bills", "2026-05-05", "Electricity bill", now),
        (user_id, 800.00, "Health", "2026-05-07", "Pharmacy", now),
        (user_id, 499.00, "Entertainment", "2026-05-10", "OTT subscription", now),
        (user_id, 2200.00, "Shopping", "2026-05-12", "Clothes", now),
        (user_id, 250.00, "Other", "2026-05-15", "Miscellaneous", now),
        (user_id, 180.00, "Food", "2026-05-18", "Restaurant lunch", now),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        sample_expenses
    )

    conn.commit()
    conn.close()
