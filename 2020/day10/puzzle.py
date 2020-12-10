from collections import Counter
from itertools import starmap
from typing import List

from more_itertools import pairwise


def find_differences(adapters: List[int]) -> Counter:
    sorted_adapters = [0] + sorted(adapters)
    diffs = Counter(starmap(lambda a, b: b - a, pairwise(sorted_adapters)))
    diffs.update([3])  # always add device adapter
    return diffs


def solver():
    with open('input.txt', 'r') as f:
        adapters = [int(x) for x in f.read().strip().splitlines()]
        diff = find_differences(adapters)
        print('Part 1:', diff.get(1) * diff.get(3))  # 2760
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
