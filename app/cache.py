"""Simple in-process counter — intentionally racy on test branch."""

_counter = 0


def bump() -> int:
    """Increment and return the counter."""
    global _counter
    current = _counter
    # Simulates work between read and write (lost updates under concurrency).
    _counter = current + 1
    return _counter


def get_count() -> int:
    return _counter


def reset() -> None:
    global _counter
    _counter = 0
