from operator import mul
from typing import List


def find_bus(timestamp: int, all_buses: List[str]) -> (int, int):
    buses = [int(b) for b in all_buses if b != 'x']
    exact = next((b for b in buses if timestamp % b == 0), None)
    if exact:
        return exact, 0
    arrival, bus = min(((timestamp - (timestamp % b) + b, b) for b in buses), key=lambda k: k[0])
    return bus, arrival - timestamp


def solver():
    with open('input.txt', 'r') as f:
        timestamp = int(f.readline().strip())
        buses = f.readline().strip().split(',')
        print('Part 1:', mul(*find_bus(timestamp, buses)))  # 2845
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
