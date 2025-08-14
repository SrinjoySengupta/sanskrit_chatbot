# app/db.py
"""
SQLite helper functions for the Sanskrit Chatbot app.
Provides:
- init_db(): create tables (users, logs)
- add_user(name, roll, college): store KYC, returns user_id
- get_user_by_roll(roll): return user row or None
- log_query(user_roll, query_text, results_text, top_score): store chat interaction
- get_all_users(), get_all_logs()
- export_users_csv(path), export_logs_csv(path)
"""

import sqlite3
import os
from datetime import datetime
import pandas as pd
from typing import Optional, List, Dict, Any

from app.config import DB_PATH

# Ensure folder exists for DB_PATH
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)


def _get_conn():
    """Return a sqlite3 connection with sensible defaults."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = _get_conn()
    cur = conn.cursor()
    # Users table: basic KYC
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            college TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    # Logs table: each chat query with result and score
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_roll TEXT,              -- FK by roll_no (optional)
            query_text TEXT NOT NULL,
            results_text TEXT NOT NULL,  -- the returned results (stringified)
            top_score REAL,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def add_user(name: str, roll: str, college: str) -> int:
    """
    Insert a user (KYC). If roll_no already exists, return existing user's id.
    Returns user id (int).
    """
    conn = _get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    try:
        cur.execute(
            "INSERT INTO users (name, roll_no, college, created_at) VALUES (?, ?, ?, ?);",
            (name.strip(), roll.strip(), college.strip(), now),
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        # roll_no unique constraint violation -> fetch existing id
        cur.execute("SELECT id FROM users WHERE roll_no = ?;", (roll.strip(),))
        row = cur.fetchone()
        user_id = row["id"] if row else -1
    finally:
        conn.close()
    return user_id


def get_user_by_roll(roll: str) -> Optional[Dict[str, Any]]:
    """Return user row as dict or None if not found."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE roll_no = ?;", (roll.strip(),))
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def log_query(user_roll: Optional[str], query_text: str, results_text: str, top_score: Optional[float]) -> int:
    """
    Log a search/query.
    user_roll may be None or empty if anonymous.
    Returns log id.
    """
    conn = _get_conn()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO logs (user_roll, query_text, results_text, top_score, created_at) VALUES (?, ?, ?, ?, ?);",
        (user_roll if user_roll else None, query_text, results_text, top_score, now),
    )
    conn.commit()
    log_id = cur.lastrowid
    conn.close()
    return log_id


def get_all_users() -> List[Dict[str, Any]]:
    """Return list of all users as dicts."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY created_at DESC;")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_logs(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """Return logs as list of dicts. If limit provided, limit rows."""
    conn = _get_conn()
    cur = conn.cursor()
    if limit:
        cur.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT ?;", (limit,))
    else:
        cur.execute("SELECT * FROM logs ORDER BY created_at DESC;")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def export_users_csv(path: str):
    """Export users table to CSV (overwrites)."""
    users = get_all_users()
    df = pd.DataFrame(users)
    df.to_csv(path, index=False, encoding="utf-8")


def export_logs_csv(path: str):
    """Export logs table to CSV (overwrites)."""
    logs = get_all_logs()
    df = pd.DataFrame(logs)
    df.to_csv(path, index=False, encoding="utf-8")


# Initialize DB on import if missing
init_db()
