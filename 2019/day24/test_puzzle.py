from .puzzle import BugSimulator, RecursiveBugSimulator


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


def test_recursive_evolve_bug_count():
    bugs = RecursiveBugSimulator('....#\n#..#.\n#.?##\n..#..\n#....')
    bugs.evolve_for(10)
    assert bugs.bugs_count == 99


def test_recursive_evolve():
    bugs = RecursiveBugSimulator('....#\n#..#.\n#.?##\n..#..\n#....')
    bugs.evolve_for(1)
    assert set(bugs.state.keys()) == {-1, 0, 1}
    assert bugs.state_to_str(0) == '#..#.\n####.\n##?.#\n##.##\n.##..'
    assert bugs.state_to_str(-1) == '.....\n..#..\n..?#.\n..#..\n.....'
    assert bugs.state_to_str(1) == '....#\n....#\n..?.#\n....#\n#####'
