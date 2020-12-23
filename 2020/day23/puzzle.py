from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cup:
    data: Optional[int]
    next: Cup = None


class Cups:
    def __init__(self, data):
        self.head = Cup(None)
        self.head.next = self.head
        current = self.head
        for d in data:
            cup = Cup(d)
            self.insert_after(current, cup)
            current = cup

    def insert_after(self, after_cup: Cup, inserted_cup: Cup) -> Cup:
        inserted_cup.next = after_cup.next
        after_cup.next = inserted_cup
        return inserted_cup

    def remove_after(self, after_cup: Cup) -> Cup:
        if after_cup.next == self.head:
            cup = self.head.next
            self.head.next = cup.next
        else:
            cup = after_cup.next
            after_cup.next = cup.next
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
        current = self.head.next
        while current != self.head:
            if current.data == data:
                return current
            current = current.next
        return None

    def find_destination_cup(self, destination):
        while destination >= 0:
            cup = self.find(destination)
            if cup:
                return cup
            destination -= 1

        current = self.head.next
        max_cup = current
        while current != self.head:
            if current.data > max_cup.data:
                max_cup = current
            current = current.next
        return max_cup


def play_game(data: str, moves: int) -> str:
    cups = Cups(int(d) for d in data)
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


def solver():
    with open('input.txt', 'r') as f:
        data = f.read().strip()
        print('Part 1:', play_game(data, 100))  # 34952786
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
