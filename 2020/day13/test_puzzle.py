from .puzzle import find_bus


timestamp = 939
buses = '7,13,x,x,59,x,31,19'.split(',')


def test_find_bus():
    assert find_bus(timestamp, buses) == (59, 5)
