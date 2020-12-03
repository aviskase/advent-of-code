import pytest

from .puzzle import find_trees, map_trees

data = [
    '..##.......',
    '#...#...#..',
    '.#....#..#.',
    '..#.#...#.#',
    '.#...##..#.',
    '..#.##.....',
    '.#.#.#....#',
    '.#........#',
    '#.##...#...',
    '#...##....#',
    '.#..#...#.#'
]


@pytest.mark.parametrize('down, right, expected', [(1, 1, 2), (1, 3, 7), (1, 5, 3), (1, 7, 4), (2, 1, 2)])
def test_find_trees(down, right, expected):
    assert find_trees(map_trees(data), down, right) == expected

