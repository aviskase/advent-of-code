import pytest

from .puzzle import find_row, find_column

data = [
    ('BFFFBBFRRR', 70, 7),
    ('FFFBBBFRRR', 14, 7),
    ('BBFFBBFRLL', 102, 4),
    ('FBFBBFFRLR', 44, 5),
]


@pytest.mark.parametrize('d, expected, _', data)
def test_find_row(d, expected, _):
    assert find_row(d) == expected


@pytest.mark.parametrize('d, _, expected', data)
def test_find_column(d, _, expected):
    assert find_column(d) == expected

