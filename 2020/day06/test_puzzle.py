import pytest

from .puzzle import count_any_yes, count_all_yes


@pytest.mark.parametrize('data, expected', [
    ('abc', 3),
    ('a\nb\nc', 3),
    ('ab\nac', 3),
    ('a\na\na\na', 1),
    ('b', 1),
])
def test_count_any_yes(data, expected):
    assert count_any_yes(data) == expected


@pytest.mark.parametrize('data, expected', [
    ('abc', 3),
    ('a\nb\nc', 0),
    ('ab\nac', 1),
    ('a\na\na\na', 1),
    ('b', 1),
])
def test_count_all_yes(data, expected):
    assert count_all_yes(data) == expected
