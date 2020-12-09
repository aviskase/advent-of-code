from itertools import combinations
from typing import List, Tuple


def find_first_invalid(numbers: List[int], preamble=25) -> int:
    start = 0
    for num in numbers[preamble:]:
        if all(sum(c) != num for c in combinations(numbers[start:start+preamble], 2)):
            return num
        start += 1


def find_range_for_invalid(numbers: List[int], invalid) -> Tuple[int, int]:
    for i in range(len(numbers)):
        for j in range(2, len(numbers)):
            if invalid == sum(numbers[i:j]):
                return min(numbers[i:j]), max(numbers[i:j])


def solver():
    with open('input.txt', 'r') as f:
        numbers = [int(x) for x in f.read().strip().splitlines()]
        invalid = find_first_invalid(numbers)
        print('Part 1:', invalid)  # 23278925
        print('Part 2:', sum(find_range_for_invalid(numbers, invalid)))  # 4011064


if __name__ == '__main__':
    solver()
