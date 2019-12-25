from typing import List


def shuffle(instructions: List[str], deck_size, shuffles, what_is_in_the_position=None, where_is_card=None):
    a, b = 1, 0
    for instruction in instructions:
        if instruction.startswith('deal into new stack'):
            a, b = -a % deck_size, (deck_size - 1 - b) % deck_size
        elif instruction.startswith('cut'):
            diff = int(instruction.split()[-1])
            a, b = a, (b - diff) % deck_size
        elif instruction.startswith('deal with increment'):
            diff = int(instruction.split()[-1])
            a, b = a * diff % deck_size, b * diff % deck_size

    r = (b * pow(1 - a, deck_size - 2, deck_size)) % deck_size

    if what_is_in_the_position:
        return ((what_is_in_the_position - r) * pow(a, shuffles * (deck_size - 2), deck_size) + r) % deck_size
    if where_is_card:
        return ((where_is_card - r) * pow(a, shuffles, deck_size) + r) % deck_size


def solver():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        print('Part 1:', shuffle(lines, 10007, 1, where_is_card=2019))
        print('Part 2:', shuffle(lines, 119315717514047, 101741582076661, what_is_in_the_position=2020))


if __name__ == '__main__':
    solver()
