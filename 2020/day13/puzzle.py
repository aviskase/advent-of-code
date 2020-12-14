import math
from operator import mul
from typing import List


def find_bus(timestamp: int, all_buses: List[str]) -> (int, int):
    buses = [int(b) for b in all_buses if b != 'x']
    exact = next((b for b in buses if timestamp % b == 0), None)
    if exact:
        return exact, 0
    arrival, bus = min(((timestamp - (timestamp % b) + b, b) for b in buses), key=lambda k: k[0])
    return bus, arrival - timestamp


def find_timestamp(all_buses: List[str]) -> int:
    buses = [int(b) for b in all_buses if b != 'x']
    remainders = [int(b)-i for i, b in enumerate(all_buses) if b != 'x']
    total_prod = math.prod(buses)
    prod = [total_prod // b for b in buses]
    total = sum(r * p * inv(p, b) for r, p, b in zip(remainders, prod, buses))
    return total % total_prod


def inv(a, b):
    # a * x = 1 (mod b)
    # simplify
    simplified_a = a % b
    # aa * x = 1 (mod b)
    x = 1
    while True:
        if (simplified_a * x) % b == 1:
            return x
        x += 1


def solver():
    with open('input.txt', 'r') as f:
        timestamp = int(f.readline().strip())
        buses = f.readline().strip().split(',')
        print('Part 1:', mul(*find_bus(timestamp, buses)))  # 2845
        print('Part 2:', find_timestamp(buses))  # 487905974205117


if __name__ == '__main__':
    solver()
