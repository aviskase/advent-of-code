from typing import List, Tuple


def find_2020(expenses: List[int]) -> Tuple[int, int]:
    sorted_expenses = sorted(expenses)
    for first, a in enumerate(sorted_expenses[:-1]):
        for second, b in enumerate(sorted_expenses[first+1:]):
            if a + b == 2020:
                return a, b


def solver():
    with open('input.txt', 'r') as f:
        expenses = [int(expense) for expense in f.readlines()]
        a, b = find_2020(expenses)
        print('Part 1:', a * b)


if __name__ == '__main__':
    solver()
