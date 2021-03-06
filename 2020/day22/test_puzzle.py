from .puzzle import parse, score, play_drunkard, play_drunkard_recursive

data = '''
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''.strip()


def test_score():
    winner, winner_id = play_drunkard(*parse(data))
    assert winner_id == 2
    assert score(winner) == 306


def test_rec_score():
    winner, winner_id = play_drunkard_recursive(*parse(data))
    assert winner_id == 2
    assert score(winner) == 291
