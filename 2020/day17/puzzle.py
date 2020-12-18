from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from typing import Dict

from more_itertools import quantify


@dataclass(unsafe_hash=True)
class Point:
    x: int
    y: int
    z: int
    w: int = 0


INACTIVE = '.'
ACTIVE = '#'
TCube = Dict[Point, str]


def point_area3d(point: Point):
    return map(lambda p: Point(*p), product(
        [point.x-1, point.x, point.x+1],
        [point.y-1, point.y, point.y+1],
        [point.z-1, point.z, point.z+1]
    ))


def point_area4d(point: Point):
    return map(lambda p: Point(*p), product(
        [point.x-1, point.x, point.x+1],
        [point.y-1, point.y, point.y+1],
        [point.z-1, point.z, point.z+1],
        [point.w-1, point.w, point.w+1]
    ))


def direct_neighbours(cube: TCube, point: Point, point_area_fn=point_area3d):
    return [cube[p] for p in point_area_fn(point) if p != point and p in cube]


def make_cube(raw_data: str) -> TCube:
    return {Point(x, y, 0): value for y, row in enumerate(raw_data.split()) for x, value in enumerate(row)}


def envelope(cube: TCube, point_area_fn=point_area3d) -> TCube:
    enveloped = deepcopy(cube)
    for point in cube:
        for p in point_area_fn(point):
            if p not in cube:
                enveloped[p] = INACTIVE
    return enveloped


def simulate(cube: TCube, max_rounds, point_area_fn=point_area3d) -> TCube:
    cur_round = 0
    cur_state = cube
    while cur_round != max_rounds:
        cur_state = envelope(cur_state, point_area_fn)
        next_state = deepcopy(cur_state)
        for point, state in cur_state.items():
            neighbors = direct_neighbours(cur_state, point, point_area_fn)
            if state == ACTIVE and neighbors.count(ACTIVE) not in [2, 3]:
                next_state[point] = INACTIVE
            elif state == INACTIVE and neighbors.count(ACTIVE) == 3:
                next_state[point] = ACTIVE
        cur_round += 1
        cur_state = next_state
    return cur_state


def count_active(cube: TCube) -> int:
    return quantify(cube.values(), lambda x: x == ACTIVE)


def solver():
    with open('input.txt', 'r') as f:
        cube = make_cube(f.read().strip())
        print('Part 1:', count_active(simulate(cube, 6)))  # 293
        print('Part 2:', count_active(simulate(cube, 6, point_area4d)))  # 1816


if __name__ == '__main__':
    solver()
