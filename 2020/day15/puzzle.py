from typing import List


def num_at_round(nums: List[int], end_round: int) -> int:
    rounds = {n: {'last': i} for i, n in enumerate(nums)}
    prev_num = nums[-1]
    for r in range(len(nums), end_round):
        last_used = rounds[prev_num].get('last')
        prev_used = rounds[prev_num].get('prev')
        if prev_used is None:
            new_num = 0
        else:
            new_num = last_used - prev_used
        if new_num not in rounds:
            rounds[new_num] = {}
        rounds[new_num]['prev'] = rounds[new_num].get('last', None)
        rounds[new_num]['last'] = r
        prev_num = new_num
    return prev_num


def solver():
    with open('input.txt', 'r') as f:
        numbers = [int(x) for x in f.read().strip().split(',')]
        print('Part 1:', num_at_round(numbers, 2020))  # 1618
        print('Part 2:', num_at_round(numbers, 30000000))  #


if __name__ == '__main__':
    solver()
