from collections import defaultdict
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


class RecursiveBugSimulator:
    size = 5
    middle = 2

    def __populator(self):
        return [[False] * self.size for _ in range(self.size)]

    def __init__(self, scan):
        self.state = defaultdict(self.__populator)
        for y, line in enumerate(scan.split()):
            for x, item in enumerate(list(line.strip())):
                self.state[0][y][x] = item == '#'

    def state_to_str(self, level):
        s = []
        for y, row in enumerate(self.state[level]):
            s.append([])
            for x, element in enumerate(row):
                s[y].append('#' if element else '.')
        s[self.middle][self.middle] = '?'
        return '\n'.join(''.join(row) for row in s)

    def evolve_for(self, minutes):
        for m in range(minutes):
            self.evolve()

    def evolve(self):
        new_state = defaultdict(self.__populator)
        for level in self.state:
            new_state[level] = self._populate_level(level)
        min_level = min(new_state.keys())
        self._add_levels(new_state, min_level, False)
        max_level = max(new_state.keys())
        self._add_levels(new_state, max_level, True)
        self.state = new_state

    def _new_state(self, x, y, level):
        bug = self.state[level][y][x]
        adjacent_bugs = []
        if (x - 1, y) == (self.middle, self.middle) and level+1 in self.state:
            adjacent_bugs.extend(self._right_border(self.state[level+1]))
        elif x - 1 >= 0:
            adjacent_bugs.append(self.state[level][y][x - 1])
        elif level-1 in self.state:
            adjacent_bugs.extend(self._left_border(self.state[level-1], True))

        if (x + 1, y) == (self.middle, self.middle) and level+1 in self.state:
            adjacent_bugs.extend(self._left_border(self.state[level+1]))
        elif x + 1 < self.size:
            adjacent_bugs.append(self.state[level][y][x + 1])
        elif level-1 in self.state:
            adjacent_bugs.extend(self._right_border(self.state[level-1], True))

        if (x, y - 1) == (self.middle, self.middle) and level+1 in self.state:
            adjacent_bugs.extend(self._lower_border(self.state[level+1]))
        elif y - 1 >= 0:
            adjacent_bugs.append(self.state[level][y - 1][x])
        elif level-1 in self.state:
            adjacent_bugs.extend(self._upper_border(self.state[level-1], True))

        if (x, y + 1) == (self.middle, self.middle) and level+1 in self.state:
            adjacent_bugs.extend(self._upper_border(self.state[level+1]))
        elif y + 1 < self.size:
            adjacent_bugs.append(self.state[level][y + 1][x])
        elif level-1 in self.state:
            adjacent_bugs.extend(self._lower_border(self.state[level-1], True))

        adjacent_bugs = adjacent_bugs.count(True)
        if bug:
            return adjacent_bugs == 1
        else:
            return adjacent_bugs == 1 or adjacent_bugs == 2

    def _populate_level(self, level):
        grid = []
        for y in range(self.size):
            grid.append([])
            for x in range(self.size):
                if (x, y) == (self.middle, self.middle):
                    # middle point must always be False for bug count to work!
                    grid[y].append(False)
                else:
                    grid[y].append(self._new_state(x, y, level))
        return grid

    def _add_levels(self, container, from_level, inner):
        new_level = from_level + 1 if inner else from_level - 1
        if self._bugs_in_borders(container[from_level], inner):
            grid = self._populate_level(new_level)
            container[new_level] = grid
            self._add_levels(container, new_level, inner)
        return

    @staticmethod
    def _bugs_in_borders(grid, inner=False):
        return any([
            *RecursiveBugSimulator._upper_border(grid, inner),
            *RecursiveBugSimulator._lower_border(grid, inner),
            *RecursiveBugSimulator._left_border(grid, inner),
            *RecursiveBugSimulator._right_border(grid, inner),
        ])

    @staticmethod
    def _upper_border(grid, inner=False):
        if inner:
            return [grid[RecursiveBugSimulator.middle - 1][RecursiveBugSimulator.middle]]
        return grid[0]

    @staticmethod
    def _lower_border(grid, inner=False):
        if inner:
            return [grid[RecursiveBugSimulator.middle + 1][RecursiveBugSimulator.middle]]
        return grid[-1]

    @staticmethod
    def _left_border(grid, inner=False):
        if inner:
            return [grid[RecursiveBugSimulator.middle][RecursiveBugSimulator.middle - 1]]
        return [i[0] for i in grid]

    @staticmethod
    def _right_border(grid, inner=False):
        if inner:
            return [grid[RecursiveBugSimulator.middle][RecursiveBugSimulator.middle + 1]]
        return [i[-1] for i in grid]

    @property
    def bugs_count(self):
        return sum(
            list(chain.from_iterable(level)).count(True)
            for level in self.state.values()
        )


def solver():
    bugs = BugSimulator(INPUT_SCAN)
    bugs.evolve_until_same()
    print('Part 1:', bugs.biodiversity())
    bugs = RecursiveBugSimulator(INPUT_SCAN)
    bugs.evolve_for(200)
    print('Part 2:', bugs.bugs_count)


if __name__ == '__main__':
    solver()
