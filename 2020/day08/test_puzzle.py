from .puzzle import parse_commands, accumulator_before_loop

data = parse_commands('''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''.strip().splitlines())


def test_accumulator_before_loop():
    assert accumulator_before_loop(data) == 5

