from .puzzle import instructions_to_coordinates, line_to_instruction, find_intersections, find_closest, find_fastest


def test_find_intersection():
    a = instructions_to_coordinates(line_to_instruction('R8,U5,L5,D3'))
    b = instructions_to_coordinates(line_to_instruction('U7,R6,D4,L4'))
    assert find_intersections(a, b) == {(3, 3), (6, 5)}


def test_find_closest():
    a = instructions_to_coordinates(line_to_instruction('R8,U5,L5,D3'))
    b = instructions_to_coordinates(line_to_instruction('U7,R6,D4,L4'))
    assert find_closest(find_intersections(a, b)) == 6


def test_find_fastest():
    a = instructions_to_coordinates(line_to_instruction('R8,U5,L5,D3'))
    b = instructions_to_coordinates(line_to_instruction('U7,R6,D4,L4'))
    assert find_fastest(find_intersections(a, b)) == 30
