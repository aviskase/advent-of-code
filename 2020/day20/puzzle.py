from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Iterator, Dict

from more_itertools import first_true

TData = List[List[str]]



@dataclass
class Tile:
    id: int
    data: TData

    def left_border(self) -> List[str]: return [row[0] for row in self.data]

    def right_border(self) -> List[str]: return [row[-1] for row in self.data]

    def top_border(self) -> List[str]: return list(self.data[0])

    def bottom_border(self) -> List[str]: return list(self.data[-1])

    def rotate(self) -> Tile: return Tile(self.id, [list(row) for row in zip(*reversed(self.data))])
    # def rotate(self) -> Tile: return Tile(self.id, list(list(row) for row in zip(*self.data))[::-1])

    def flip_y(self) -> Tile: return Tile(self.id, [list(reversed(row)) for row in self.data])
    # def flip_y(self) -> Tile: return Tile(self.id, list(reversed(self.data)))

    def flip_x(self) -> Tile: return Tile(self.id, [list(reversed(r)) for r in self.data])

    def reorient(self) -> Iterator[Tile]:
        current = self
        for _j in range(4):
            current = current.rotate()
            yield current
        current = current.flip_y()
        for _j in range(4):
            current = current.rotate()
            yield current

    def match_top(self, other_tile: Tile):
        return first_true(other_tile.reorient(), None, lambda t: self.top_border() == t.bottom_border())

    def match_left(self, other_tile: Tile):
        return first_true(other_tile.reorient(), None, lambda t: self.left_border() == t.right_border())

    def match_right(self, other_tile: Tile):
        return first_true(other_tile.reorient(), None, lambda t: self.right_border() == t.left_border())

    def match_bottom(self, other_tile: Tile):
        return first_true(other_tile.reorient(), None, lambda t: self.bottom_border() == t.top_border())


TTiles = Dict[int, Tile]
TImage = List[List[Optional[Tile]]]


def parse(raw_data: str) -> TTiles:
    tiles = {}
    raw_tiles = raw_data.split('\n\n')
    for raw_tile in raw_tiles:
        title, *data = raw_tile.strip().splitlines()
        tile_id = int(title.replace('Tile ', '').replace(':', '').strip())
        tiles[tile_id] = Tile(id=tile_id, data=[list(d) for d in data])
    return tiles


# def detect_image(input_tiles: TTiles) -> TImage:
#     tiles = deepcopy(input_tiles)
#     size = int(len(tiles.keys()) ** 0.5)
#     image: TImage = [[None] * size for _ in range(size)]
#
#     offset_y = 0
#     offset_x = 0
#     while tiles:
#         y = offset_y
#         for x in range(offset_x, size-offset_x):
#             if x == 0 and y == 0:
#                 doing = find_left_top(tiles)
#                 del tiles[doing.id]
#                 image[0][0] = doing
#                 continue
#             current = image[y][x-1]
#             matching = next((other_tile for other_tile in tiles.values() if current.match_right(other_tile)), None)
#             del tiles[matching.id]
#             image[y][x] = matching
#
#         x = size - 1 - offset_x
#         for y in range(1+offset_y, size-offset_y):
#             current = image[y-1][x]
#             matching = next((other_tile for other_tile in tiles.values() if current.match_bottom(other_tile)), None)
#             del tiles[matching.id]
#             image[y][x] = matching
#
#         y = size - 1 - offset_y
#         for x in range(size-2-offset_x, offset_x-1, -1):
#             current = image[y][x + 1]
#             matching = next((other_tile for other_tile in tiles.values() if current.match_left(other_tile)), None)
#             del tiles[matching.id]
#             image[y][x] = matching
#
#         x = offset_x
#         for y in range(size-2-offset_y, offset_y, -1):
#             current = image[y+1][x]
#             matching = next((other_tile for other_tile in tiles.values() if current.match_top(other_tile)), None)
#             del tiles[matching.id]
#             image[y][x] = matching
#         offset_y += 1
#         offset_x += 1
#
#     return image


def img_ids(image: TImage):
    return [list(t.id if t else '----' for t in row) for row in image]


def find_corners(tiles: TTiles) -> List[Tile]:
    corners = []
    for tile in tiles.values():
        other_tiles = [t for t in tiles.values() if t.id != tile.id]
        num = [
            next((1 for other_tile in other_tiles if tile.match_top(other_tile)), 0),
            next((1 for other_tile in other_tiles if tile.match_left(other_tile)), 0),
            next((1 for other_tile in other_tiles if tile.match_bottom(other_tile)), 0),
            next((1 for other_tile in other_tiles if tile.match_right(other_tile)), 0)
        ]
        if sum(num) == 2:
            corners.append(tile)
    return corners


def solver():
    with open('input.txt', 'r') as f:
        tiles = parse(f.read().strip())
        corners = find_corners(tiles)
        print('Part 1:', math.prod(t.id for t in corners))  # 30425930368573
        # print('Part 2:', )  # 332


if __name__ == '__main__':
    solver()
