from collections import deque
from typing import List

THand = List[int]


def parse(raw_data: str) -> (THand, THand):
    player_1, player_2 = raw_data.split('\n\n', 2)
    player_1 = [int(card) for card in player_1.strip().splitlines()[1:]]
    player_2 = [int(card) for card in player_2.strip().splitlines()[1:]]
    return player_1, player_2


def play_drunkard(player_1: THand, player_2: THand) -> (THand, int):
    cur_1 = deque(player_1)
    cur_2 = deque(player_2)
    while len(cur_1) and len(cur_2):
        card_1 = cur_1.popleft()
        card_2 = cur_2.popleft()
        if card_1 > card_2:
            cur_1.append(card_1)
            cur_1.append(card_2)
        else:
            cur_2.append(card_2)
            cur_2.append(card_1)
    if len(cur_1):
        return list(cur_1), 1
    return list(cur_2), 2


def play_drunkard_recursive(player_1: THand, player_2: THand) -> (THand, int):
    cur_1 = deque(player_1)
    cur_2 = deque(player_2)
    rounds = []
    while len(cur_1) and len(cur_2):
        if (list(cur_1), list(cur_2)) in rounds:
            return list(cur_1), 1
        rounds.append((list(cur_1), list(cur_2)))
        card_1 = cur_1.popleft()
        card_2 = cur_2.popleft()
        if card_1 <= len(cur_1) and card_2 <= len(cur_2):
            _, winner = play_drunkard_recursive(list(cur_1)[:card_1], list(cur_2)[:card_2])
        else:
            winner = 1 if card_1 > card_2 else 2
        if winner == 1:
            cur_1.append(card_1)
            cur_1.append(card_2)
        else:
            cur_2.append(card_2)
            cur_2.append(card_1)
    if len(cur_1):
        return list(cur_1), 1
    return list(cur_2), 2


def score(player: THand) -> int:
    return sum(i * c for i, c in enumerate(reversed(player), 1))


def solver():
    with open('input.txt', 'r') as f:
        p1, p2 = parse(f.read().strip())
        winner_hand, winner_id = play_drunkard(p1, p2)
        print('Part 1:', score(winner_hand))  # 33403
        winner_hand, winner_id = play_drunkard_recursive(p1, p2)
        print('Part 2:', score(winner_hand))  # 29177


if __name__ == '__main__':
    solver()
