from collections import deque, defaultdict
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


def network(program):
    size = 50
    computers = []
    inputs = [deque() for _ in range(size)]
    default_input = -1
    for i in range(size):
        computer = IntcodeComputer.from_string(program)
        task = computer.execute()
        computers.append(task)
        next(task)
        v = task.send(i)
        assert v is None

    while True:
        for i in range(size):
            computer = computers[i]
            if inputs[i]:
                assert len(inputs[i]) >= 2
                output = computer.send(inputs[i].popleft())
                assert output is None
                output = computer.send(inputs[i].popleft())
            else:
                output = computer.send(default_input)
            while output is not None:
                address = output
                x = next(computer)
                y = next(computer)
                output = next(computer)
                if address == 255:
                    return x, y
                inputs[address].append(x)
                inputs[address].append(y)


def network_with_nat(program):
    size = 50
    computers = []
    inputs = [deque() for _ in range(size)]
    default_input = -1
    for i in range(size):
        computer = IntcodeComputer.from_string(program)
        task = computer.execute()
        computers.append(task)
        next(task)
        v = task.send(i)
        assert v is None

    nat = [-1, -1]
    last_nat = nat
    while True:
        for i in range(size):
            computer = computers[i]
            if inputs[i]:
                assert len(inputs[i]) >= 2
                output = computer.send(inputs[i].popleft())
                assert output is None
                output = computer.send(inputs[i].popleft())
            else:
                output = computer.send(default_input)
            while output is not None:
                address = output
                x = next(computer)
                y = next(computer)
                output = next(computer)
                if address == 255:
                    nat = [x, y]
                else:
                    inputs[address].append(x)
                    inputs[address].append(y)
        if any(inputs):
            continue
        if nat[1] == last_nat[1]:
            return nat[1]
        last_nat = nat
        inputs[0].extend(nat)


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        print('Part 1:', network(line)[-1])
        print('Part 2:', network_with_nat(line))


if __name__ == '__main__':
    solver()
