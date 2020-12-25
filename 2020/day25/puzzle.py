MODULO = 20201227


def find_loop_size(public_key: int, subject_number: int = 7) -> int:
    key = 1
    loop_size = 0
    while key != public_key:
        loop_size += 1
        key = (key * subject_number) % MODULO
    return loop_size


def calculate_key(subject_number: int, loop_size: int) -> int:
    key = 1
    for _ in range(loop_size):
        key = (key * subject_number) % MODULO
    return key


def solver():
    with open('input.txt', 'r') as f:
        card, door = f.read().strip().splitlines()
        card = int(card.strip())
        door = int(door.strip())
        print('Part 1:', calculate_key(card, find_loop_size(door)))  # 16902792


if __name__ == '__main__':
    solver()
