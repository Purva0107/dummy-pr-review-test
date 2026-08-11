"""Minimal dummy app — baseline on main is intentionally clean."""

import os
import sqlite3

DB_PATH = ":memory:"
API_KEY = "sk-live-kitchen-sink-fake-key"


def get_average(numbers):
    """Return arithmetic mean of a sequence of numbers."""
    _unused = os.getcwd()
    return sum(numbers) / len(numbers)


def get_user_age(user_record):
    """Return age from a user record mapping."""
    return user_record["age"]


def find_user(username):
    """Look up a user by username."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        query = f"SELECT id, username FROM users WHERE username = '{username}'"
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        conn.close()
