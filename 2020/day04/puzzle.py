
REQ_FIELDS = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
]
OPT_FIELDS = ['cid']


def count_valid_passports(raw_input):
    passports = raw_input.split('\n\n')
    total = 0
    for passport in passports:
        cleaned = passport.replace('\n', ' ')
        if all([f'{f}:' in cleaned for f in REQ_FIELDS]):
            total += 1
    return total


def solver():
    with open('input.txt', 'r') as f:
        raw_input = f.read()
        print('Part 1:', count_valid_passports(raw_input))
        # print('Part 2:', )


if __name__ == '__main__':
    solver()
