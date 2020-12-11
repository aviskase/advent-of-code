import pytest

from .puzzle import simulate

data = [list(d) for d in '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''.strip().splitlines()]

one_round = [list(d) for d in '''#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
'''.strip().splitlines()]

second_round = [list(d) for d in '''#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##
'''.strip().splitlines()]

end_round = [list(d) for d in '''#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##
'''.strip().splitlines()]


@pytest.mark.parametrize('rounds, expected', [(1, one_round), (2, second_round), (None, end_round)])
def test_simulate(rounds, expected):
    assert simulate(data, max_rounds=rounds) == expected
