from itertools import islice

import pytest

from .puzzle import to_signal, get_pattern, phase, cycle_phases, get_message


def test_to_signal():
    assert to_signal('1234') == [1, 2, 3, 4]


@pytest.mark.parametrize('position, output', [
    (1, [1, 0, -1, 0, 1, 0, -1, 0]),
    (2, [0, 1, 1, 0, 0, -1, -1, 0]),
    (3, [0, 0, 1, 1, 1, 0, 0, 0]),
    (4, [0, 0, 0, 1, 1, 1, 1, 0]),
    (5, [0, 0, 0, 0, 1, 1, 1, 1]),
    (6, [0, 0, 0, 0, 0, 1, 1, 1]),
    (7, [0, 0, 0, 0, 0, 0, 1, 1]),
    (8, [0, 0, 0, 0, 0, 0, 0, 1]),
])
def test_pattern(position, output):
    assert list(islice(get_pattern(position), 8)) == output


def test_phase():
    assert phase(to_signal('12345678')) == to_signal('48226158')


@pytest.mark.parametrize('signal, p, output', [
    ('12345678', 4, '01029498'),
    ('80871224585914546619083218645595', 100, '24176176'),
    ('19617804207202209144916044189917', 100, '73745418'),
    ('69317163492948606335995924319873', 100, '52432133'),
])
def test_phases(signal, p, output):
    assert cycle_phases(to_signal(signal), p)[:8] == to_signal(output)


@pytest.mark.parametrize('signal, message', [
    ('03036732577212944063491565474664', '84462026'),
    ('02935109699940807407585447034323', '78725270'),
    ('03081770884921959731165446850517', '53553731'),
])
def test_get_message(signal, message):
    signal = to_signal(signal * 10000)
    assert get_message(signal, 100) == to_signal(message)
