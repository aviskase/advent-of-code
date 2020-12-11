from copy import deepcopy
from itertools import product
from typing import List

from more_itertools import flatten, first_true, quantify

FLOOR = '.'
OCCUPIED = '#'
EMPTY = 'L'

TSeats = List[List[str]]


def add_border(seats: TSeats) -> TSeats:
    new_seats = [[FLOOR, *s, FLOOR] for s in seats]
    row = list(FLOOR * len(new_seats[0]))
    return [row, *new_seats, row]


def remove_border(seats: TSeats) -> TSeats:
    return [s[1:-1] for s in seats[1:-1]]


def direct_neighbours(seats, i, j):
    return [
        seats[i-1][j-1], seats[i-1][j], seats[i-1][j+1],
        seats[i][j-1], seats[i][j+1],
        seats[i+1][j-1], seats[i+1][j], seats[i+1][j+1],
    ]


def all_visible(seats, i, j):
    def not_floor(x): return x != FLOOR
    max_rows = len(seats)
    max_cols = len(seats[0])
    return [
        first_true(seats[i][j-1::-1], FLOOR, not_floor),  # ←
        first_true(seats[i][j+1:], FLOOR, not_floor),  # →
        first_true((seats[k][j] for k in range(i-1, -1, -1)), FLOOR, not_floor),  # ↑
        first_true((seats[k][j] for k in range(i+1, max_rows)), FLOOR, not_floor),  # ↓

        first_true((seats[k][l] for k, l in zip(range(i-1, -1, -1), range(j-1, -1, -1))), FLOOR, not_floor),  # ↖
        first_true((seats[k][l] for k, l in zip(range(i+1, max_rows), range(j-1, -1, -1))), FLOOR, not_floor),  # ↙
        first_true((seats[k][l] for k, l in zip(range(i-1, -1, -1), range(j+1, max_cols))), FLOOR, not_floor),  # ↗
        first_true((seats[k][l] for k, l in zip(range(i+1, max_rows), range(j+1, max_cols))), FLOOR, not_floor),  # ↘
    ]


def simulate(seats: TSeats, max_rounds=None, occupied_threshold=4, neighbours_fn=direct_neighbours) -> TSeats:
    cur_round = 0
    with_changes = True
    cur_seats = add_border(seats)
    max_rows = len(cur_seats)-1
    max_cols = len(cur_seats[0])-1
    while cur_round != max_rounds and with_changes:
        with_changes = False
        next_seats = deepcopy(cur_seats)
        for i, j in product(range(1, max_rows), range(1, max_cols)):
            seat = cur_seats[i][j]
            neighbours = neighbours_fn(cur_seats, i, j)
            if seat == EMPTY and neighbours.count(OCCUPIED) == 0:
                next_seats[i][j] = OCCUPIED
                with_changes = True
            elif seat == OCCUPIED and neighbours.count(OCCUPIED) >= occupied_threshold:
                next_seats[i][j] = EMPTY
                with_changes = True
        cur_round += 1
        cur_seats = next_seats
    return remove_border(cur_seats)


def solver():
    with open('input.txt', 'r') as f:
        seats = [list(x) for x in f.read().strip().splitlines()]
        end_state = simulate(seats)
        print('Part 1:', quantify(flatten(end_state), lambda x: x == OCCUPIED))  # 2277
        end_state = simulate(seats, occupied_threshold=5, neighbours_fn=all_visible)
        print('Part 1:', quantify(flatten(end_state), lambda x: x == OCCUPIED))  # 2066


if __name__ == '__main__':
    solver()
