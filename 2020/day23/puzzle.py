from __future__ import annotations

from dataclasses import dataclass
from operator import mul
from typing import Optional, List


@dataclass
class Cup:
    data: Optional[int]
    next: Cup = None


class Cups:
    def __init__(self, data: List[int]):
        self.head = Cup(None)
        self.head.next = self.head
        current = self.head
        self.index = {}
        for d in data:
            cup = Cup(d)
            current = self.insert_after(current, cup)
            self.index[d] = current

    def insert_after(self, after_cup: Cup, inserted_cup: Cup) -> Cup:
        inserted_cup.next = after_cup.next
        after_cup.next = inserted_cup
        self.index[inserted_cup.data] = inserted_cup
        return inserted_cup

    def remove_after(self, after_cup: Cup) -> Cup:
        if after_cup.next == self.head:
            cup = self.head.next
            self.head.next = cup.next
        else:
            cup = after_cup.next
            after_cup.next = cup.next
        del self.index[cup.data]
        return Cup(cup.data)

    def __iter__(self):
        current = self.head.next
        while True:
            if current is not self.head:
                yield current
            current = current.next

    def data(self):
        data = []
        current = self.head.next
        while current != self.head:
            data.append(current.data)
            current = current.next
        return data

    def find(self, data):
        return self.index.get(data, None)

    def find_destination_cup(self, destination):
        while destination >= 0:
            if destination in self.index:
                return self.index[destination]
            destination -= 1

        max_cup = max(self.index)
        return self.index[max_cup]


def play_game(data: str, moves: int) -> str:
    cups = Cups([int(d) for d in data])
    it = iter(cups)
    for move in range(moves):
        current = next(it)
        a = cups.remove_after(current)
        b = cups.remove_after(current)
        c = cups.remove_after(current)
        destination = cups.find_destination_cup(current.data - 1)
        a = cups.insert_after(destination, a)
        b = cups.insert_after(a, b)
        cups.insert_after(b, c)
    result = cups.data()
    cup_1 = result.index(1)
    return ''.join(str(x) for x in result[cup_1+1:] + result[:cup_1])


def play_game2(data) -> (int, int):
    start_data = [int(d) for d in data]
    max_cup = max(start_data)
    additional_data = [x for x in range(max_cup+1, 1000001)]
    cups = Cups([int(d) for d in start_data+additional_data])
    it = iter(cups)
    for move in range(10000000):
        current = next(it)
        a = cups.remove_after(current)
        b = cups.remove_after(current)
        c = cups.remove_after(current)
        destination = cups.find_destination_cup(current.data - 1)
        a = cups.insert_after(destination, a)
        b = cups.insert_after(a, b)
        cups.insert_after(b, c)
    cup_1 = cups.find(1)
    a = cup_1.next
    return a.data, a.next.data


def solver():
    with open('input.txt', 'r') as f:
        data = f.read().strip()
        print('Part 1:', play_game(data, 100))  # 34952786
        print('Part 2:', mul(*play_game2(data)))  # 505334281774


if __name__ == '__main__':
    solver()
