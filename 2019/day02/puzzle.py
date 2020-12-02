from typing import List


def execute_program(intcodes: List[int]):
    intcodes_result = intcodes.copy()
    index = 0
    current_code = intcodes_result[index]
    while current_code != 99:
        value_1 = intcodes_result[intcodes_result[index+1]]
        value_2 = intcodes_result[intcodes_result[index+2]]
        position = intcodes_result[index+3]
        if current_code == 1:
            intcodes_result[position] = value_1 + value_2
        elif current_code == 2:
            intcodes_result[position] = value_1 * value_2
        else:
            raise ValueError(f'Unexpected intcode {current_code}')
        index += 4
        current_code = intcodes_result[index]
    return intcodes_result


def solver():
    with open('input.txt', 'r') as f:
        program = [int(intcode) for intcode in f.readline().split(',')]
        for noun in range(100):
            for verb in range(100):
                program[1] = noun
                program[2] = verb
                result = execute_program(program)
                if result[0] == 19690720:
                    print(f'{noun=}, {verb=}')
                    print('Result:', 100 * noun + verb)
                    exit()


if __name__ == '__main__':
    solver()
