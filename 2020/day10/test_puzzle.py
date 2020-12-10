import pytest

from .puzzle import find_differences, count_arrangements

my_data = [1, 4, 5]

data = [int(x) for x in '''16
10
15
5
1
11
7
19
6
12
4
'''.strip().splitlines()]

second_data = [int(x) for x in '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
'''.strip().splitlines()]


@pytest.mark.parametrize('d, expected1, expected3', [(data, 7, 5), (second_data, 22, 10)])
def test_find_differences(d, expected1, expected3):
    diff = find_differences(d)
    assert diff.get(1) == expected1
    assert diff.get(3) == expected3


@pytest.mark.parametrize('d, expected', [(my_data, 1), (data, 8), (second_data, 19208)])
def test_count_arrangements(d, expected):
    assert count_arrangements(d) == expected
