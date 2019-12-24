from typing import List


def shuffle_deck(deck, instructions):
    new_deck = deck
    l = len(deck)
    for instruction in instructions:
        if instruction.startswith('deal into new stack'):
            new_deck.reverse()
        elif instruction.startswith('cut'):
            size = int(instruction.split()[-1])
            new_deck = new_deck[size:] + new_deck[:size]
        elif instruction.startswith('deal with increment'):
            size = int(instruction.split()[-1])
            temp = [-1] * l
            i = 0
            for d in new_deck:
                temp[i*size % l] = d
                i += 1
            new_deck = temp
    return new_deck


def part_one(lines: List[str]):
    deck_size = 10007
    deck = shuffle_deck(list(range(deck_size)), lines)
    print('Part 1:', deck.index(2019))


def solver():
    with open('input.txt', 'r') as f:
        lines = f.readlines()
        part_one(lines)


if __name__ == '__main__':
    solver()
