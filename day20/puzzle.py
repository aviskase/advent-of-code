import string
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, Deque, Union


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


class Maze:
    entry: Point
    exit: Point
    tiles: Dict[Point, Dict[str, Union[str, None, Point]]]

    def __init__(self, lines):
        raw_data = [list(line.strip('\n')) for line in lines]
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
                    if y+1 < len(raw_data) and x < len(raw_data[y+1]) and raw_data[y+1][x] in string.ascii_uppercase:
                        to_skip.add((x, y+1))
                        door = ch + raw_data[y+1][x]
                        if y+2 < len(raw_data) and raw_data[y+2][x] == '.':
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
            self.tiles[p2]['to'] = p1


@dataclass
class QueueNode:
    point: Point
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


def solver():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        maze = Maze(lines)
        print('Part 1:', bfs(maze))


if __name__ == '__main__':
    solver()
