from .puzzle import find_2020, find3_2020

data = [1721, 979, 366, 299, 675, 1456]


def test_find_2020():
    a, b = find_2020(data)
    assert {1721, 299} == {a, b}


def test_find3_202():
    a, b, c = find3_2020(data)
    assert {979, 366, 675} == {a, b, c}
