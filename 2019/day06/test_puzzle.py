import pytest

from .puzzle import get_indirects, find_orbits, find_common_node, total_nodes, total_transfers_to_node

orbits_map = {
    'B': 'COM',
    'C': 'B',
    'D': 'C',
    'E': 'D',
    'F': 'E',
    'G': 'B',
    'H': 'G',
    'I': 'D',
    'J': 'E',
    'K': 'J',
    'L': 'K',
}

full_orbits_map = dict(orbits_map)
full_orbits_map.update({'YOU': 'K', 'SAN': 'I'})


@pytest.mark.parametrize('node,orbits', [
    ('B', []),
    ('C', [['B', 'COM']]),
    ('D', [['C', 'B'], ['B', 'COM']]),
])
def test_get_indirects(node, orbits):
    assert get_indirects(node, orbits_map) == orbits


def test_find_orbits():
    assert len(find_orbits(orbits_map)) == 42


def test_common_node():
    my_orbits = total_nodes(get_indirects('YOU', full_orbits_map))
    santa_orbits = total_nodes(get_indirects('SAN', full_orbits_map))
    assert find_common_node(my_orbits, santa_orbits) == 'D'


def test_num_of_transfers():
    my_orbits = total_nodes(get_indirects('YOU', full_orbits_map))
    santa_orbits = total_nodes(get_indirects('SAN', full_orbits_map))
    assert total_transfers_to_node(my_orbits, 'D') == 3
    assert total_transfers_to_node(santa_orbits, 'D') == 1
