from typing import List
from itertools import permutations, cycle, repeat


def unpack_code(raw_code):
    data = f'{raw_code:05}'
    code = int(data[-2:])
    modes = list(map(int, data[-3::-1]))
    return code, modes


def get_value(cell, mode, program):
    if mode == 1:
        return cell
    if mode == 0:
        return program[cell]


def inputs_generator(available_inputs):
    for i in available_inputs:
        yield i
    yield from repeat(available_inputs[-1])


def execute_program(intcodes: List[int], inputs, index=0, exit_on_output=False):
    intcodes_result = intcodes.copy()
    outputs = []
    current_code, current_modes = unpack_code(intcodes_result[index])
    while current_code != 99:
        if current_code == 1:
            value1 = get_value(intcodes_result[index + 1], current_modes[0], intcodes_result)
            value2 = get_value(intcodes_result[index + 2], current_modes[1], intcodes_result)
            position = intcodes_result[index + 3]
            intcodes_result[position] = value1 + value2
            index += 4
        elif current_code == 2:
            value1 = get_value(intcodes_result[index + 1], current_modes[0], intcodes_result)
            value2 = get_value(intcodes_result[index + 2], current_modes[1], intcodes_result)
            position = intcodes_result[index + 3]
            intcodes_result[position] = value1 * value2
            index += 4
        elif current_code == 3:
            position = intcodes_result[index + 1]
            intcodes_result[position] = next(inputs)
            index += 2
        elif current_code == 4:
            cell = intcodes_result[index + 1]
            output_value = get_value(cell, current_modes[0], intcodes_result)
            index += 2
            if exit_on_output:
                return [output_value], intcodes_result, index
            outputs.append(output_value)
        elif current_code == 5:
            value = get_value(intcodes_result[index + 1], current_modes[0], intcodes_result)
            position = get_value(intcodes_result[index + 2], current_modes[1], intcodes_result)
            index = position if value != 0 else index + 3
        elif current_code == 6:
            value = get_value(intcodes_result[index + 1], current_modes[0], intcodes_result)
            position = get_value(intcodes_result[index + 2], current_modes[1], intcodes_result)
            index = position if value == 0 else index + 3
        elif current_code == 7:
            value1 = get_value(intcodes_result[index + 1], current_modes[0], intcodes_result)
            value2 = get_value(intcodes_result[index + 2], current_modes[1], intcodes_result)
            position = intcodes_result[index + 3]
            intcodes_result[position] = 1 if value1 < value2 else 0
            index += 4
        elif current_code == 8:
            value1 = get_value(intcodes_result[index + 1], current_modes[0], intcodes_result)
            value2 = get_value(intcodes_result[index + 2], current_modes[1], intcodes_result)
            position = intcodes_result[index + 3]
            intcodes_result[position] = 1 if value1 == value2 else 0
            index += 4
        else:
            raise ValueError(f'Unexpected intcode {current_code}')
        current_code, current_modes = unpack_code(intcodes_result[index])
    return intcodes_result, outputs


def run_engines(phases, program):
    input_data = 0
    for phase in phases:
        _, outputs = execute_program(program,  inputs_generator([phase, input_data]))
        input_data = outputs[0]
    return input_data


def run_engines_with_feedback(phases, program):
    input_data = [0]
    engines = []
    for phase in phases:
        output_value, intcodes_result, index = execute_program(
            program,  inputs_generator([phase, *input_data]), 0, True
        )
        engines.append({'program': list(intcodes_result), 'index': index})
        input_data = output_value
    i = 0
    e_outs = []
    while True:
        engine = engines[i]
        result = execute_program(
            engine['program'], inputs_generator(input_data), engine['index'], True
        )
        if len(result) == 2:
            _, outputs = result
            if i == 4:
                e_outs.extend(outputs)
                return e_outs[-1]
            output_value = outputs
        else:
            output_value, intcodes_result, index = result
            engines[i] = {'program': list(intcodes_result), 'index': index}
        input_data = output_value
        if i == 4:
            e_outs.extend(output_value)
        i += 1
        if i == 5:
            i = 0


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
