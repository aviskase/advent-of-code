from .puzzle import valid, valid2

data = [
    ['1-3 a', 'abcde'],
    ['1-3 b', 'cdefg'],
    ['2-9 c', 'ccccccccc'],
]


def test_valid():
    assert {'abcde', 'ccccccccc'} == set(valid(data))

def test_valid2():
    assert {'abcde'} == set(valid2(data))
