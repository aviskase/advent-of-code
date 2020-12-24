import pytest

from .puzzle import parse_tile, Direction, count_blacks, paint_it_black, flip


@pytest.mark.parametrize('tile, expected', [
    ('esenee', [Direction.E, Direction.SE, Direction.NE, Direction.E]),
    ('esew', [Direction.E, Direction.SE, Direction.W]),
    ('nwwswee', [Direction.NW, Direction.W, Direction.SW, Direction.E, Direction.E])
])
def test_parse_tile(tile, expected):
    assert parse_tile(tile) == expected



data = '''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew'''.strip().splitlines()


def test_count_blacks():
    d = [parse_tile(d) for d in data]
    assert count_blacks(paint_it_black(d)) == 10


def test_flip():
    d = [parse_tile(d) for d in data]
    assert count_blacks(flip(paint_it_black(d))) == 2208
