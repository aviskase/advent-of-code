import pytest

from .puzzle import play_game


@pytest.mark.parametrize('moves, expected', [(10, '92658374'), (100, '67384529')])
def test_play_game(moves, expected):
    data = '389125467'
    assert play_game(data, moves) == expected
