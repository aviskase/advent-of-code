def is_valid(password):
    password = list(map(int, str(password)))
    prev = None
    group_count = 1
    groups = set()
    for digit in password:
        if prev is not None and digit < prev:
            return False
        if digit == prev:
            group_count += 1
        else:
            groups.add(group_count == 2)
            group_count = 1
        prev = digit
    groups.add(group_count == 2)
    return any(groups)


def count_valid(start, end):
    valids = [password for password in range(start, end + 1) if is_valid(password)]
    from pprint import pprint as pp
    pp(valids)
    return len(valids)


def solver():
    start = 367479
    end = 893698
    print('Num of valids:', count_valid(start, end))


if __name__ == '__main__':
    solver()
