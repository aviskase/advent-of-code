from typing import List, Callable


def calculate_fuel(mass: int) -> int:
    fuel = mass // 3 - 2
    return fuel if fuel >= 0 else 0


def calculate_fuel_recursively(mass: int) -> int:
    fuel = calculate_fuel(mass)
    return fuel if fuel <= 0 else fuel + calculate_fuel_recursively(fuel)


def total_fuel(masses: List[int], calculator: Callable[[int], int]) -> int:
    return sum(calculator(m) for m in masses)


def solver():
    with open('input.txt', 'r') as f:
        masses = [int(module_mass) for module_mass in f.readlines()]
        print('Part 1:', total_fuel(masses, calculate_fuel))
        print('Part 2:', total_fuel(masses, calculate_fuel_recursively))


if __name__ == '__main__':
    solver()
