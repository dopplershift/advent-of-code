import operator


def parse(s):
    return list(reversed(s))


def evaluate(chars):
    val_stack = []
    oper = None
    while True:
        if len(val_stack) == 2 and oper:
            val_stack.append(oper(val_stack.pop(), val_stack.pop()))
            oper = None
        elif chars:
            char = chars.pop()
            if char.isdigit():
                val_stack.append(int(char))
            elif char == '*':
                oper = operator.mul
            elif char == '+':
                oper = operator.add
            elif char == '(':
                val_stack.append(evaluate(chars))
            elif char == ')':
                break
        else:
            break
    return val_stack[-1]


def evaluate2(chars):
    stack = []
    while chars:
        char = chars.pop()
        if char.isdigit():
            stack.append(int(char))
        elif char == '*':
            stack.append(operator.mul)
        elif char == '+':
            stack.append(operator.add)
        elif char == '(':
            stack.append(evaluate2(chars))
        elif char == ')':
            break

    for op in (operator.add, operator.mul):
        while stack.count(op):
            op_loc = stack.index(op)
            stack[op_loc] = op(stack[op_loc - 1], stack[op_loc + 1])
            del stack[op_loc + 1]
            del stack[op_loc - 1]

    return stack[-1]


# Shunting-yard algorithm: https://en.wikipedia.org/wiki/Shunting-yard_algorithm
# Much happier with this one since it's easy to adjust behavior
def shuntyard(chars, add_prec=1):
    ops = {'*': operator.mul, '+': operator.add}
    prec = {operator.mul: 1, operator.add: add_prec}
    val_stack = []
    op_stack = []
    tokens = iter(chars)
    for char in tokens:
        if char.isdigit():
            val_stack.append(int(char))
        elif char in ops:
            op = ops[char]
            while op_stack and prec[op_stack[-1]] >= prec[op]:
                val_stack.append(op_stack.pop()(val_stack.pop(), val_stack.pop()))
            op_stack.append(op)
        elif char == '(':
            val_stack.append(shuntyard(tokens, add_prec))
        elif char == ')':
            break
    while op_stack:
        val_stack.append(op_stack.pop()(val_stack.pop(), val_stack.pop()))
    return val_stack[-1]

if __name__ == '__main__':
    from aocd.models import Puzzle

    assert evaluate(parse('1 + 2 * 3 + 4 * 5 + 6')) == 71
    assert evaluate(parse('2 * 3 + (4 * 5)')) == 26
    assert evaluate(parse('5 + (8 * 3 + 9 + 3 * 4 * 3)')) == 437
    assert evaluate(parse('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')) == 12240
    assert evaluate(parse('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) == 13632

    assert evaluate2(parse('1 + 2 * 3 + 4 * 5 + 6')) == 231
    assert evaluate2(parse('1 + (2 * 3) + (4 * (5 + 6))')) == 51
    assert evaluate2(parse('2 * 3 + (4 * 5)')) == 46
    assert evaluate2(parse('5 + (8 * 3 + 9 + 3 * 4 * 3)')) == 1445
    assert evaluate2(parse('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')) == 669060
    assert evaluate2(parse('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')) == 23340

    assert shuntyard('1 + 2 * 3 + 4 * 5 + 6') == 71
    assert shuntyard('2 * 3 + (4 * 5)') == 26
    assert shuntyard('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
    assert shuntyard('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
    assert shuntyard('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

    assert shuntyard('1 + 2 * 3 + 4 * 5 + 6', 2) == 231
    assert shuntyard('1 + (2 * 3) + (4 * (5 + 6))', 2) == 51
    assert shuntyard('2 * 3 + (4 * 5)', 2) == 46
    assert shuntyard('5 + (8 * 3 + 9 + 3 * 4 * 3)', 2) == 1445
    assert shuntyard('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 2) == 669060
    assert shuntyard('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 2) == 23340

    puz = Puzzle(2020, 18)

    puz.answer_a = sum(evaluate(parse(line)) for line in puz.input_data.split('\n'))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = sum(evaluate2(parse(line)) for line in puz.input_data.split('\n'))
    print(f'Part 2: {puz.answer_b}')
