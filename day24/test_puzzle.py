from day24.puzzle import BugSimulator


def test_biodiversity_calc():
    bugs = BugSimulator('.....\n.....\n.....\n#....\n.#...')
    assert bugs.biodiversity() == 2129920


def test_evolve():
    bugs = BugSimulator('....#\n#..#.\n#..##\n..#..\n#....')
    bugs.evolve()
    assert str(bugs) == '#..#.\n####.\n###.#\n##.##\n.##..'
    bugs.evolve_for(minutes=3)
    assert str(bugs) == '####.\n....#\n##..#\n.....\n##...'


def test_evolve_same():
    bugs = BugSimulator('....#\n#..#.\n#..##\n..#..\n#....')
    bugs.evolve_until_same()
    assert str(bugs) == '.....\n.....\n.....\n#....\n.#...'
