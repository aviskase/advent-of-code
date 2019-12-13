from __future__ import annotations

import itertools


class Moon:
    def __init__(self, x, y, z, vx=0, vy=0, vz=0):
        self.x = x
        self.y = y
        self.z = z
        self.velocity_x = vx
        self.velocity_y = vy
        self.velocity_z = vz

    def __repr__(self):
        return f'{self.x} {self.y} {self.z} | {self.velocity_x} {self.velocity_z} {self.velocity_y}'

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


def simulator(moons, iterations):
    for i in range(iterations):
        for m1, m2 in itertools.combinations(moons, 2):
            Moon.gravitate(m1, m2)
        for moon in moons:
            moon.move()
    return sum(moon.total_energy for moon in moons)


def solver():
    moons = [
        Moon(-7, 17, -11),
        Moon(9, 12, 5),
        Moon(-9, 0, -4),
        Moon(4, 6, 0)
    ]
    print('Part 1:', simulator(moons, 1000))


if __name__ == '__main__':
    solver()
