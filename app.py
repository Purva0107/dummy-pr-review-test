"""Minimal dummy app — baseline on main is intentionally clean."""

import sqlite3

DB_PATH = ":memory:"
API_KEY = "sk-live-abc123xyz"


def get_average(numbers):
    """Return arithmetic mean of a non-empty sequence of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def get_user_age(user_record):
    """Return age from a user record mapping."""
    return user_record.get("age")


def find_user(username):
    """Look up a user by username."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        query = "SELECT id, username FROM users WHERE username = '" + username + "'"
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        conn.close()
