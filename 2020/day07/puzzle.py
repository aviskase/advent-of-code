import re


def map_rules(rules):
    rule_map = {}
    for rule in rules:
        bag_name, inner_bags = rule.strip('.').split(' bags contain ')
        rule_map[bag_name] = {}
        if inner_bags != 'no other bags':
            inner_bags = map(lambda x: x.split(' ', 1), re.sub(r' bags?', '', inner_bags).split(', '))
            rule_map[bag_name] = {b[1]: int(b[0]) for b in inner_bags}
    return rule_map


def can_contain(rules, main_bag):
    bags = set()
    for bag, inner_bags in rules.items():
        if main_bag in inner_bags.keys():
            bags.update({bag, *can_contain(rules, bag)})
    return bags


def solver():
    with open('input.txt', 'r') as f:
        rules = f.read().strip().splitlines()
        rule_map = map_rules(rules)
        print('Part 1:', len(can_contain(rule_map, 'shiny gold')))  # 248
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
