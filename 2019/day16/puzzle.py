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
    return list(map(int, line))


def new_digit(signal, position):
    result = sum(map(mul, signal, get_pattern(position)))
    return abs(result) % 10


def phase(signal):
    middle = len(signal) // 2
    new_signal = track_head(signal, middle + 1)
    new_signal.extend(track_tail(signal, middle - 1))
    return new_signal


def track_head(signal, end):
    return [
        new_digit(signal, position)
        for position in range(1, end)
    ]


def track_tail(signal, start):
    return [
        sum(signal[:position:-1]) % 10
        for position in range(start, len(signal) - 1)
    ]


def cycle_phases(signal, phases):
    for p in range(phases):
        signal = phase(signal)
    return signal


def signal_to_str(signal):
    return ''.join(map(str, signal))


def get_message(signal, phases):
    offset = int(signal_to_str(signal[:7]))
    middle = len(signal) // 2
    if offset >= middle:
        signal_tail = signal[offset:]
        for _ in range(phases):
            for i in range(len(signal_tail)-1, 0, -1):
                signal_tail[i-1] = (signal_tail[i-1] + signal_tail[i]) % 10
        return signal_tail[:8]
    raise ValueError('Not optimized to calculate')


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline().strip()
        signal = to_signal(line)
        part_1 = cycle_phases(signal, 100)
        print('Part 1:', signal_to_str(part_1[:8]))
        real_signal = to_signal(line * 10000)
        part_2 = get_message(real_signal, 100)
        print('Part 2:', signal_to_str(part_2))


if __name__ == '__main__':
    solver()
