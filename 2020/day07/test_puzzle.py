import pytest

from .puzzle import can_contain, map_rules, num_of_bags_inside

data = map_rules('''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''.strip().splitlines())

second_data = map_rules('''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
'''.strip().splitlines())


def test_can_contain():
    assert can_contain(data, 'shiny gold') == {'bright white', 'muted yellow', 'dark orange', 'light red'}


@pytest.mark.parametrize('d, expected', [(data, 32), (second_data, 126)])
def test_num_of_bags_inside(d, expected):
    assert num_of_bags_inside(d, 'shiny gold') == expected
