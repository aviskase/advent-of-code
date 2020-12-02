from typing import List


def valid(rules: List[List[str]]) -> List[str]:
    valid_passwords = []
    for [rule, password] in rules:
        numbers, letter = rule.split(' ')
        a, b = numbers.split('-')
        if int(a) <= password.count(letter) <= int(b):
            valid_passwords.append(password)
    return valid_passwords


def solver():
    with open('input.txt', 'r') as f:
        rules = [line.split(': ') for line in f.readlines()]
        print('Part 1:', len(valid(rules)))
        # print('Part 2:', )


if __name__ == '__main__':
    solver()
