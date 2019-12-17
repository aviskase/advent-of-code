from itertools import islice, cycle, repeat
from operator import mul

BASE_PATTERN = [0, 1, 0, -1]


def get_pattern(position):
    return islice(
        cycle(
            r
            for item in BASE_PATTERN
            for r in repeat(item, position)
        ),
        1, None
    )


def to_signal(line):
    return list(map(int, line.strip()))


def new_digit(signal, position):
    result = sum(map(mul, signal, get_pattern(position)))
    return abs(result) % 10


def phase(signal):
    return [
        new_digit(signal, position)
        for position in range(1, len(signal) + 1)
    ]


def cycle_phases(signal, phases):
    for p in range(phases):
        signal = phase(signal)
    return signal


def signal_to_str(signal):
    return ''.join(map(str, signal))


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        signal = to_signal(line)
        part_1 = cycle_phases(signal, 100)
        print('Part 1:', signal_to_str(part_1[:8]))


if __name__ == '__main__':
    solver()
