from collections import deque


def convert_to_postfix(expr):
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
        elif token in ['*', '+']:
            while operators and operators[-1] != '(':
                postfix_expr.append(operators.pop())
            operators.append(token)
        else:
            postfix_expr.append(int(token))
    while operators:
        postfix_expr.append(operators.pop())
    return postfix_expr


def calculate(expr: str) -> int:
    postfix_expr = convert_to_postfix(expr)
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
        # print('Part 2:', )  # 1816


if __name__ == '__main__':
    solver()
