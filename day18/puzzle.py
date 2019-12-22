import string
from collections import deque
from dataclasses import dataclass
from typing import Deque, Set


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int
    keys: Set[str]


@dataclass(eq=True, frozen=True)
class QueueNode:
    point: Point
    distance: int


class Maze:
    def __init__(self, lines):
        self.keys = set()
        self.doors = set()
        self.maze = {}
        for y, line in enumerate(lines):
            for x, element in enumerate(line):
                if element != '#':
                    self.maze[(x, y)] = element
                if element == '@':
                    self.entry = Point(x, y, frozenset())
                elif element in string.ascii_lowercase:
                    self.keys.add(element)
                elif element in string.ascii_uppercase:
                    self.doors.add(element)


def bfs(maze: Maze):
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    visited = [maze.entry]
    queue: Deque[QueueNode] = deque()
    queue.append(QueueNode(maze.entry, 0))
    distances = set()
    while queue:
        node = queue.popleft()
        for i in range(4):
            x = node.point.x + directions_x[i]
            y = node.point.y + directions_y[i]
            maze_point = maze.maze.get((x, y))
            if not maze_point:
                continue
            keys = set(node.point.keys)
            if maze_point in maze.keys:
                keys.add(maze_point)
            if keys == maze.keys:
                return node.distance + 1
            if maze_point in maze.doors and maze_point.lower() not in node.point.keys:
                continue
            point = Point(x, y, frozenset(keys))
            if point not in visited:
                visited.append(point)
                queue.append(QueueNode(point, node.distance + 1))
                distances.add(node.distance + 1)
    return max(distances)


def solver():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        result = bfs(Maze(lines))
        print('Print 1:', result)


if __name__ == '__main__':
    solver()
