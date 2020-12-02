from typing import List
from itertools import permutations, repeat


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

    def execute(self, input_data=None, exit_on_output=False):
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
                if inputs is None:
                    raise ValueError('Unexpected input optcode with no inputs provided')
                self.set_value(1, next(inputs), current_modes)
                self.index += 2
            elif current_code == 4:
                output_value = self.get_value(1, current_modes)
                self.index += 2
                outputs.append(output_value)
                ready_to_exit = exit_on_output
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

    def resume(self, inputs, exit_on_output=False):
        return self.execute(inputs, exit_on_output)

    @staticmethod
    def inputs_generator(inputs):
        if not isinstance(inputs, list):
            inputs = [inputs]
        for i in inputs:
            yield i
        yield from repeat(inputs[-1])


def run_engines(phases, program):
    input_data = 0
    for phase in phases:
        engine = IntcodeComputer(program)
        outputs = engine.execute([phase, input_data])
        input_data = outputs[0]
    return input_data


def run_engines_with_feedback(phases, program):
    input_data = [0]
    last_engine = len(phases) - 1
    engines = []
    for phase in phases:
        engine = IntcodeComputer(program)
        outputs = engine.execute([phase, *input_data], True)
        engines.append(engine)
        input_data = outputs
    current_engine = 0
    last_engine_outputs = []
    while True:
        engine = engines[current_engine]
        outputs = engine.resume(input_data, True)
        input_data = outputs
        if current_engine == last_engine:
            last_engine_outputs.extend(outputs)
            if engine.finished:
                return last_engine_outputs
        current_engine = 0 if current_engine == last_engine else current_engine + 1


def solver():
    with open('input.txt', 'r') as f:
        line = f.readline()
        part_1 = IntcodeComputer.from_string(line)
        print('Part 1:', part_1.execute(1))
        part_2 = IntcodeComputer.from_string(line)
        print('Part 2:', part_2.execute(2))


if __name__ == '__main__':
    solver()
