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


def find_highest_seat_id(boarding_passes):
    max_id = 0
    for boarding_pass in boarding_passes:
        seat_id = find_row(boarding_pass) * 8 + find_column(boarding_pass)
        if seat_id > max_id:
            max_id = seat_id
    return max_id


def solver():
    with open('input.txt', 'r') as f:
        boarding_passes = f.read().strip().splitlines()
        print('Part 1:', find_highest_seat_id(boarding_passes))
        # print('Part 2:', )


if __name__ == '__main__':
    solver()
