import string
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, Deque, Union


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class LevelPoint:
    x: int
    y: int
    level: int


class Maze:
    entry: Point
    exit: Point
    tiles: Dict[Point, Dict[str, Union[str, None, Point]]]
    width: int
    height: int

    def __init__(self, lines):
        raw_data = [list(line.strip('\n')) for line in lines]
        self.height = len(raw_data)
        self.width = len(raw_data[3])
        self.tiles = {
            Point(x, y): {'door': None}
            for y, r in enumerate(raw_data)
            for x, ch in enumerate(r)
            if ch == '.'
        }
        to_skip = set()
        doors = defaultdict(set)
        for y, row in enumerate(raw_data):
            for x, ch in enumerate(row):
                if (x, y) in to_skip:
                    continue
                if ch in string.ascii_uppercase:
                    if y+1 < self.height and x < len(raw_data[y+1]) and raw_data[y+1][x] in string.ascii_uppercase:
                        to_skip.add((x, y+1))
                        door = ch + raw_data[y+1][x]
                        if y+2 < self.height and raw_data[y+2][x] == '.':
                            self.tiles[Point(x, y+2)]['door'] = door
                            doors[door].add(Point(x, y+2))
                        elif raw_data[y-1][x] == '.':
                            self.tiles[Point(x, y-1)]['door'] = door
                            doors[door].add(Point(x, y-1))
                    elif raw_data[y][x+1] in string.ascii_uppercase:
                        to_skip.add((x+1, y))
                        door = ch + raw_data[y][x+1]
                        if x+2 < len(raw_data[y]) and raw_data[y][x+2] == '.':
                            self.tiles[Point(x+2, y)]['door'] = door
                            doors[door].add(Point(x+2, y))
                        elif raw_data[y][x-1] == '.':
                            self.tiles[Point(x-1, y)]['door'] = door
                            doors[door].add(Point(x-1, y))
        self.entry = doors['AA'].pop()
        del doors['AA']
        self.exit = doors['ZZ'].pop()
        del doors['ZZ']
        for points in doors.values():
            p1 = points.pop()
            p2 = points.pop()
            self.tiles[p1]['to'] = p2
            self.tiles[p1]['type'] = self.door_type(p1)
            self.tiles[p2]['to'] = p1
            self.tiles[p2]['type'] = self.door_type(p2)

    def door_type(self, p: Point):
        if p.x <= 3 or p.y <= 3:
            return 'out'
        if p.x >= self.width - 3 or p.y >= self.height - 3:
            return 'out'
        return 'in'


@dataclass
class QueueNode:
    point: Point
    distance: int


@dataclass
class QueueLevelNode:
    point: LevelPoint
    distance: int


def bfs(maze: Maze):
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    visited = [maze.entry]
    queue: Deque[QueueNode] = deque()
    queue.append(QueueNode(maze.entry, 0))
    while queue:
        node = queue.popleft()
        not_moved = True
        for i in range(4):
            x = node.point.x + directions_x[i]
            y = node.point.y + directions_y[i]
            new_point = Point(x, y)
            if new_point == maze.exit:
                return node.distance + 1

            if new_point not in visited and new_point in maze.tiles.keys():
                not_moved = False
                visited.append(new_point)
                queue.append(QueueNode(new_point, node.distance + 1))
        if not_moved and 'to' in maze.tiles[node.point]:
            new_point = maze.tiles[node.point]['to']
            if new_point == maze.exit:
                return node.distance + 1
            if new_point not in visited:
                visited.append(new_point)
                queue.append(QueueNode(new_point, node.distance + 1))

    return -1


def bfs_with_levels(maze: Maze):
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    visited = [LevelPoint(maze.entry.x, maze.entry.y, 0)]
    queue: Deque[QueueLevelNode] = deque()
    queue.append(QueueLevelNode(visited[0], 0))
    while queue:
        node = queue.popleft()
        not_moved = True
        for i in range(4):
            x = node.point.x + directions_x[i]
            y = node.point.y + directions_y[i]
            new_point = LevelPoint(x, y, node.point.level)
            if new_point.level == 0 and new_point.x == maze.exit.x and new_point.y == maze.exit.y:
                return node.distance + 1

            if new_point not in visited and Point(new_point.x, new_point.y) in maze.tiles.keys():
                not_moved = False
                visited.append(new_point)
                queue.append(QueueLevelNode(new_point, node.distance + 1))
        if not_moved and 'to' in maze.tiles[Point(node.point.x, node.point.y)]:
            new_point = maze.tiles[Point(node.point.x, node.point.y)]['to']
            if maze.tiles[Point(node.point.x, node.point.y)]['type'] == 'in':
                new_point = LevelPoint(new_point.x, new_point.y, node.point.level + 1)
            else:
                if node.point.level == 0:
                    continue
                new_point = LevelPoint(new_point.x, new_point.y, node.point.level - 1)
            if new_point.level == 0 and new_point.x == maze.exit.x and new_point.y == maze.exit.y:
                return node.distance + 1
            if new_point not in visited:
                visited.append(new_point)
                queue.append(QueueLevelNode(new_point, node.distance + 1))

    return -1


def bfs_nodes(start, maze: Maze):
    nodes = []
    return nodes


def solver():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        maze = Maze(lines)
        print('Part 1:', bfs(maze))
        print('Part 2:', bfs_with_levels(maze))


if __name__ == '__main__':
    solver()
