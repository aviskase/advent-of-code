from itertools import chain


INPUT_SCAN = '''
#..##
#.#..
#...#
##..#
#..##'''


class BugSimulator:
    size = 5

    def __init__(self, scan):
        self.current_state, self.states = [], []
        for y, line in enumerate(scan.split()):
            self.current_state.append([])
            for x, item in enumerate(list(line.strip())):
                self.current_state[y].append(item == '#')

    def __str__(self):
        s = []
        for y, row in enumerate(self.current_state):
            s.append([])
            for x, element in enumerate(row):
                s[y].append('#' if element else '.')
        return '\n'.join(''.join(row) for row in s)

    def biodiversity(self):
        flat_state = chain.from_iterable(self.current_state)
        return sum(2**i for i, bug in enumerate(flat_state) if bug)

    def evolve_for(self, minutes):
        for m in range(minutes):
            self.evolve()

    def evolve_until_same(self):
        minutes = 0
        while True:
            self.evolve()
            minutes += 1
            if self.current_state in self.states:
                return minutes

    def evolve(self):
        new_state = []
        for y in range(self.size):
            new_state.append([])
            for x in range(self.size):
                new_state[y].append(self._new_state(x, y))
        self.states.append(self.current_state)
        self.current_state = new_state

    def _new_state(self, x, y):
        bug = self.current_state[y][x]
        adjacent_bugs = [
            self.current_state[y][x-1] if x-1 >= 0 else False,
            self.current_state[y][x+1] if x+1 < self.size else False,
            self.current_state[y-1][x] if y-1 >= 0 else False,
            self.current_state[y+1][x] if y+1 < self.size else False,
        ]
        adjacent_bugs = adjacent_bugs.count(True)
        if bug:
            return adjacent_bugs == 1
        else:
            return adjacent_bugs == 1 or adjacent_bugs == 2


def solver():
    bugs = BugSimulator(INPUT_SCAN)
    bugs.evolve_until_same()
    print('Part 1:', bugs.biodiversity())


if __name__ == '__main__':
    solver()
