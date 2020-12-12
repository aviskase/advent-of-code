from .puzzle import move_ship, mdistance, move_ship_with_waypoint

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


def test_move_ship_with_waypoint():
    position = move_ship_with_waypoint(data)
    assert position == (214, -72)
    assert mdistance(*position) == 286
