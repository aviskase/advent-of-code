import math

def map_trees(lines):
    return [
        list(map(lambda x: x == '#', list(line.strip())))
        for line in lines
    ]


def find_trees(trees, slope_down, slope_right):
    start_y = 0
    start_x = 0
    max_x = len(trees[0]) - 1
    current_x = start_x
    num_of_trees = 0
    for y in range(start_y, len(trees), slope_down):
        if trees[y][current_x]:
            num_of_trees += 1
        current_x += slope_right
        if current_x > max_x:
            current_x = (current_x % max_x) - 1
    return num_of_trees


def solver():
    with open('input.txt', 'r') as f:
        raw_input = f.readlines()
        trees = map_trees(raw_input)
        print('Part 1:', find_trees(trees, 1, 3))
        slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
        print('Part 2:', math.prod([
            find_trees(trees, *slope)
            for slope in slopes
        ]))


if __name__ == '__main__':
    solver()
