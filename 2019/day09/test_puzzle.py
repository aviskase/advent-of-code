import pytest

from .puzzle import IntcodeComputer, run_engines, run_engines_with_feedback


@pytest.mark.parametrize('program,result', [
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ([3, 0, 4, 0, 99], [1, 0, 4, 0, 99]),
    ([1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99]),
    ([1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99]),
])
def test_execute_program(program, result):
    computer = IntcodeComputer(program)
    computer.execute(1)
    assert computer.program == result


@pytest.mark.parametrize('program,inputs,output', [
    ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 7, 0),
    ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),
    ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
    ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1),
    ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, 0),
    ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
    ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 7, 0),
    ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),
    ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 9, 0),
    ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1),
    ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, 0),
    ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
    ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 99, 1),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
    ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 99, 1),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4,
      20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 7, 999),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4,
      20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 8, 1000),
    ([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4,
      20, 1105, 1, 46, 104, 999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], 9, 1001),
])
def test_output(program, inputs, output):
    computer = IntcodeComputer(program)
    assert computer.execute(inputs)[0] == output


@pytest.mark.parametrize('code,instruction,modes', [
    (1002, 2, [0, 1, 0]),
    (11001, 1, [0, 1, 1]),
    (3, 3, [0, 0, 0]),
    (99, 99, [0, 0, 0])
])
def test_unpack_codes(code, instruction, modes):
    assert IntcodeComputer.unpack_code(code) == (instruction, modes)


@pytest.mark.parametrize('program,phases,output', [
    ([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], [4, 3, 2, 1, 0], 43210),
    (
    [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0, 1, 2, 3, 4],
    54321),
    ([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31,
      4, 31, 99, 0, 0, 0], [1, 0, 4, 3, 2], 65210),
])
def test_run_engine(program, phases, output):
    assert run_engines(phases, program) == output


@pytest.mark.parametrize('program,phases,output', [
    (
    [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5],
    [9, 8, 7, 6, 5], 139629729),
    (
    [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53,
     54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10],
    [9, 7, 8, 5, 6], 18216)
])
def test_run_engine_with_feedback(program, phases, output):
    assert run_engines_with_feedback(phases, program)[-1] == output


@pytest.mark.parametrize('program,output', [
    ('104,1125899906842624,99', 1125899906842624),
    ('1102,34915192,34915192,7,4,7,99,0', 1219070632396864)
])
def test_big_numbers(program, output):
    computer = IntcodeComputer.from_string(program)
    assert computer.execute()[0] == output


def test_memory():
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    assert IntcodeComputer(program).execute() == program


@pytest.mark.parametrize('program,output', [
    ([109, -1, 4, 1, 99], -1),
    ([109, -1, 104, 1, 99], 1),
    ([109, -1, 204, 1, 99], 109),
    ([109, 1, 9, 2, 204, -6, 99], 204),
    ([109, 1, 109, 9, 204, -6, 99], 204),
    ([109, 1, 209, -1, 204, -106, 99], 204),
    ([109, 1, 3, 3, 204, 2, 99], 678),
    ([109, 1, 203, 2, 204, 2, 99], 678),
])
def test_from_reddit(program, output):
    assert IntcodeComputer(program).execute(678)[0] == output
