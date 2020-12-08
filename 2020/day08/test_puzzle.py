from .puzzle import parse_commands, execute, repair

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
    assert execute(data) == (5, False)


def test_repair():
    assert repair(data) == 8
