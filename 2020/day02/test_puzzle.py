from .puzzle import valid

data = [
    ['1-3 a', 'abcde'],
    ['1-3 b', 'cdefg'],
    ['2-9 c', 'ccccccccc'],
]


def test_valid():
    assert {'abcde', 'ccccccccc'} == set(valid(data))

