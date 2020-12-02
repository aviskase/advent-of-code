from __future__ import annotations

import itertools
from functools import reduce
from math import gcd


def lcm(a, b):
    return int(a * b / gcd(a, b))


def lcms(*numbers):
    return reduce(lcm, numbers)


class Moon:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.velocity_x = vx
        self.velocity_y = vy
        self.velocity_z = vz

    def __repr__(self):
        return f'{self.x:4} {self.y:4} {self.z:4} | {self.velocity_x:4} {self.velocity_z:4} {self.velocity_y:4}'

    @property
    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    @property
    def kinetic_energy(self):
        return abs(self.velocity_x) + abs(self.velocity_y) + abs(self.velocity_z)

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.z += self.velocity_z

    @staticmethod
    def gravitate(moon_one: Moon, moon_two: Moon):
        if moon_one.x > moon_two.x:
            moon_one.velocity_x -= 1
            moon_two.velocity_x += 1
        if moon_one.x < moon_two.x:
            moon_one.velocity_x += 1
            moon_two.velocity_x -= 1
        if moon_one.y > moon_two.y:
            moon_one.velocity_y -= 1
            moon_two.velocity_y += 1
        if moon_one.y < moon_two.y:
            moon_one.velocity_y += 1
            moon_two.velocity_y -= 1
        if moon_one.z > moon_two.z:
            moon_one.velocity_z -= 1
            moon_two.velocity_z += 1
        if moon_one.z < moon_two.z:
            moon_one.velocity_z += 1
            moon_two.velocity_z -= 1


def time_step(moons):
    for m1, m2 in itertools.combinations(moons, 2):
        Moon.gravitate(m1, m2)
    for moon in moons:
        moon.move()


def simulator(moons, iterations):
    for i in range(iterations):
        time_step(moons)
    return sum(moon.total_energy for moon in moons)


def perioder(index, coordinate, patterns, moon_coordinate):
    patterns[index][coordinate]['path'].append(moon_coordinate)
    s = patterns[index][coordinate]['start']
    if s != -1:
        n = patterns[index][coordinate]['next']
        if moon_coordinate == patterns[index][coordinate]['path'][n]:
            patterns[index][coordinate]['next'] += 1
            if patterns[index][coordinate]['next'] == patterns[index][coordinate]['start']:
                patterns[index][coordinate]['period'] = patterns[index][coordinate]['start']
            return
        else:
            patterns[index][coordinate]['start'] = -1
            patterns[index][coordinate]['next'] = -1
    if moon_coordinate == patterns[index][coordinate]['path'][0]:
        patterns[index][coordinate]['start'] = len(patterns[index][coordinate]['path']) - 1
        patterns[index][coordinate]['next'] = 1


def all_periods(patterns):
    periods = set()
    for moon in patterns:
        periods.add(moon['x']['period'])
        periods.add(moon['y']['period'])
        periods.add(moon['z']['period'])
    return periods


def find_old_new_state(moons):
    step = 1
    patterns = [
        {
            'x': {'start': -1, 'path': [moon.x], 'next': -1, 'period': None},
            'y': {'start': -1, 'path': [moon.y], 'next': -1, 'period': None},
            'z': {'start': -1, 'path': [moon.z], 'next': -1, 'period': None},
        }
        for moon in moons
    ]
    while True:
        time_step(moons)
        for i, moon in enumerate(moons):
            if patterns[i]['x']['period'] is None:
                perioder(i, 'x', patterns, moon.x)
            if patterns[i]['y']['period'] is None:
                perioder(i, 'y', patterns, moon.y)
            if patterns[i]['z']['period'] is None:
                perioder(i, 'z', patterns, moon.z)
            periods = all_periods(patterns)
            if None not in periods:
                return lcms(*periods)


def solver():
    moons = [
        (-7, 17, -11),
        (9, 12, 5),
        (-9, 0, -4),
        (4, 6, 0)
    ]
    print('Part 1:', simulator([Moon(*m) for m in moons], 1000))
    print('Part 2:', find_old_new_state([Moon(*m) for m in moons]))


if __name__ == '__main__':
    solver()
