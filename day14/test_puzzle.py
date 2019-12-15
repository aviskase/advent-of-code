import pytest
from day14.puzzle import parse_data, calculate_fuel

f0 = """10 ORE => 10 A
1 ORE => 1 B
1 ORE, 2 B => 2 C
2 A, 3 C => 1 FUEL"""

f1 = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

f2 = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""


@pytest.mark.parametrize('data, result', [
    (f0.split('\n'), 16),
    (f1.split('\n'), 31),
    (f2.split('\n'), 165),
])
def test_calculate_ore(data, result):
    assert calculate_fuel(parse_data(data)) == result
