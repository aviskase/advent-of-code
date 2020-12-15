import operator
from typing import List


def num_at_round(nums: List[int], end_round: int) -> int:
    rounds = nums.copy()
    for r in range(len(nums), end_round):
        prev_num = rounds[-1]
        last_used = rindex(rounds, prev_num)
        prev_used = rindex(rounds[:last_used], prev_num)
        if prev_used != -1:
            rounds.append(last_used - prev_used)
        else:
            rounds.append(0)
    return rounds[-1]


def rindex(lst, value):
    try:
        return len(lst) - operator.indexOf(reversed(lst), value) - 1
    except:
        return -1


def solver():
    with open('input.txt', 'r') as f:
        numbers = [int(x) for x in f.read().strip().split(',')]
        print('Part 1:', num_at_round(numbers, 2020))  # 1618
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
