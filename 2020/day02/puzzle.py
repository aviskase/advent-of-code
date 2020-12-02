from typing import List


def valid(rules: List[List[str]]) -> List[str]:
    valid_passwords = []
    for [rule, password] in rules:
        numbers, letter = rule.split(' ')
        a, b = map(lambda x: int(x), numbers.split('-'))
        if a <= password.count(letter) <= b:
            valid_passwords.append(password)
    return valid_passwords


def valid2(rules: List[List[str]]) -> List[str]:
    valid_passwords = []
    for [rule, password] in rules:
        numbers, letter = rule.split(' ')
        a, b = map(lambda x: int(x) - 1, numbers.split('-'))
        if (password[a] == letter and password[b] != letter) or (password[a] != letter and password[b] == letter):
            valid_passwords.append(password)
    return valid_passwords


def solver():
    with open('input.txt', 'r') as f:
        rules = [line.split(': ') for line in f.readlines()]
        print('Part 1:', len(valid(rules)))
        print('Part 1:', len(valid2(rules)))


if __name__ == '__main__':
    solver()
