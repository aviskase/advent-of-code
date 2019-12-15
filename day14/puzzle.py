import math


def parse_ingridient(ingridient):
    num, name = ingridient.split(' ')
    return name, int(num)


def parse_line(line):
    inputs, result = line.split(' => ')
    inputs = inputs.split(', ')
    name, output = parse_ingridient(result)
    return name, {
        'output': output,
        'inputs': [parse_ingridient(i) for i in inputs],
        'produced': 0
    }


def parse_data(data):
    formulas = dict()
    for line in data:
        name, value = parse_line(line.strip())
        formulas[name] = value
    formulas['ORE'] = {'produced': 0}
    return formulas


def calculate(element, amount, formulas):
    if element == 'ORE':
        return amount
    done = formulas[element]['produced']
    if done != 0:
        if amount <= done:
            formulas[element]['produced'] -= amount
            return 0
        amount -= done
    formulas[element]['produced'] = 0

    inputs = formulas[element]['inputs']
    output = formulas[element]['output']
    ore = 0
    multiple = 1 if output > amount else math.ceil(amount / output)
    out_amount = multiple * output
    for i in inputs:
        ore += calculate(i[0], i[1] * multiple, formulas)
    if out_amount > amount:
        formulas[element]['produced'] += out_amount - amount
    return ore


def calculate_fuel(formulas):
    return calculate('FUEL', 1, formulas)


def calculate_fuel_by_ore(data, total_ore):
    amount = 1
    step = total_ore - amount
    while True:
        formulas = parse_data(data)
        ore = calculate('FUEL', amount, formulas)
        step = round(step / 2)
        if step < 1:
            break
        if ore > total_ore:
            amount -= step
        else:
            amount += step
    return amount


def solver():
    with open('input.txt', 'r') as f:
        data = f.readlines()
    formulas = parse_data(data)
    print('Part 1:', calculate_fuel(formulas))
    print('Part 2:', calculate_fuel_by_ore(data, 1000000000000))


if __name__ == '__main__':
    solver()
