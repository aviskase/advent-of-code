from copy import deepcopy
from dataclasses import dataclass
from typing import Set, List


@dataclass
class Food:
    ingredients: Set[str]
    allergens: Set[str]


def parse(raw_data: str) -> List[Food]:
    foods = []
    for line in raw_data.splitlines():
        ing, allergens = line.replace(')', '').split(' (contains ', 2)
        foods.append(Food(set(ing.strip().split(' ')), set(allergens.strip().split(', '))))
    return foods


def find_potentially_safe(input_foods: List[Food]) -> Set[str]:
    foods = deepcopy(input_foods)
    all_allergens = {i for food in foods for i in food.allergens}
    while all_allergens:
        for allergen in all_allergens:
            relevant_foods = (f for f in foods if allergen in f.allergens)
            common_ingredients = set.intersection(*list(f.ingredients for f in relevant_foods))
            if len(common_ingredients) == 1:
                for f in foods:
                    f.ingredients.difference_update(common_ingredients)
                    f.allergens.difference_update({allergen})
        all_allergens = {i for food in foods for i in food.allergens}
    return {i for food in foods for i in food.ingredients}


def count_potentially_safe(foods: List[Food], safe: Set[str]) -> int:
    return sum(len(food.ingredients.intersection(safe)) for food in foods)


def solver():
    with open('input.txt', 'r') as f:
        foods = parse(f.read().strip())
        safe = find_potentially_safe(foods)
        print('Part 1:', count_potentially_safe(foods, safe))  # 2542
        # print('Part 2:', )  #


if __name__ == '__main__':
    solver()
