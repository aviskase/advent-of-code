from .puzzle import execute_program, memory_sum, execute_program2

data = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''.strip().splitlines()


data2 = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''.strip().splitlines()


def test_execute():
    memory = execute_program(data)
    assert set(memory.values()) == {101, 64}
    assert memory_sum(memory) == 165


def test_execute2():
    assert memory_sum(execute_program2(data2)) == 208
