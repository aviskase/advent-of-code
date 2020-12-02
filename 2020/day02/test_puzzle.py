from .puzzle import valid, compare_by_count, compare_by_position

data = [
    ['1-3 a', 'abcde'],
    ['1-3 b', 'cdefg'],
    ['2-9 c', 'ccccccccc'],
]


def test_valid_by_count():
    assert {'abcde', 'ccccccccc'} == set(valid(data, compare_by_count))


def test_valid_by_position():
    assert {'abcde'} == set(valid(data, compare_by_position))
