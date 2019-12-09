from __future__ import annotations
from dataclasses import dataclass
from typing import List
from timeit import default_timer as timer


def distance_from_center(point) -> int:
    return abs(point[0]) + abs(point[1])


def find_fastest(intersections, a_sizes, b_sizes):
    return min(
        a_sizes[point] + b_sizes[point]
        for point in intersections
    )


def find_closest(intersections):
    return min(distance_from_center(point) for point in intersections)


def find_intersections(a, b):
    return a.intersection(b)


def instructions_to_coordinates(instructions):
    sizes = dict()
    size = 1
    coordinates = set()
    current = (0, 0)
    for direction, step in instructions:
        points = []
        if direction == 'L':
            points = [(current[0] - s, current[1]) for s in range(1, step + 1)]
        elif direction == 'R':
            points = [(current[0] + s, current[1]) for s in range(1, step + 1)]
        elif direction == 'U':
            points = [(current[0], current[1] + s) for s in range(1, step + 1)]
        elif direction == 'D':
            points = [(current[0], current[1] - s) for s in range(1, step + 1)]
        current = points[-1]
        coordinates.update(points)
        for point in points:
            sizes[point] = size
            size += 1
    return coordinates, sizes


def line_to_instruction(line: str):
    return [(instruction[0], int(instruction[1:])) for instruction in line.split(',')]


def solver():
    with open('input.txt', 'r') as f:
        start = timer()
        first, first_size = instructions_to_coordinates(line_to_instruction(f.readline()))
        end = timer()
        print('First done: ', end - start)
        start = timer()
        second, second_size = instructions_to_coordinates(line_to_instruction(f.readline()))
        end = timer()
        print('Second done: ', end - start)
        start = timer()
        intersections = find_intersections(first, second)
        end = timer()
        print('Intersections done: ', end - start)
        print('Closest distance:', find_closest(intersections))
        print('Fastest distance:', find_fastest(intersections, first_size, second_size))


if __name__ == '__main__':
    solver()
