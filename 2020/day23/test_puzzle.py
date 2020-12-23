import pytest

from .puzzle import play_game, play_game2


@pytest.mark.parametrize('moves, expected', [(10, '92658374'), (100, '67384529')])
def test_play_game(moves, expected):
    data = '389125467'
    assert play_game(data, moves) == expected


def test_play_game2():
    data = '389125467'
    assert play_game2(data) == (934001, 159792)
