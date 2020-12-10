import functools
from collections import Counter
from itertools import starmap
from typing import List

from more_itertools import pairwise


def find_differences(adapters: List[int]) -> Counter:
    sorted_adapters = [0] + sorted(adapters)
    diffs = Counter(starmap(lambda a, b: b - a, pairwise(sorted_adapters)))
    diffs.update([3])  # always add device adapter
    return diffs


def count_arrangements(adapters: List[int]) -> int:
    all_adapters = [0] + sorted(adapters)
    all_adapters.append(all_adapters[-1] + 3)
    return traverse_arrangements(all_adapters)


def traverse_arrangements(adapters: List[int]):
    def valid_inc(pos, inc): return pos + inc < len(adapters) and adapters[pos+inc] - adapters[pos] <= 3

    @functools.lru_cache()
    def _traverse(pos):
        if adapters[pos] == adapters[-1]:
            return 1
        counter = 0
        if valid_inc(pos, 1):
            counter += _traverse(pos+1)
        if valid_inc(pos, 2):
            counter += _traverse(pos+2)
        if valid_inc(pos, 3):
            counter += _traverse(pos+3)
        return counter

    return _traverse(0)


def solver():
    with open('input.txt', 'r') as f:
        adapters = [int(x) for x in f.read().strip().splitlines()]
        diff = find_differences(adapters)
        print('Part 1:', diff.get(1) * diff.get(3))  # 2760
        print('Part 2:', count_arrangements(adapters))  # 13816758796288


if __name__ == '__main__':
    solver()
