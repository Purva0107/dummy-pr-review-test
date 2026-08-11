from app import get_last_item


def test_get_last_item():
    assert get_last_item([10, 20, 30]) == 30
