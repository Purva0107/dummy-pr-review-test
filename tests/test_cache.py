import threading

from cache import bump, get_count, reset


def test_bump_is_monotonic_under_concurrency():
    reset()
    threads = [threading.Thread(target=bump) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert get_count() == 50
