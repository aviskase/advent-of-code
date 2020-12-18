from copy import deepcopy
from itertools import product
from typing import NamedTuple, Dict

from more_itertools import quantify

INACTIVE = '.'
ACTIVE = '#'
Point = NamedTuple('Point', [('x', int), ('y', int), ('z', int)])
TCube = Dict[Point, str]


def direct_neighbours(cube: TCube, point: Point):
    return [cube[p] for p in point_area(point) if p != point and p in cube]


def point_area(point: Point):
    return map(lambda p: Point(*p), product(
        [point.x-1, point.x, point.x+1],
        [point.y-1, point.y, point.y+1],
        [point.z-1, point.z, point.z+1]
    ))


def make_cube(raw_data: str, z=0) -> TCube:
    return {Point(x, y, z): value for y, row in enumerate(raw_data.split()) for x, value in enumerate(row)}


def envelope(cube: TCube) -> TCube:
    enveloped = deepcopy(cube)
    for point in cube:
        for p in point_area(point):
            if p not in cube:
                enveloped[p] = INACTIVE
    return enveloped


def simulate(cube: TCube, max_rounds=None) -> TCube:
    cur_round = 0
    with_changes = True
    cur_state = cube
    while cur_round != max_rounds and with_changes:
        with_changes = False
        cur_state = envelope(cur_state)
        next_state = deepcopy(cur_state)
        for point, state in cur_state.items():
            neighbors = direct_neighbours(cur_state, point)
            if state == ACTIVE and neighbors.count(ACTIVE) not in [2, 3]:
                next_state[point] = INACTIVE
                with_changes = True
            elif state == INACTIVE and neighbors.count(ACTIVE) == 3:
                next_state[point] = ACTIVE
                with_changes = True
        cur_round += 1
        cur_state = next_state
    return cur_state


def count_active(cube: TCube) -> int:
    return quantify(cube.values(), lambda x: x == ACTIVE)


def solver():
    with open('input.txt', 'r') as f:
        cube = make_cube(f.read().strip())
        end_state = simulate(cube, 6)
        print('Part 1:', count_active(end_state))  # 2277
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
