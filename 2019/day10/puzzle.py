from math import atan2, isclose, dist, degrees


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
        if point != center
    ]




def calculate_angles(points):
    return [(degrees(atan2(*point)), point) for point in points]


def sort_right_quadrant(points):
    return sorted([p for p in points if p[0] >= 0], key=lambda p: p[0], reverse=True)


def sort_left_quadrant(points):
    return sorted([p for p in points if p[0] < 0], key=lambda p: p[0], reverse=True)


def solver():
    with open('input.txt', 'r') as f:
        coordinates = extract_coordinates(f.readlines())
        center = find_center(coordinates)
        coordinates = convert_to_relative_map(center, coordinates)
        first_sight = in_direct_sight((0, 0), coordinates)
        print('Part 1:', len(first_sight))
        angles = calculate_angles(first_sight)
        right = sort_right_quadrant(angles)
        left_to_find = 200 - len(right)
        left = sort_left_quadrant(angles)
        found = left[left_to_find-1][1]
        result = (found[0] + center[0])*100 + (center[1] + found[1])
        print('Part 2:', result)


if __name__ == '__main__':
    solver()
