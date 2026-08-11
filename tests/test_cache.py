import threading

from app.cache import bump, get_count


def test_bump_under_load():
    threads = [threading.Thread(target=bump) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert get_count() == 20
