import pytest

from .puzzle import convert_to_layers, num_of_x, find_with_smallest_zeros, combine_layers


def test_convert_to_layers():
    assert convert_to_layers('123456789012', 3, 2) == [[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [0, 1, 2]]]


@pytest.mark.parametrize('layer,num', [
    ([[1, 2, 3], [4, 5, 6]], 0),
    ([[7, 8, 9], [0, 1, 2]], 1),
    ([[7, 8, 0], [0, 1, 2]], 2),
])
def test_num_of_zeros(layer, num):
    assert num_of_x(layer) == num


def test_find_smallest():
    layers = [[[1, 2, 3], [0, 0, 6]], [[7, 8, 9], [0, 1, 2]]]
    assert find_with_smallest_zeros(layers) == [[7, 8, 9], [0, 1, 2]]


def test_combine():
    data = convert_to_layers('0222112222120000', 2, 2)
    assert combine_layers(data, 2, 2) == [[0, 1], [1, 0]]
