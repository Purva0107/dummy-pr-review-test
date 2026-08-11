import pytest

from app import collect_tags


def test_collect_tags_does_not_leak_across_calls():
    first = collect_tags("a")
    second = collect_tags("b")
    assert first == ["a"]
    assert second == ["b"]
