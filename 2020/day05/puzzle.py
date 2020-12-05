def find_place(placepath, bottom_label, max_place):
    place = range(0, max_place+1)
    for p in placepath:
        if p == bottom_label:
            place = place[len(place)//2:]
        else:
            place = place[:len(place)//2]
    return place[0]


def find_row(boarding_pass):
    return find_place(boarding_pass[:7], 'B', 127)


def find_column(boarding_pass):
    return find_place(boarding_pass[7:], 'R', 7)


def all_ids(boarding_passes):
    return sorted([
        find_row(boarding_pass) * 8 + find_column(boarding_pass)
        for boarding_pass in boarding_passes
    ])


def solver():
    with open('input.txt', 'r') as f:
        boarding_passes = f.read().strip().splitlines()
        print('Part 1:', all_ids(boarding_passes)[-1])  # 842
        # print('Part 2:', )


if __name__ == '__main__':
    solver()
