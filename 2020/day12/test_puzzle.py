from .puzzle import move_ship, mdistance

data = '''F10
N3
F7
R90
F11
'''.strip().splitlines()


def test_move_ship():
    position = move_ship(data)
    assert position == (17, -8)
    assert mdistance(*position) == 25
