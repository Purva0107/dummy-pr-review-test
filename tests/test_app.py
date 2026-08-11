"""Tests for the dummy PR review harness."""

import sqlite3

import pytest

from app import find_user, get_average, get_user_age


def test_get_average_nonempty():
    assert get_average([1, 2, 3]) == pytest.approx(2.0)


def test_get_average_empty():
    assert get_average([]) == 0.0


def test_get_user_age_present():
    assert get_user_age({"age": 30}) == 30


def test_get_user_age_missing():
    assert get_user_age({}) is None


def test_find_user_uses_parameterized_query(tmp_path, monkeypatch):
    # :memory: DBs are per-connection; use a shared file DB for setup + find_user.
    db_path = tmp_path / "users.db"
    monkeypatch.setattr("app.DB_PATH", str(db_path))

    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE users (id INTEGER, username TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'alice')")
    conn.commit()
    conn.close()

    row = find_user("alice")
    assert row == (1, "alice")

    # Injection attempt should not return extra rows when parameterized.
    row = find_user("' OR '1'='1")
    assert row is None
