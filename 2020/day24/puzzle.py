from __future__ import annotations

from enum import Enum
from typing import List, Dict, Tuple

from more_itertools import quantify

TCoordinates = Tuple[int, int]
TFloor = Dict[TCoordinates, bool]


def get_neighbor(coordinates: TCoordinates, direction: Direction) -> TCoordinates:
    return coordinates[0] + direction.value[0], coordinates[1] + direction.value[1]


def all_neighbors(coordinates: TCoordinates):
    return [get_neighbor(coordinates, d) for d in Direction]


def add_neighbors(floor: TFloor) -> TFloor:
    new_floor = floor.copy()
    for tile in floor:
        new_floor.update({n: False for n in all_neighbors(tile) if n not in floor})
    return new_floor


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


def flip(start_floor: TFloor, days=100) -> TFloor:
    current_floor = start_floor
    for _ in range(days):
        current_floor = add_neighbors(current_floor)
        next_floor = current_floor.copy()
        for tile, is_black in current_floor.items():
            black_neighbors = quantify(current_floor[n] for n in all_neighbors(tile) if n in current_floor)
            if is_black and black_neighbors not in [1, 2]:
                next_floor[tile] = False
            elif not is_black and black_neighbors == 2:
                next_floor[tile] = True
        current_floor = next_floor
    return current_floor


def solver():
    with open('input.txt', 'r') as f:
        raw_data = f.read().strip().splitlines()
        data = [parse_tile(d) for d in raw_data]
        init_state = paint_it_black(data)
        print('Part 1:', count_blacks(init_state))  # 450
        print('Part 2:', count_blacks(flip(init_state)))  # 4059


if __name__ == '__main__':
    solver()
