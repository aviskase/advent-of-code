import pytest
from day10.puzzle import extract_coordinates, in_direct_sight, find_center, convert_to_relative_map, calculate_angles, sort_left_quadrant, sort_right_quadrant

BASE_MAP = [
    '.#..#',
    '.....',
    '#####',
    '....#',
    '...##',
]

BASE_COORDINATES = [
    (1, 0), (4, 0), (0, 2), (1, 2), (2, 2),
    (3, 2), (4, 2), (4, 3), (3, 4), (4, 4)
]


def test_extract_coordinates():
    assert extract_coordinates(BASE_MAP) == BASE_COORDINATES


@pytest.mark.parametrize('point, num', list(zip(BASE_COORDINATES, [7, 7, 6, 7, 7, 7, 5, 7, 8, 7])))
def test_in_direct_sight(point, num):
    assert len(in_direct_sight(point, BASE_COORDINATES)) == num


def test_find_center():
    assert find_center(BASE_COORDINATES) == (3, 4)


def test_maps():
    angles = calculate_angles(convert_to_relative_map((2, 2), BASE_COORDINATES))
    from pprint import pprint
    pprint(angles)
    pprint(sort_right_quadrant(angles))
    pprint(sort_left_quadrant(angles))
