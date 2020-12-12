from typing import List


def move_ship(raw_commands: List[str]) -> (int, int):
    x = y = 0
    direction = 0  # clock-wise
    for raw_cmd in raw_commands:
        cmd = raw_cmd[0]
        value = int(raw_cmd[1:])
        if cmd == 'N':
            y += value
        elif cmd == 'S':
            y -= value
        elif cmd == 'E':
            x += value
        elif cmd == 'W':
            x -= value
        elif cmd == 'F':
            if direction == 0:
                x += value
            elif direction == 90:
                y -= value
            elif direction == 180:
                x -= value
            else:
                y += value
        elif cmd == 'L':
            direction = (360 - value + direction) % 360
        elif cmd == 'R':
            direction = (direction + value) % 360
    return x, y


def mdistance(x: int, y: int) -> int:
    return abs(x) + abs(y)


def solver():
    with open('input.txt', 'r') as f:
        raw_commands = f.read().strip().splitlines()
        print('Part 1:', mdistance(*move_ship(raw_commands)))  # 1589
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
