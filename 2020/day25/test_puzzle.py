import pytest

from .puzzle import find_loop_size, calculate_key

card = 5764801
door = 17807724


@pytest.mark.parametrize('key, loop', [(card, 8), (door, 11)])
def test_find_loop_size(key, loop):
    assert find_loop_size(key) == loop


@pytest.mark.parametrize('key, loop', [(card, 11), (door, 8)])
def test_calculate_key(key, loop):
    assert calculate_key(key, loop) == 14897079
