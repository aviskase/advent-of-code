from .puzzle import parse, RuleRange, find_errors, find_fields


data = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''.strip()

parsed_rules = {
    'class': [RuleRange(1, 3), RuleRange(5, 7)],
    'row': [RuleRange(6, 11), RuleRange(33, 44)],
    'seat': [RuleRange(13, 40), RuleRange(45, 50)],
}

parsed_my_ticket = [7, 1, 14]

parsed_other_tickets = [
    [7, 3, 47],
    [40, 4, 50],
    [55, 2, 20],
    [38, 6, 12],
]


def test_parse():
    rules, my_ticket, other_tickets = parse(data)
    assert rules == parsed_rules
    assert my_ticket == parsed_my_ticket
    assert other_tickets == parsed_other_tickets


def test_find_errors():
    assert find_errors(parsed_rules, parsed_other_tickets) == [4, 55, 12]


data2 = '''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9'''.strip()


def test_find_fields():
    rules, my_ticket, other_tickets = parse(data2)
    assert find_fields(rules, other_tickets) == ['row', 'class', 'seat']
