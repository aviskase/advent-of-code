from math import atan2, isclose, dist


def is_blocking(suspect, a, b):
    return isclose(dist(a, suspect) + dist(b, suspect), dist(a, b))


def in_direct_sight(center, points):
    can_see = []
    for point in points:
        if point == center:
            continue
        no_blocks = True
        for suspect in points:
            if suspect == center or suspect == point:
                continue
            if is_blocking(suspect, center, point):
                no_blocks = False
                break
        if no_blocks:
            can_see.append(point)
    return can_see


def extract_coordinates(raw_data):
    return [
        (x, y)
        for y, row in enumerate(raw_data)
        for x, column in enumerate(row)
        if column == '#'
    ]


def find_center(coordinates):
    return max(coordinates, key=lambda p: len(in_direct_sight(p, coordinates)))


def convert_to_relative_map(center, coordinates):
    return [
        (point[0]-center[0], point[1]-center[1])
        for point in coordinates
    ]


def solver():
    with open('input.txt', 'r') as f:
        coordinates = extract_coordinates(f.readlines())
        center = find_center(coordinates)
        print(len(in_direct_sight(center, coordinates)))


if __name__ == '__main__':
    solver()
