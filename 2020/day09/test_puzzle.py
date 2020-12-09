from .puzzle import find_first_invalid

data = [int(x) for x in '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576
'''.strip().splitlines()]


def test_find_first_invalid():
    assert find_first_invalid(data, 5) == 127

