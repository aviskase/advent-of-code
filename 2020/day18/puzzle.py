from collections import deque


ORDERS_1 = {
    '(': 1,
    '+': 2,
    '*': 2,
}

ORDERS_2 = {
    '(': 1,
    '+': 3,
    '*': 2,
}


def convert_to_postfix(expr, orders):
    expr_clean = expr.replace('(', ' ( ').replace(')', ' ) ').replace('  ', ' ').strip()
    operators = deque()
    postfix_expr = []
    for token in expr_clean.split(' '):
        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators[-1] != '(':
                postfix_expr.append(operators.pop())
            operators.pop()
        elif token in orders:
            while operators and orders[operators[-1]] >= orders[token]:
                postfix_expr.append(operators.pop())
            operators.append(token)
        else:
            postfix_expr.append(int(token))
    while operators:
        postfix_expr.append(operators.pop())
    return postfix_expr


def calculate(expr: str, orders=None) -> int:
    if orders is None:
        orders = ORDERS_1
    postfix_expr = convert_to_postfix(expr, orders)
    stack = deque()
    for token in postfix_expr:
        if token == '+':
            stack.append(stack.pop() + stack.pop())
        elif token == '*':
            stack.append(stack.pop() * stack.pop())
        else:
            stack.append(token)
    return stack.pop()


def solver():
    with open('input.txt', 'r') as f:
        data = f.read().strip().splitlines()
        print('Part 1:', sum(calculate(expr) for expr in data))  # 98621258158412
        print('Part 2:', sum(calculate(expr, ORDERS_2) for expr in data))  # 241216538527890


if __name__ == '__main__':
    solver()
