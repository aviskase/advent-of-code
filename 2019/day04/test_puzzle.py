from day04.puzzle import is_valid


def test_is_valid():
    assert is_valid(112233)


def test_is_valid_with_groups():
    assert is_valid(111122)


def test_invalid_decreasing():
    assert not is_valid(223450)


def test_invalid_no_double():
    assert not is_valid(123789)


def test_invalid_large_group():
    assert not is_valid(123444)


def test_invalid_odd_group():
    assert not is_valid(367777)
