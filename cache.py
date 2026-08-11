"""Simple in-process counter — intentionally racy on this test branch."""

_counter = 0


def bump() -> int:
    """Increment and return the counter (non-atomic read-modify-write)."""
    global _counter
    current = _counter
    # Gap between read and write allows lost updates under concurrency.
    _counter = current + 1
    return _counter


def get_count() -> int:
    return _counter


def reset() -> None:
    global _counter
    _counter = 0
