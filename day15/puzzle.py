from collections import deque
from dataclasses import dataclass
from typing import List, Deque
from itertools import repeat, zip_longest
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


class SparseStrList(SparseList):
    filler = '█'


class SparseList2D(list):
    def __setitem__(self, index, value):
        missing = index - len(self) + 1
        if missing > 0:
            self.extend(SparseStrList() for _ in range(missing))
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            self[index] = SparseStrList()
            return self[index]


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


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Board:
    def __init__(self, data):
        self.oxygen = None
        self.droid = None
        self.board = dict()
        self.screen = SparseList2D()
        for x, y, value in grouper(data, 3):
            self.update(x, y, value)

    def update(self, x, y, value):
        if value == 'block':
            self.screen[y][x] = '#'
        if value == 'visited':
            self.screen[y][x] = '.'
        if value == 'oxygen':
            self.oxygen = (x, y)
            self.screen[y][x] = 'W' if self.oxygen == self.droid else 'x'
        if value == 'droid':
            self.droid = (x, y)
            self.screen[y][x] = 'W' if self.oxygen == self.droid else 'D'

    def display(self):
        print('\n'.join(''.join(row) for row in self.screen))
        if self.oxygen is not None:
            print(f'Oxygen found! {self.oxygen}')


def new_coordinate(origin, direction):
    if direction == 1:
        return origin[0], origin[1] - 1
    if direction == 2:
        return origin[0], origin[1] + 1
    if direction == 3:
        return origin[0] - 1, origin[1]
    if direction == 4:
        return origin[0] + 1, origin[1]


def control_droid(computer: IntcodeComputer):
    current_position = (25, 25)
    board = Board([*current_position, 'droid'])
    while not computer.finished:
        computer.execute(exit_on_input=True)
        move = int(input('1n, 2s, 3w, 4e, 0exit: '))
        if move == 0:
            break
        output = computer.execute(input_data=move, exit_on_output=True)[0]
        if output == 0:
            board.update(*new_coordinate(current_position, move), 'block')
        if output == 1:
            board.update(*current_position, 'visited')
            current_position = new_coordinate(current_position, move)
            board.update(*current_position, 'droid')
        if output == 2:
            board.update(*current_position, 'visited')
            current_position = new_coordinate(current_position, move)
            board.update(*current_position, 'oxygen')
            board.update(*current_position, 'droid')
        board.display()


@dataclass
class Point:
    x: int
    y: int


@dataclass
class QueueNode:
    point: Point
    distance: int
    computer: IntcodeComputer


def bfs(computer):
    source = Point(25, 25)
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    visited = [source]
    queue: Deque[QueueNode] = deque()
    queue.append(QueueNode(source, 0, deepcopy(computer)))
    while queue:
        current_node = queue[0]
        current_point = current_node.point
        queue.popleft()
        for i in range(4):
            direction = i + 1
            x = current_point.x + directions_x[i]
            y = current_point.y + directions_y[i]
            new_point = Point(x, y)
            current_computer = deepcopy(current_node.computer)
            output = current_computer.execute(input_data=direction, exit_on_output=True)[0]
            if output == 2:
                return current_node.distance + 1
            if new_point not in visited and output == 1:
                visited.append(new_point)
                queue.append(QueueNode(
                    new_point,
                    current_node.distance + 1,
                    current_computer
                ))
    return -1


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        computer = IntcodeComputer.from_string(line)
        print('Part 1:', bfs(computer))


if __name__ == '__main__':
    solver()
