import string
from collections import deque
from dataclasses import dataclass
from typing import Deque


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int
    keys: int


@dataclass(eq=True, frozen=True)
class QueueNode:
    point: Point
    distance: int


def keyidx(ch) -> int:
    return ord(ch) - ord('a')


def keybit(ch):
    return 1 << keyidx(ch)


def dooridx(ch):
    if ch in string.ascii_uppercase:
        return ord(ch) - ord('A')


def doorbit(ch):
    return 1 << dooridx(ch)


def has_key(keys, door):
    return (keys & doorbit(door)) != 0


class Maze:
    def __init__(self, lines):
        self.maze = {}
        self.keys = [None] * 26
        self.nkeys = 0
        for y, line in enumerate(lines):
            for x, element in enumerate(line.strip()):
                if element != '#':
                    self.maze[(x, y)] = element
                if element == '@':
                    self.entry = Point(x, y, 0)
                elif element in string.ascii_lowercase:
                    self.keys[keyidx(element)] = (x, y)
                    self.nkeys += 1


def step(x, y, direction):
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    return x + directions_x[direction], y + directions_y[direction]


def bfs(maze: Maze):
    state = {}
    queue: Deque[QueueNode] = deque()
    queue.append(QueueNode(maze.entry, 0))
    all_keys = (1 << maze.nkeys) - 1
    while queue:
        node = queue.popleft()
        keys = node.point.keys
        maze_point = maze.maze.get((node.point.x, node.point.y))
        if maze_point in string.ascii_lowercase:
            keys = node.point.keys | keybit(maze_point)
            if keys == all_keys:
                return node.distance
        if maze_point in string.ascii_uppercase and not has_key(node.point.keys, maze_point):
            continue
        point = Point(node.point.x, node.point.y, keys)
        state_distance = state.get(point, 100000)
        if node.distance >= state_distance:
            continue
        state[point] = node.distance
        queue.extend(
            QueueNode(Point(*step(point.x, point.y, d), point.keys), node.distance+1)
            for d in range(4)
            if step(point.x, point.y, d) in maze.maze
        )
    return -1


def solver():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        result = bfs(Maze(lines))
        print('Print 1:', result)


if __name__ == '__main__':
    solver()
