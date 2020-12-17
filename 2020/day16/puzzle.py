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
    other_tickets = [list(map(lambda x: int(x), i.split(','))) for i in other_tickets.splitlines()[1:]]
    return rules, my_ticket, other_tickets


def find_errors(rules: TRules, tickets: List[TTicket]) -> List[int]:
    return [
        value
        for value in flatten(tickets)
        if not any(r.start <= value <= r.end for r in flatten(rules.values()))
    ]


def solver():
    with open('input.txt', 'r') as f:
        raw_data = f.read().strip()
        rules, my_ticket, other_tickets = parse(raw_data)
        print('Part 1:', sum(find_errors(rules, other_tickets)))  # 25916
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
