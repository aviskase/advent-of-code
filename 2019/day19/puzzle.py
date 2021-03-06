from dataclasses import dataclass
from itertools import repeat
from typing import List, Set


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


def create_beam(program) -> Set[Point]:
    beam = set()
    for y in range(BEAM_START_Y, BEAM_START_Y+BEAM_HEIGHT):
        beam.update(beam_row(program, y, BEAM_START_X, BEAM_WIDTH))
    return beam


def beam_gen(program):
    def _beam(x, y):
        computer = IntcodeComputer.from_string(program)
        outputs = computer.execute(input_data=[x, y], exit_on_output=True)
        return outputs[-1]
    return _beam


def beam_row(program, row, x_start, x_width) -> Set[Point]:
    beam = set()
    beamg = beam_gen(program)
    for x in range(x_start, x_start + x_width):
        if beamg(x, row) == 1:
            beam.add(Point(x, row))
    return beam


def print_beam(beam):
    grid = [
        ['.' for x in range(BEAM_WIDTH)] for y in range(BEAM_HEIGHT)
    ]
    for b in beam:
        grid[b.y - BEAM_START_Y][b.x - BEAM_START_X] = '#'
    print('\n'.join(''.join(row) for row in grid))


def search_square(program, bottom_left=(0, 10), square_size=100):
    beamg = beam_gen(program)
    coord_diff = square_size - 1
    while True:
        if beamg(*bottom_left):
            top_right = (bottom_left[0] + coord_diff, bottom_left[1] - coord_diff)
            if beamg(*top_right):  # implies top_left and bottom_right
                top_left = (bottom_left[0], bottom_left[1] - coord_diff)
                return 10000 * top_left[0] + top_left[1]
            bottom_left = bottom_left[0], bottom_left[1] + 1  # Move down
        else:
            bottom_left = bottom_left[0] + 1, bottom_left[1]  # Move right


BEAM_START_Y = 0
BEAM_START_X = 0
BEAM_WIDTH = 50
BEAM_HEIGHT = 50


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        beam = create_beam(line)
        print('Part 1:', len(beam))
        # print_beam(beam)
        print('Part 2:', search_square(line))


if __name__ == '__main__':
    solver()

