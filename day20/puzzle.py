import string
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum, auto
from queue import PriorityQueue
from typing import Dict, Deque, List


class DoorType(Enum):
    OUT = auto()
    IN = auto()
    EXIT = auto()


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class Node:
    point: Point
    steps: int
    door_type: DoorType


class Maze:
    entry: Point
    exit: Point
    tiles: Dict[Point, Dict[str, List[Node]]]
    width: int
    height: int

    def __init__(self, lines):
        self.tiles = {}
        self.height = len(lines)
        self.width = len(max(lines, key=len).strip('\n'))
        raw_data = [[' '] * self.width for y in range(self.height)]
        for y, row in enumerate(lines):
            for x, ch in enumerate(row.strip('\n')):
                raw_data[y][x] = ch
                if ch == '.':
                    self.tiles[Point(x, y)] = {'nodes': []}

        to_skip = set()
        doors = defaultdict(set)
        for y, row in enumerate(raw_data):
            for x, ch in enumerate(row):
                if (x, y) in to_skip:
                    continue
                if ch in string.ascii_uppercase:
                    point = None
                    if y+1 < self.height and raw_data[y+1][x] in string.ascii_uppercase:
                        to_skip.add((x, y+1))
                        door = ch + raw_data[y+1][x]
                        if y+2 < self.height and raw_data[y+2][x] == '.':
                            point = Point(x, y+2)
                        elif raw_data[y-1][x] == '.':
                            point = Point(x, y-1)
                    else:
                        if raw_data[y][x+1] not in string.ascii_uppercase:
                            raise ValueError('No doors found', x, y)
                        to_skip.add((x+1, y))
                        door = ch + raw_data[y][x+1]
                        if x+2 < self.width and raw_data[y][x+2] == '.':
                            point = Point(x+2, y)
                        elif raw_data[y][x-1] == '.':
                            point = Point(x-1, y)
                    doors[door].add(point)

        self.entry = doors['AA'].pop()
        del doors['AA']
        self.exit = doors['ZZ'].pop()
        del doors['ZZ']
        self.transfers = {}
        for points in doors.values():
            p1 = points.pop()
            p2 = points.pop()
            self.transfers[p1] = p2
            self.transfers[p2] = p1

        build_graph(self)

    def door_type(self, p: Point):
        if p == self.exit:
            return DoorType.EXIT
        if p.x <= 4 or p.y <= 4:
            return DoorType.OUT
        if p.x >= self.width - 4 or p.y >= self.height - 4:
            return DoorType.OUT
        return DoorType.IN


def step(x, y, direction):
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    return x + directions_x[direction], y + directions_y[direction]


def bfs_nodes(maze: Maze, entry: Point):
    visited = [entry]
    queue: Deque[QueueNode] = deque()
    queue.append(QueueNode(0, entry))

    while queue:
        node = queue.popleft()
        not_moved = True
        for i in range(4):
            x, y = step(node.point.x, node.point.y, i)
            new_point = Point(x, y)
            if new_point == maze.exit:
                maze.tiles[entry]['nodes'].append(Node(
                    new_point,
                    node.distance+1,
                    maze.door_type(new_point)
                ))
                continue
            if new_point not in visited and new_point in maze.tiles.keys():
                not_moved = False
                visited.append(new_point)
                queue.append(QueueNode(node.distance + 1, new_point))
        if not_moved and node.point in maze.transfers:
            maze.tiles[entry]['nodes'].append(Node(
                maze.transfers[node.point],
                node.distance+1,
                maze.door_type(node.point)
            ))


def build_graph(maze: Maze):
    for entry in maze.transfers:
        if entry != maze.exit:
            bfs_nodes(maze, entry)
    bfs_nodes(maze, maze.entry)


@dataclass(order=True)
class QueueNode:
    distance: int
    point: Point = field(compare=False)
    level: int = field(default=0, compare=False)


def bfs_on_graph(maze: Maze):
    queue: PriorityQueue[QueueNode] = PriorityQueue()
    queue.put(QueueNode(0, maze.entry))
    while queue:
        node = queue.get()
        if node.point == maze.exit:
            return node.distance
        for next_node in maze.tiles[node.point]['nodes']:
            queue.put(QueueNode(node.distance + next_node.steps, next_node.point))
    return -1


def bfs_on_graph_with_levels(maze: Maze):
    queue: PriorityQueue[QueueNode] = PriorityQueue()
    queue.put(QueueNode(0, maze.entry, 0))
    while queue:
        node = queue.get()
        if node.point == maze.exit and node.level == 0:
            return node.distance
        for next_node in maze.tiles[node.point]['nodes']:
            if next_node.door_type == DoorType.OUT:
                if node.level != 0:
                    queue.put(QueueNode(
                        node.distance + next_node.steps,
                        next_node.point,
                        node.level - 1
                    ))
            elif next_node.door_type == DoorType.IN:
                queue.put(QueueNode(
                    node.distance + next_node.steps,
                    next_node.point,
                    node.level + 1
                ))
            elif next_node.door_type == DoorType.EXIT and node.level == 0:
                return node.distance + next_node.steps
    return -1


def solver():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        maze = Maze(lines)
        print('Part 1:', bfs_on_graph(maze))
        print('Part 2:', bfs_on_graph_with_levels(maze))


if __name__ == '__main__':
    solver()
