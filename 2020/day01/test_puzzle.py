from .puzzle import find_2020


def test_find_2020():
    data = [1721, 979, 366, 299, 675, 1456]
    a, b = find_2020(data)
    print(a, b)
    assert {1721, 299} == {a, b}
