import functools
import string

def anyone(group):
    return functools.reduce(lambda c, n: c | set(n), group.split(), set())


def everyone(group):
    return functools.reduce(lambda c, n: c & set(n), group.split(), set(string.ascii_lowercase))


def count(groups, who):
    return sum(len(who(group)) for group in groups)


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''abc

    a
    b
    c

    ab
    ac

    a
    a
    a
    a

    b'''

    groups = t.split('\n\n')
    assert count(groups, anyone) == 11
    assert count(groups, everyone) == 6

    puz = Puzzle(2020, 6)
    groups = puz.input_data.split('\n\n')

    puz.answer_a = count(groups, anyone)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = count(groups, everyone)
    print(f'Part 2: {puz.answer_b}')
