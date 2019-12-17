import pytest
from itertools import islice
from day16.puzzle import to_signal, get_pattern, phase, cycle_phases


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
