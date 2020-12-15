from .puzzle import execute_program, memory_sum

data = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''.strip().splitlines()


def test_execute():
    memory = execute_program(data)
    assert set(memory.values()) == {101, 64}
    assert memory_sum(memory) == 165
