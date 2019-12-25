from collections import defaultdict
from typing import Dict


class IntcodeComputer:
    relative_base = 0
    index = 0

    @classmethod
    def from_string(cls, s):
        program = defaultdict(lambda: 0)
        for i, intcode in enumerate(s.split(',')):
            program[i] = int(intcode)
        return cls(program)

    def __init__(self, program: Dict[int, int]):
        self.program = program
        self.finished = False

    def change_memory(self, index, value):
        self.program[index] = value

    @staticmethod
    def get_mode(code, param_num):
        return code // (10 * 10 ** param_num) % 10

    def set_value(self, param_num, value, code):
        mode = IntcodeComputer.get_mode(code, param_num)
        val = self.program[self.index + param_num]
        if mode == 0:
            self.program[val] = value
        elif mode == 2:
            self.program[val + self.relative_base] = value

    def get_value(self, param_num, code):
        mode = IntcodeComputer.get_mode(code, param_num)
        val = self.program[self.index + param_num]
        if mode == 0:
            return self.program[val]
        if mode == 1:
            return val
        if mode == 2:
            return self.program[val + self.relative_base]

    def execute(self):
        while not self.finished:
            code = self.program[self.index]
            operation = code % 100
            if operation == 1:
                value1 = self.get_value(1, code)
                value2 = self.get_value(2, code)
                self.set_value(3, value1 + value2, code)
                self.index += 4
            elif operation == 2:
                value1 = self.get_value(1, code)
                value2 = self.get_value(2, code)
                self.set_value(3, value1 * value2, code)
                self.index += 4
            elif operation == 3:
                value = yield
                self.set_value(1, value, code)
                self.index += 2
            elif operation == 4:
                output_value = self.get_value(1, code)
                self.index += 2
                yield output_value
            elif operation == 5:
                value = self.get_value(1, code)
                position = self.get_value(2, code)
                self.index = position if value != 0 else self.index + 3
            elif operation == 6:
                value = self.get_value(1, code)
                position = self.get_value(2, code)
                self.index = position if value == 0 else self.index + 3
            elif operation == 7:
                value1 = self.get_value(1, code)
                value2 = self.get_value(2, code)
                result = 1 if value1 < value2 else 0
                self.set_value(3, result, code)
                self.index += 4
            elif operation == 8:
                value1 = self.get_value(1, code)
                value2 = self.get_value(2, code)
                result = 1 if value1 == value2 else 0
                self.set_value(3, result, code)
                self.index += 4
            elif operation == 9:
                self.relative_base += self.get_value(1, code)
                self.index += 2
            elif operation == 99:
                self.finished = True
            else:
                raise ValueError(f'Unexpected optcode {operation}')


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()


if __name__ == '__main__':
    solver()
