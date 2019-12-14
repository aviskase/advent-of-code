from typing import List
from itertools import repeat, zip_longest


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


class SparseList2D(list):
    def __setitem__(self, index, value):
        missing = index - len(self) + 1
        if missing > 0:
            self.extend(SparseList() for _ in range(missing))
        list.__setitem__(self, index, value)

    def __getitem__(self, index):
        try:
            return list.__getitem__(self, index)
        except IndexError:
            self[index] = SparseList()
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


def draw_board(computer):
    outputs = computer.execute(exit_on_input=True)
    return Board(outputs)


class Board:
    def __init__(self, data):
        self.ball = None
        self.paddle = None
        self.score = 0
        self.board = dict()
        self.screen = SparseList2D()
        for x, y, value in grouper(data, 3):
            self.update(x, y, value)

    def num_of_blocks(self):
        return sum(value == 2 for value in self.board.values())

    def update(self, x, y, value):
        if x == -1 and y == 0:
            self.score = value
        else:
            self.board[(x, y)] = value
            if value == 0:
                self.screen[y][x] = ' '
            if value == 1:
                self.screen[y][x] = '█'
            if value == 2:
                self.screen[y][x] = '#'
            if value == 3:
                self.paddle = (x, y)
                self.screen[y][x] = '_'
            if value == 4:
                self.ball = (x, y)
                self.screen[y][x] = 'o'

    def display(self):
        print('\n'.join(''.join(row) for row in self.screen))
        print(f'{self.score = }')


def predict_move(ball, paddle):
    if ball[0] == paddle[0]:
        return 0
    if ball[0] > paddle[0]:
        return 1
    if ball[0] < paddle[0]:
        return -1


def play_game(computer):
    board = draw_board(computer)
    while board.num_of_blocks() != 0:
        move = predict_move(board.ball, board.paddle)
        result = computer.execute(exit_on_output=True, exit_after=3, input_data=move, exit_on_input=True)
        if len(result) != 3:
            move = predict_move(board.ball, board.paddle)
            result = computer.execute(exit_on_output=True, exit_after=3, input_data=move)
        board.update(*result)
    result = computer.execute()
    board.update(*result)
    return board.score


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        computer = IntcodeComputer.from_string(line)
        board = draw_board(computer)
        print('Part 1:', board.num_of_blocks())
        computer = IntcodeComputer.from_string(line)
        computer.change_memory(0, 2)
        print('Part 2:', play_game(computer))


if __name__ == '__main__':
    solver()
