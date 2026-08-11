from app import username_length


def test_username_length_handles_none():
    assert username_length(None) == 0


def test_username_length_present():
    assert username_length({"username": "ada"}) == 3
