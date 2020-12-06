import pytest

from .puzzle import count_yes


@pytest.mark.parametrize('data, expected', [
    ('abc', 3),
    ('a\nb\nc', 3),
    ('ab\nac', 3),
    ('a\na\na\na', 1),
    ('b', 1),
])
def test_count_yes(data, expected):
    assert count_yes(data) == expected
