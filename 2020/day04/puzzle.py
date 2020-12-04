import re

REQ_FIELDS = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
]

REQ_FIELDS_STRICT = [
    r'byr:(19[2-9]\d|200[0-2])\s',
    r'iyr:(201\d|2020)\s',
    r'eyr:(202\d|2030)\s',
    r'hgt:((1[5-8]\d|19[0-3])cm|(59|6\d|7[0-6])in)\s',
    r'hcl:#[\da-f]{6}\s',
    r'ecl:(amb|blu|brn|gry|grn|hzl|oth)\s',
    r'pid:\d{9}\s',
]


def count_valid_passports(raw_input):
    passports = raw_input.split('\n\n')
    total = 0
    for passport in passports:
        cleaned = passport.replace('\n', ' ')
        if all((f'{f}:' in cleaned for f in REQ_FIELDS)):
            total += 1
    return total


def strict_count_valid_passports(raw_input):
    passports = raw_input.split('\n\n')
    total = 0
    for passport in passports:
        cleaned = passport.replace('\n', ' ') + ' '
        if all((re.search(p, cleaned) for p in REQ_FIELDS_STRICT)):
            total += 1
    return total


def solver():
    with open('input.txt', 'r') as f:
        raw_input = f.read()
        print('Part 1:', count_valid_passports(raw_input))  # 216
        print('Part 2:', strict_count_valid_passports(raw_input))  # 150


if __name__ == '__main__':
    solver()
