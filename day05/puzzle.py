from typing import List


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


def execute_program(intcodes: List[int], default_input):
    intcodes_result = intcodes.copy()
    outputs = []
    index = 0
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
            intcodes_result[position] = default_input
            index += 2
        elif current_code == 4:
            cell = intcodes_result[index + 1]
            outputs.append(get_value(cell, current_modes[0], intcodes_result))
            index += 2
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


def solver():
    with open('input.txt', 'r') as f:
        program = [int(intcode) for intcode in f.readline().split(',')]
        _, outputs = execute_program(program, 1)
        print(outputs)
        _, outputs = execute_program(program, 5)
        print(outputs)


if __name__ == '__main__':
    solver()
