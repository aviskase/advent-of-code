import math
from itertools import product
from typing import Tuple, Dict, List, NamedTuple

from more_itertools import flatten

RuleRange = NamedTuple('RuleRange', [('start', int), ('end', int)])
TRules = Dict[str, List[RuleRange]]
TTicket = List[int]


def rule_range(r):
    a, b = r.split('-')
    return RuleRange(start=int(a), end=int(b))


def parse(raw_data: str) -> Tuple[TRules, TTicket, List[TTicket]]:
    raw_rules, my_ticket, other_tickets = raw_data.split('\n\n')
    rules = {}
    for r in raw_rules.splitlines():
        name, ranges = r.split(': ')
        rules[name] = [rule_range(r) for r in ranges.split(' or ')]
    my_ticket = [int(i) for i in my_ticket.splitlines()[-1].split(',')]
    other_tickets = [list(int(x) for x in i.split(',')) for i in other_tickets.splitlines()[1:]]
    return rules, my_ticket, other_tickets


def find_errors(rules: TRules, tickets: List[TTicket]) -> List[int]:
    return [
        value
        for value in flatten(tickets)
        if not any(is_valid_to_rule_range(value, r) for r in rules.values())
    ]


def is_valid_to_rule_range(value: int, ranges: List[RuleRange]):
    return any(r.start <= value <= r.end for r in ranges)


def find_fields(rules: TRules, tickets: List[TTicket]) -> List[str]:
    valid_tickets = [t for t in tickets if not find_errors(rules, [t])]
    possible_fields = [set() for _ in rules]
    for field, (i, pos) in product(rules, enumerate(zip(*valid_tickets))):
        if all(is_valid_to_rule_range(p, rules[field]) for p in pos):
            possible_fields[i].add(field)

    fields = ['' for _ in rules]
    while any(len(x) > 0 for x in possible_fields):
        index, unique = next((i, p) for i, p in enumerate(possible_fields) if len(p) == 1)
        fields[index] = next(iter(unique))
        possible_fields = [p.difference(unique) for p in possible_fields]
    return fields


def mul_departure(fields: List[str], ticket: TTicket) -> int:
    return math.prod(ticket[i] for i, f in enumerate(fields) if f.startswith('departure'))


def solver():
    with open('input.txt', 'r') as f:
        raw_data = f.read().strip()
        rules, my_ticket, other_tickets = parse(raw_data)
        print('Part 1:', sum(find_errors(rules, other_tickets)))  # 25916
        print('Part 2:', mul_departure(find_fields(rules, other_tickets), my_ticket))  # 2564529489989


if __name__ == '__main__':
    solver()
