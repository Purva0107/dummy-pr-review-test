"""Minimal dummy app — baseline on main is intentionally clean."""

import sqlite3

DB_PATH = ":memory:"


def get_average(numbers):
    """Return arithmetic mean of a sequence of numbers."""
    return sum(numbers) / len(numbers)


def get_user_age(user_record):
    """Return age from a user record mapping."""
    return user_record.get("age")


def find_user(username):
    """Look up a user by username."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username FROM users WHERE username = ?",
            (username,),
        )
        return cursor.fetchone()
    finally:
        conn.close()
