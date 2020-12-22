from __future__ import annotations

import math
import re
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional, Iterator, Dict

from more_itertools import first_true

TData = List[List[str]]


@dataclass
class Tile:
    id: int
    data: TData

    @property
    def left_border(self) -> List[str]: return [row[0] for row in self.data]

    @property
    def right_border(self) -> List[str]: return [row[-1] for row in self.data]

    @property
    def top_border(self) -> List[str]: return list(self.data[0])

    @property
    def bottom_border(self) -> List[str]: return list(self.data[-1])

    def rotate(self) -> Tile: return Tile(self.id, [list(row) for row in zip(*reversed(self.data))])

    def flip(self) -> Tile: return Tile(self.id, [list(reversed(row)) for row in self.data])

    def reorient(self) -> Iterator[Tile]:
        current = self
        for _j in range(4):
            current = current.rotate()
            yield current
        current = current.flip()
        for _j in range(4):
            current = current.rotate()
            yield current

    def match_top(self, other_tiles: TTiles):
        for other_tile in other_tiles.values():
            matched = first_true(other_tile.reorient(), None, lambda t: self.top_border == t.bottom_border)
            if matched:
                return matched

    def match_left(self, other_tiles: TTiles):
        for other_tile in other_tiles.values():
            matched = first_true(other_tile.reorient(), None, lambda t: self.left_border == t.right_border)
            if matched:
                return matched

    def match_right(self, other_tiles: TTiles):
        for other_tile in other_tiles.values():
            matched = first_true(other_tile.reorient(), None, lambda t: self.right_border == t.left_border)
            if matched:
                return matched

    def match_bottom(self, other_tiles: TTiles):
        for other_tile in other_tiles.values():
            matched = first_true(other_tile.reorient(), None, lambda t: self.bottom_border == t.top_border)
            if matched:
                return matched

    @property
    def inner(self): return [row[1:-1] for row in self.data[1:-1]]

    @classmethod
    def from_image(cls, image: TImage) -> Tile:
        rows_per_tile = len(image[0][0].inner)
        data = [
            list(value for tile in row for value in tile.inner[sub_row])
            for row in image
            for sub_row in range(rows_per_tile)
        ]
        return cls(0, data)

    def __repr__(self):
        return '\n'.join(self.semi_stringified())

    def semi_stringified(self):
        return [''.join(row) for row in self.data]


TTiles = Dict[int, Tile]
TImage = List[List[Optional[Tile]]]


def replace_sea_monsters(img: TImage) -> int:
    top_regex = re.compile('.{18}#.')
    middle_regex = re.compile('#.{4}##.{4}##.{4}###')
    bottom_regex = re.compile('.#..#..#..#..#..#...')
    main_tile = Tile.from_image(img)
    snake_tiles = 15

    for tile in main_tile.reorient():
        found = False
        roughness = repr(tile).count('#')
        tile_s = tile.semi_stringified()
        for i, s in enumerate(tile_s[1:-1]):
            for match in middle_regex.finditer(s):
                if top_regex.match(tile_s[i], match.start(), match.end()) and bottom_regex.match(tile_s[i+2], match.start(), match.end()):
                    found = True
                    roughness -= snake_tiles
        if found:
            return roughness


def parse(raw_data: str) -> TTiles:
    tiles = {}
    raw_tiles = raw_data.split('\n\n')
    for raw_tile in raw_tiles:
        title, *data = raw_tile.strip().splitlines()
        tile_id = int(title.replace('Tile ', '').replace(':', '').strip())
        tiles[tile_id] = Tile(id=tile_id, data=[list(d) for d in data])
    return tiles


def detect_image(tiles: TTiles, corners: List[Tile]) -> TImage:
    for corner in corners:
        for reoriented_corner in corner.reorient():
            image = get_image_from_left_top_corner(tiles, reoriented_corner)
            if image:
                return image


def get_image_from_left_top_corner(input_tiles: TTiles, left_top: Tile) -> Optional[TImage]:
    tiles = deepcopy(input_tiles)
    size = int(len(tiles.keys()) ** 0.5)
    image: TImage = [[None] * size for _ in range(size)]
    offset_y = 0
    offset_x = 0
    try:
        while tiles:
            y = offset_y
            for x in range(offset_x, size-offset_x):
                if x == 0 and y == 0:
                    del tiles[left_top.id]
                    image[0][0] = left_top
                    continue
                current = image[y][x-1]
                matching = current.match_right(tiles)
                del tiles[matching.id]
                image[y][x] = matching

            x = size - 1 - offset_x
            for y in range(1+offset_y, size-offset_y):
                current = image[y-1][x]
                matching = current.match_bottom(tiles)
                del tiles[matching.id]
                image[y][x] = matching

            y = size - 1 - offset_y
            for x in range(size-2-offset_x, offset_x-1, -1):
                current = image[y][x + 1]
                matching = current.match_left(tiles)
                del tiles[matching.id]
                image[y][x] = matching

            x = offset_x
            for y in range(size-2-offset_y, offset_y, -1):
                current = image[y+1][x]
                matching = current.match_top(tiles)
                del tiles[matching.id]
                image[y][x] = matching
            offset_y += 1
            offset_x += 1

        return image
    except AttributeError:
        return None


def find_corners(tiles: TTiles) -> List[Tile]:
    corners = []
    for tile in tiles.values():
        other_tiles = {k: t for k, t in tiles.items() if t.id != tile.id}
        matches = [
            1 if tile.match_top(other_tiles) else 0,
            1 if tile.match_left(other_tiles) else 0,
            1 if tile.match_bottom(other_tiles) else 0,
            1 if tile.match_right(other_tiles) else 0,
        ]
        if sum(matches) == 2:
            corners.append(tile)
    return corners


def solver():
    with open('input.txt', 'r') as f:
        tiles = parse(f.read().strip())
        corners = find_corners(tiles)
        print('Part 1:', math.prod(t.id for t in corners))  # 30425930368573
        img = detect_image(tiles, corners)
        print('Part 2:', replace_sea_monsters(img))  # 2453


if __name__ == '__main__':
    solver()
