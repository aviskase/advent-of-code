from __future__ import annotations

from enum import Enum
from typing import List, Dict, Tuple

from more_itertools import quantify

TCoordinates = Tuple[int, int]
TFloor = Dict[TCoordinates, bool]


def get_neighbor(coordinates: TCoordinates, direction: Direction) -> TCoordinates:
    return coordinates[0] + direction.value[0], coordinates[1] + direction.value[1]


class Direction(Enum):
    NE: TCoordinates = (1, -1)
    E: TCoordinates = (1, 0)
    SE: TCoordinates = (0, 1)
    SW: TCoordinates = (-1, 1)
    W: TCoordinates = (-1, 0)
    NW: TCoordinates = (0, -1)


TInstruction = List[Direction]


def parse_tile(data: str) -> TInstruction:
    directions = []
    prev_token = None
    for token in data:
        if prev_token == 's':
            directions.append(Direction.SE if token == 'e' else Direction.SW)
        elif prev_token == 'n':
            directions.append(Direction.NE if token == 'e' else Direction.NW)
        elif token in ['e', 'w']:
            directions.append(Direction.E if token == 'e' else Direction.W)
        prev_token = token
    return directions


def count_blacks(floor: TFloor) -> int:
    return quantify(floor.values())


def paint_it_black(tiles: List[TInstruction]) -> TFloor:
    floor = {(0, 0): False}
    for tile in tiles:
        cur_tile = (0, 0)
        for i in tile:
            cur_tile = get_neighbor(cur_tile, i)
        floor[cur_tile] = not floor[cur_tile] if cur_tile in floor else True
    return floor


def solver():
    with open('input.txt', 'r') as f:
        raw_data = f.read().strip().splitlines()
        data = [parse_tile(d) for d in raw_data]
        print('Part 1:', count_blacks(paint_it_black(data)))  # 450
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
