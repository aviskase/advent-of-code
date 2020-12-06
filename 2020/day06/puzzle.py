def count_yes(answers):
    return len(set((answers.replace('\n', ''))))


def solver():
    with open('input.txt', 'r') as f:
        raw_input = f.read().strip()
        groups = raw_input.split('\n\n')
        print('Part 1:', sum(count_yes(g) for g in groups))  # 6504
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
