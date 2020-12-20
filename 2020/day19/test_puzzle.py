import pytest

from .puzzle import parse, find_valid

data0 = '''
0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"

aab
aba
abb
'''.strip()


data1 = '''
0: 1 2
1: "a"
2: 1 3 | 3 1
3: 4
4: "b"

aab
aba
abb
'''.strip()

data2 = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
'''.strip()


@pytest.mark.parametrize('d, expected', [
    (data0, ['aab', 'aba']),
    (data1, ['aab', 'aba']),
    (data2, ['ababbb', 'abbbab'])
])
def test_find_valid(d, expected):
    rule, messages = parse(d)
    assert find_valid(rule, messages) == expected


