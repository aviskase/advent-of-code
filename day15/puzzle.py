from collections import deque
from dataclasses import dataclass
from typing import List, Deque
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


@dataclass
class Point:
    x: int
    y: int


@dataclass
class QueueNode:
    point: Point
    distance: int
    computer: IntcodeComputer


def bfs(computer, fill_all=False):
    source = Point(0, 0)
    directions_x = [0, 0, -1, 1]
    directions_y = [-1, 1, 0, 0]
    visited = [source]
    queue: Deque[QueueNode] = deque()
    queue.append(QueueNode(source, 0, deepcopy(computer)))
    distances = set()
    while queue:
        node = queue[0]
        queue.popleft()
        for i in range(4):
            direction = i + 1
            x = node.point.x + directions_x[i]
            y = node.point.y + directions_y[i]
            new_point = Point(x, y)
            current_computer = deepcopy(node.computer)
            output = current_computer.execute(input_data=direction, exit_on_output=True)[0]
            if output == 2 and not fill_all:
                return node.distance + 1, current_computer
            if new_point not in visited and output == 1:
                visited.append(new_point)
                queue.append(QueueNode(new_point, node.distance + 1, current_computer))
                distances.add(node.distance + 1)
    return max(distances)


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        computer = IntcodeComputer.from_string(line)
        distance, init_computer = bfs(computer)
        print('Part 1:', distance)
        print('Part 2:', bfs(init_computer, fill_all=True))


if __name__ == '__main__':
    solver()
