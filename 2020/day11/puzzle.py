from copy import deepcopy
from itertools import product
from typing import List

from more_itertools import flatten

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


def simulate(seats: TSeats, max_rounds=None) -> TSeats:
    cur_round = 0
    change_count = 999
    cur_seats = add_border(seats)
    max_rows = len(cur_seats)-1
    max_seats = len(cur_seats[0])-1
    while cur_round != max_rounds and change_count > 0:
        change_count = 0
        next_seats = deepcopy(cur_seats)
        for i, j in product(range(1, max_rows), range(1, max_seats)):
            seat = cur_seats[i][j]
            neighbours = [
                cur_seats[i-1][j-1], cur_seats[i-1][j], cur_seats[i-1][j+1],
                cur_seats[i][j-1], cur_seats[i][j+1],
                cur_seats[i+1][j-1], cur_seats[i+1][j], cur_seats[i+1][j+1],
            ]
            if seat == EMPTY and neighbours.count(OCCUPIED) == 0:
                next_seats[i][j] = OCCUPIED
                change_count += 1
            elif seat == OCCUPIED and neighbours.count(OCCUPIED) >= 4:
                next_seats[i][j] = EMPTY
                change_count += 1
        cur_round += 1
        cur_seats = next_seats
    return remove_border(cur_seats)


def solver():
    with open('input.txt', 'r') as f:
        seats = [list(x) for x in f.read().strip().splitlines()]
        end_state = simulate(seats)
        print('Part 1:', list(flatten(end_state)).count(OCCUPIED))  # 2277
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
