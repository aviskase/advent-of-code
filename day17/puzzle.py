from collections import deque
from dataclasses import dataclass
from typing import List, Deque, Set
from itertools import repeat
from copy import deepcopy


class SparseList(list):
    filler = 0

    def __setitem__(self, index, value):
        missing = index - len(self) + 1
        if missing > 0:
            self.extend([self.filler] * missing)
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            self[index] = self.filler
            return self.filler


class IntcodeComputer:
    relative_base = 0
    index = 0

    @classmethod
    def from_string(cls, program):
        return cls([int(intcode) for intcode in program.split(',')])

    def __init__(self, program: List[int]):
        self.program = SparseList(program.copy())
        self.finished = False

    def change_memory(self, index, value):
        self.program[index] = value

    @staticmethod
    def unpack_code(raw_code):
        data = f'{raw_code:05}'
        code = int(data[-2:])
        modes = list(map(int, data[-3::-1]))
        return code, modes

    def set_value(self, param_num, value, modes):
        mode = modes[param_num-1]
        val = self.program[self.index + param_num]
        if mode == 0:
            self.program[val] = value
        elif mode == 2:
            self.program[val + self.relative_base] = value

    def get_value(self, param_num, modes):
        mode = modes[param_num-1]
        val = self.program[self.index + param_num]
        if mode == 0:
            return self.program[val]
        if mode == 1:
            return val
        if mode == 2:
            return self.program[val + self.relative_base]

    def execute(self, input_data=None, exit_on_output=False, exit_after=1, exit_on_input=False):
        outputs = []
        inputs = None
        if input_data is not None:
            inputs = self.inputs_generator(input_data)
        ready_to_exit = False
        while not ready_to_exit:
            current_code, current_modes = self.unpack_code(self.program[self.index])
            if current_code == 1:
                value1 = self.get_value(1, current_modes)
                value2 = self.get_value(2, current_modes)
                self.set_value(3, value1 + value2, current_modes)
                self.index += 4
            elif current_code == 2:
                value1 = self.get_value(1, current_modes)
                value2 = self.get_value(2, current_modes)
                self.set_value(3, value1 * value2, current_modes)
                self.index += 4
            elif current_code == 3:
                if not exit_on_input:
                    value = next(inputs)
                    self.set_value(1, value, current_modes)
                    self.index += 2
                ready_to_exit = exit_on_input
            elif current_code == 4:
                output_value = self.get_value(1, current_modes)
                self.index += 2
                outputs.append(output_value)
                ready_to_exit = exit_on_output and len(outputs) == exit_after
            elif current_code == 5:
                value = self.get_value(1, current_modes)
                position = self.get_value(2, current_modes)
                self.index = position if value != 0 else self.index + 3
            elif current_code == 6:
                value = self.get_value(1, current_modes)
                position = self.get_value(2, current_modes)
                self.index = position if value == 0 else self.index + 3
            elif current_code == 7:
                value1 = self.get_value(1, current_modes)
                value2 = self.get_value(2, current_modes)
                result = 1 if value1 < value2 else 0
                self.set_value(3, result, current_modes)
                self.index += 4
            elif current_code == 8:
                value1 = self.get_value(1, current_modes)
                value2 = self.get_value(2, current_modes)
                result = 1 if value1 == value2 else 0
                self.set_value(3, result, current_modes)
                self.index += 4
            elif current_code == 9:
                self.relative_base += self.get_value(1, current_modes)
                self.index += 2
            elif current_code == 99:
                ready_to_exit = True
                self.finished = True
            else:
                raise ValueError(f'Unexpected optcode {current_code}')
        return outputs

    @staticmethod
    def inputs_generator(inputs):
        if not isinstance(inputs, list):
            inputs = [inputs]
        for i in inputs:
            yield i
        yield from repeat(inputs[-1])


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


class Grid:
    robot: Point
    scaffold: Set[Point]

    @classmethod
    def from_ascii_codes(cls, codes):
        grid = []
        row = []
        for code in map(chr, codes):
            if code == '\n':
                grid.append(row)
                row = []
            else:
                row.append(code)
        return cls(grid)

    @staticmethod
    def grid_to_coordinates(grid):
        scaffold = set()
        for y, row in enumerate(grid):
            for x, item in enumerate(row):
                if item == '#':
                    scaffold.add(Point(x, y))
                if item == '^':
                    direction = 'up'
                    scaffold.add(Point(x, y))
                    robot = Point(x, y)
                if item == 'v':
                    direction = 'down'
                    scaffold.add(Point(x, y))
                    robot = Point(x, y)
                if item == '<':
                    direction = 'left'
                    scaffold.add(Point(x, y))
                    robot = Point(x, y)
                if item == '>':
                    direction = 'right'
                    scaffold.add(Point(x, y))
                    robot = Point(x, y)
        return scaffold, robot, direction

    def __init__(self, grid):
        self.grid = grid
        self.scaffold, self.robot, self.direction = Grid.grid_to_coordinates(self.grid)

    def find_intersections(self) -> Set[Point]:
        intersections = set()
        #  .#.
        #  ###
        #  .#.
        for p in self.scaffold:
            on_path = {
                Point(p.x, p.y - 1),
                Point(p.x, p.y + 1),
                Point(p.x - 1, p.y),
                Point(p.x + 1, p.y),
            }
            not_on_path = {
                Point(p.x - 1, p.y - 1),
                Point(p.x + 1, p.y - 1),
                Point(p.x - 1, p.y + 1),
                Point(p.x + 1, p.y + 1),
            }
            if on_path <= self.scaffold and not not_on_path <= self.scaffold:
                intersections.add(p)
        return intersections

    def alignment(self):
        return sum(p.x * p.y for p in self.find_intersections())

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)


def create_grid(computer: IntcodeComputer):
    outputs = computer.execute()
    return Grid.from_ascii_codes(outputs)


def manual_solve(computer: IntcodeComputer):
    routine = list(map(ord, 'B,C,B,C,A,B,A,B,A,C\n'))
    A = list(map(ord, 'L,8,L,4,R,12,L,6,L,4\n'))
    B = list(map(ord, 'R,12,L,8,L,4,L,4\n'))
    C = list(map(ord, 'L,8,R,6,L,6\n'))
    routine.extend(A)
    routine.extend(B)
    routine.extend(C)
    return computer.execute(input_data=routine)


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        computer = IntcodeComputer.from_string(line)
        grid = create_grid(computer)
        print(grid)
        print('Part 1:', grid.alignment())
        computer = IntcodeComputer.from_string(line)
        computer.change_memory(0, 2)
        print('Part 2:', manual_solve(computer)[-1])


if __name__ == '__main__':
    solver()


# R,1,2,L,8,L,4,L,4,L,8,R,6,L,6,R,1,2,L,8,L,4,L,4,L,8,R,6,L,6,L,8,L,4,R,1,2,L,6,L,4,R,1,2,L,8,L,4,L,4,L,8,L,4,R,1,2,L,6,L,4,R,1,2,L,8,L,4,L,4,L,8,L,4,R,1,2,L,6,L,4,L,8,R,6,L,6
# 'B,C,B,C,A,B,A,B,A,C\n'
#
# a = 'L,8,L,4,R,12,L,6,L,4\n'
# b = 'R,12,L,8,L,4,L,4\n'
# c = 'L,8,R,6,L,6\n'
