import pytest

from .puzzle import find_bus, find_timestamp

timestamp = 939
buses = '7,13,x,x,59,x,31,19'.split(',')


def test_find_bus():
    assert find_bus(timestamp, buses) == (59, 5)


@pytest.mark.parametrize('b, expected', [
    (buses, 1068781),
    ('17,x,13,19'.split(','), 3417),
    ('67,7,59,61'.split(','), 754018),
    ('67,x,7,59,61'.split(','), 779210),
    ('67,7,x,59,61'.split(','), 1261476),
    ('1789,37,47,1889'.split(','), 1202161486),
])
def test_find_timestamp(b, expected):
    assert find_timestamp(b) == expected
