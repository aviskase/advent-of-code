import re


def parse(raw_data: str):
    raw_rules, raw_messages = raw_data.split('\n\n', 2)
    rules = {}
    for r in raw_rules.strip().splitlines():
        code, info = r.split(': ')
        rules[code] = [i.strip().split(' ') for i in info.replace('"', '').split('|')]
    messages = raw_messages.strip().splitlines()
    return rules, messages


def find_valid(master_rule, messages):
    return [msg for msg in messages if master_rule.match(msg)]


def build_regex(rules, start_rule='0'):
    or_rules = []
    for or_rule in rules[start_rule]:
        sub = ['(']
        for sub_rule in or_rule:
            if sub_rule not in rules:
                sub.append(sub_rule)
            else:
                sub.append(build_regex(rules, sub_rule))
        sub.append(')')
        or_rules.append(''.join(sub))
    return f"({'|'.join(or_rules)})"


def part_1_regex(rules):
    return re.compile(f'^{build_regex(rules)}$')


def part_2_regex(rules):
    # 0: 8 11
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    rule_42 = build_regex(rules, '42')
    rule_31 = build_regex(rules, '31')
    rule_8 = f'({rule_42})+'
    # fake it with up to 5 nested rules
    rule_11 = '|'.join(['(' + f'({rule_42})' * i + f'({rule_31})' * i + ')' for i in range(1, 5)])
    return re.compile(f'^({rule_8})({rule_11})$')


def solver():
    with open('input.txt', 'r') as f:
        rules, messages = parse(f.read().strip())
        master_rule = part_1_regex(rules)
        print('Part 1:', len(find_valid(master_rule, messages)))  # 149
        master_rule = part_2_regex(rules)
        print('Part 2:', len(find_valid(master_rule, messages)))  # 332


if __name__ == '__main__':
    solver()
