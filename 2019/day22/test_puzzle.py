import pytest

from .puzzle import shuffle_deck


@pytest.mark.parametrize('size, instructions, result', [
    (5, ['deal into new stack'], [4, 3, 2, 1, 0]),
    (5, ['cut 1'], [1, 2, 3, 4, 0]),
    (5, ['cut 3'], [3, 4, 0, 1, 2]),
    (5, ['cut -1'], [4, 0, 1, 2, 3]),
    (5, ['cut -3'], [2, 3, 4, 0, 1]),
    (10, ['deal with increment 3'], [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]),
    (10, 'deal with increment 7\ndeal into new stack\ndeal into new stack'.split('\n'), [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]),
    (10, 'cut 6\ndeal with increment 7\ndeal into new stack'.split('\n'), [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]),
    (10, 'deal with increment 7\ndeal with increment 9\ncut -2'.split('\n'), [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]),
    (10, 'deal into new stack\ncut -2\ndeal with increment 7\ncut 8\ncut -4\ndeal with increment 7\ncut 3\n'
         'deal with increment 9\ndeal with increment 3\ncut -1'.split('\n'), [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]),
])
def test_shuffle(size, instructions, result):
    assert shuffle_deck(list(range(size)), instructions) == result
