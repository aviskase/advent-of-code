from typing import Dict, List

TMemory = Dict[int, int]


def execute_program(program: List[str]) -> TMemory:
    memory = {}
    mask = None
    for cmd in program:
        if cmd.startswith('mask = '):
            mask = [(i, int(m)) for i, m in enumerate(reversed(cmd.replace('mask = ', ''))) if m != 'X']
        else:
            addr, value = cmd.split('] = ')
            addr = int(addr.replace('mem[', ''))
            value = int(value)
            for i, m in mask:
                value = set_bit(value, i, m)
            memory[addr] = value
    return memory


def set_bit(num, offset, bit_value):
    if bit_value == 1:
        mask = 1 << offset
        return num | mask
    mask = ~(1 << offset)
    return num & mask


def memory_sum(memory: TMemory) -> int:
    return sum(memory.values())


def solver():
    with open('input.txt', 'r') as f:
        raw_program = f.read().strip().splitlines()
        print('Part 1:', memory_sum(execute_program(raw_program)))  # 13496669152158
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
