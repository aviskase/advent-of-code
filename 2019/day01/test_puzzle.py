import pytest

from .puzzle import calculate_fuel, total_fuel, calculate_fuel_recursively


@pytest.mark.parametrize('mass,fuel', [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583)
])
def test_calculate_fuel(mass, fuel):
    assert calculate_fuel(mass) == fuel


@pytest.mark.parametrize('mass,fuel', [
    (14, 2),
    (1969, 966),
    (100756, 50346)
])
def test_calculate_fuel_recursively(mass, fuel):
    assert calculate_fuel_recursively(mass) == fuel


@pytest.mark.parametrize('masses,calculator,fuel', [
    ([12, 14, 1969, 100756], calculate_fuel, 658 + 33583),
    ([14, 1969, 100756], calculate_fuel_recursively, 968 + 50346),
])
def test_total_fuel(masses, calculator, fuel):
    assert total_fuel(masses, calculator) == fuel
