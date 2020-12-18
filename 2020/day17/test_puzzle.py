import pytest

from .puzzle import simulate, make_cube, count_active

data = '''.#.
..#
###
'''.strip()

round_one = '''#..
..#
.#.

#.#
.##
.#.

#..
..#
.#.
'''.strip()

round_two = '''.....
.....
..#..
.....
.....

..#..
.#..#
....#
.#...
.....

##...
##...
#....
....#
.###.

..#..
.#..#
....#
.#...
.....

.....
.....
..#..
.....
.....'''


@pytest.mark.parametrize('rounds, end', [(1, round_one.count('#')), (2, round_two.count('#')), (6, 112)])
def test_simulate(rounds, end):
    assert count_active(simulate(make_cube(data), max_rounds=rounds)) == end

