import string
from collections import deque
from dataclasses import dataclass
from typing import Deque, Union, List, Tuple


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
    entry: Point
    entries: List[Point]
    keys: List[Union[Tuple[int, int], None]]

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

    def transform(self):
        del self.maze[(self.entry.x, self.entry.y)]
        for d in range(4):
            del self.maze[step(self.entry.x, self.entry.y, d)]

        keys_by_quadrant = [0, 0, 0, 0]
        for i in range(self.nkeys):
            kx, ky = self.keys[i]
            idx = (2 if ky > self.entry.y else 0) | (1 if kx > self.entry.x else 0)
            keys_by_quadrant[idx] |= (1 << i)

        all_keys = (1 << self.nkeys) - 1
        initial_keys = [all_keys ^ k for k in keys_by_quadrant]

        self.entries = [
            Point(*step(*step(self.entry.x, self.entry.y, 0), 2), initial_keys[0]),
            Point(*step(*step(self.entry.x, self.entry.y, 0), 3), initial_keys[1]),
            Point(*step(*step(self.entry.x, self.entry.y, 1), 2), initial_keys[2]),
            Point(*step(*step(self.entry.x, self.entry.y, 1), 3), initial_keys[3])
        ]
        for entry in self.entries:
            self.maze[(entry.x, entry.y)] = '@'


def step(x, y, direction):
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    return x + directions_x[direction], y + directions_y[direction]


def bfs(maze: Maze, entrance=None):
    state = {}
    queue: Deque[QueueNode] = deque()
    if not entrance:
        entrance = maze.entry
    queue.append(QueueNode(entrance, 0))
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
        maze = Maze(lines)
        result = bfs(maze)
        print('Print 1:', result)
        maze.transform()
        shortest = sum(bfs(maze, maze.entries[i]) for i in range(4))
        print('Print 2:', shortest)


if __name__ == '__main__':
    solver()
