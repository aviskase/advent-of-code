import re


def parse(raw_data: str):
    raw_rules, raw_messages = raw_data.split('\n\n', 2)
    rules = {}
    for r in raw_rules.strip().splitlines():
        code, info = r.split(': ')
        rules[code] = [i.strip().split(' ') for i in info.replace('"', '').split('|')]
    master_rule = re.compile(f'^{build_regex(rules)}$')
    messages = raw_messages.strip().splitlines()
    return master_rule, messages


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


def solver():
    with open('input.txt', 'r') as f:
        master_rule, messages = parse(f.read().strip())
        print('Part 1:', len(find_valid(master_rule, messages)))  # 149
        print('Part 2:', )  #


if __name__ == '__main__':
    solver()
