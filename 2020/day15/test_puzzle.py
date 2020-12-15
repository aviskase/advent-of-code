import pytest

from .puzzle import num_at_round


@pytest.mark.parametrize('d, expected', [
    ([0, 3, 6], 436),
    ([1, 3, 2], 1),
    ([2, 1, 3], 10),
    ([1, 2, 3], 27),
    ([2, 3, 1], 78),
    ([3, 2, 1], 438),
    ([3, 1, 2], 1836),
])
def test_num_at_round(d, expected):
    assert num_at_round(d, 2020) == expected
