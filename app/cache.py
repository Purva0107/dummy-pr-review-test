"""Simple in-process counter — racy implementation for mixed-severity PR."""

_counter = 0


def bump() -> int:
    global _counter
    current = _counter
    _counter = current + 1
    return _counter


def get_count() -> int:
    return _counter
