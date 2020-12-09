from itertools import combinations
from typing import List


def find_first_invalid(numbers: List[int], preamble=25) -> int:
    start = 0
    for num in numbers[preamble:]:
        if all(sum(c) != num for c in combinations(numbers[start:start+preamble], 2)):
            return num
        start += 1


def solver():
    with open('input.txt', 'r') as f:
        numbers = [int(x) for x in f.read().strip().splitlines()]
        print('Part 1:', find_first_invalid(numbers))  # 23278925
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
