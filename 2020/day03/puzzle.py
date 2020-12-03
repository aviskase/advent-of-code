

def map_trees(lines):
    return [
        list(map(lambda x: x == '#', list(line.strip())))
        for line in lines
    ]


SLOPE_RIGHT = 3
SLOPE_DOWN = 1


def find_trees(trees):
    start_y = 0
    start_x = 0
    max_x = len(trees[0]) - 1
    current_x = start_x
    num_of_trees = 0
    for y in range(start_y, len(trees), SLOPE_DOWN):
        if trees[y][current_x]:
            num_of_trees += 1
        current_x += SLOPE_RIGHT
        if current_x > max_x:
            current_x = (current_x % max_x) - 1
    return num_of_trees


def solver():
    with open('input.txt', 'r') as f:
        raw_input = f.readlines()
        print('Part 1:', find_trees(map_trees(raw_input)))
        # print('Part 2:', )


if __name__ == '__main__':
    solver()
