from typing import List
from itertools import permutations, repeat


class IntcodeComputer:
    relative_base = 0
    index = 0

    def __init__(self, program: List[int]):
        self.program = program.copy()
        self.finished = False

    @staticmethod
    def unpack_code(raw_code):
        data = f'{raw_code:05}'
        code = int(data[-2:])
        modes = list(map(int, data[-3::-1]))
        return code, modes

    def get_value(self, cell, mode):
        if mode == 0:
            return self.program[cell]
        if mode == 1:
            return cell
        if mode == 2:
            return self.program[self.relative_base + cell]

    def execute(self, input_data, exit_on_output=False):
        outputs = []
        inputs = self.inputs_generator(input_data)
        ready_to_exit = False
        while not ready_to_exit:
            current_code, current_modes = self.unpack_code(self.program[self.index])
            if current_code == 1:
                value1 = self.get_value(self.program[self.index + 1], current_modes[0])
                value2 = self.get_value(self.program[self.index + 2], current_modes[1])
                position = self.program[self.index + 3]
                self.program[position] = value1 + value2
                self.index += 4
            elif current_code == 2:
                value1 = self.get_value(self.program[self.index + 1], current_modes[0])
                value2 = self.get_value(self.program[self.index + 2], current_modes[1])
                position = self.program[self.index + 3]
                self.program[position] = value1 * value2
                self.index += 4
            elif current_code == 3:
                position = self.program[self.index + 1]
                self.program[position] = next(inputs)
                self.index += 2
            elif current_code == 4:
                cell = self.program[self.index + 1]
                output_value = self.get_value(cell, current_modes[0])
                self.index += 2
                outputs.append(output_value)
                ready_to_exit = exit_on_output
            elif current_code == 5:
                value = self.get_value(self.program[self.index + 1], current_modes[0])
                position = self.get_value(self.program[self.index + 2], current_modes[1])
                self.index = position if value != 0 else self.index + 3
            elif current_code == 6:
                value = self.get_value(self.program[self.index + 1], current_modes[0])
                position = self.get_value(self.program[self.index + 2], current_modes[1])
                self.index = position if value == 0 else self.index + 3
            elif current_code == 7:
                value1 = self.get_value(self.program[self.index + 1], current_modes[0])
                value2 = self.get_value(self.program[self.index + 2], current_modes[1])
                position = self.program[self.index + 3]
                self.program[position] = 1 if value1 < value2 else 0
                self.index += 4
            elif current_code == 8:
                value1 = self.get_value(self.program[self.index + 1], current_modes[0])
                value2 = self.get_value(self.program[self.index + 2], current_modes[1])
                position = self.program[self.index + 3]
                self.program[position] = 1 if value1 == value2 else 0
                self.index += 4
            elif current_code == 9:
                self.relative_base = self.get_value(self.program[self.index + 1], current_modes[0])
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
        program = [int(intcode) for intcode in f.readline().split(',')]
        max_result = -1
        phase_result = []
        for phases in permutations(range(5)):
            result = run_engines(phases, program)
            if result > max_result:
                max_result = result
                phase_result = list(phases)
        print('Base engine: ', max_result, ' - ', phase_result)

        max_result = -1
        phase_result = []
        for phases in permutations(range(5, 10)):
            result = run_engines_with_feedback(phases, program)
            if result > max_result:
                max_result = result
                phase_result = list(phases)
        print('Feedback engine: ', max_result, ' - ', phase_result)


if __name__ == '__main__':
    solver()
