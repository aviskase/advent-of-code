from typing import List


def compare_by_count(a, b, letter, password):
    return a <= password.count(letter) <= b


def compare_by_position(a, b, letter, password):
    return (password[a-1] == letter and password[b-1] != letter) or (password[a-1] != letter and password[b-1] == letter)


def valid(rules: List[List[str]], comparator) -> List[str]:
    valid_passwords = []
    for [rule, password] in rules:
        numbers, letter = rule.split(' ')
        a, b = map(lambda x: int(x), numbers.split('-'))
        if comparator(a, b, letter, password):
            valid_passwords.append(password)
    return valid_passwords


def solver():
    with open('input.txt', 'r') as f:
        rules = [line.split(': ') for line in f.readlines()]
        print('Part 1:', len(valid(rules, compare_by_count)))
        print('Part 1:', len(valid(rules, compare_by_position)))


if __name__ == '__main__':
    solver()
