import pytest
from day12.puzzle import Moon, simulator


@pytest.mark.parametrize('data, result', [
    ((2, 1, -3, -3, -2, 1), 36),
    ((1, 8, 0, -1, 1, 3), 45),
    ((3, -6, 1, 3, 2, -3), 80),
    ((2, 0, 4, 1, -1, -1), 18),
])
def test_energy(data, result):
    assert Moon(*data).total_energy == result


def test_gravitation():
    m1 = Moon(3, 0, 0)
    m2 = Moon(5, 0, 0)
    Moon.gravitate(m1, m2)
    assert m1.velocity_x == 1
    assert m2.velocity_x == -1


@pytest.mark.parametrize('moons, iters, energy', [
    ([Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)], 10, 179),
    ([Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)], 100, 1940),
])
def test_simulation(moons, iters, energy):
    assert simulator(moons, iters) == energy
