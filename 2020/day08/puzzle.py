from typing import List, NamedTuple

Command = NamedTuple('Command', [('cmd', str), ('num', int)])
TCommands = List[Command]


def parse_commands(lines: List[str]) -> TCommands:
    return [
        Command(line[:line.index(' ')], int(line[line.index(' ')+1:]))
        for line in lines
    ]


def accumulator_before_loop(commands: TCommands) -> int:
    visited = set()
    accumulator = 0
    current = 0
    while True:
        if current in visited:
            return accumulator
        visited.add(current)
        if commands[current].cmd == 'acc':
            accumulator += commands[current].num
            current += 1
        elif commands[current].cmd == 'jmp':
            current += commands[current].num
        else:
            current += 1


def solver():
    with open('input.txt', 'r') as f:
        raw_data = f.read().strip().splitlines()
        commands = parse_commands(raw_data)
        print('Part 1:', accumulator_before_loop(commands))  # 1818
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
