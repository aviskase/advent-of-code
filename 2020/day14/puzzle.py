from itertools import product
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


def execute_program2(program: List[str]) -> TMemory:
    memory = {}
    mask_ones = None
    mask_floating_positions = None
    mask_floating = None
    for cmd in program:
        if cmd.startswith('mask = '):
            mask = list(reversed(cmd.replace('mask = ', '')))
            mask_ones = [i for i, m in enumerate(mask) if m == '1']
            mask_floating_positions = [i for i, m in enumerate(mask) if m == 'X']
            mask_floating = list(product([0, 1], repeat=mask.count('X')))
        else:
            addr, value = cmd.split('] = ')
            addr = int(addr.replace('mem[', ''))
            for i in mask_ones:
                addr = set_bit(addr, i, 1)
            for cur_mask in mask_floating:
                floating_addr = addr
                for p, m in zip(mask_floating_positions, cur_mask):
                    floating_addr = set_bit(floating_addr, p, m)
                memory[floating_addr] = int(value)
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
        print('Part 2:', memory_sum(execute_program2(raw_program)))  # 3278997609887


if __name__ == '__main__':
    solver()
