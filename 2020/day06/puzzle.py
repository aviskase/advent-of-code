def count_any_yes(answers):
    return len(set((answers.replace('\n', ''))))


def count_all_yes(answers):
    return len(set.intersection(*[set(a) for a in answers.split('\n')]))


def solver():
    with open('input.txt', 'r') as f:
        raw_input = f.read().strip()
        groups = raw_input.split('\n\n')
        print('Part 1:', sum(count_any_yes(g) for g in groups))  # 6504
        print('Part 2:', sum(count_all_yes(g) for g in groups))  # 3351


if __name__ == '__main__':
    solver()
