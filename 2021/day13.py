from ast import literal_eval
import re

from aoc_tools import ocr

def parse(s):
    dots, folds = s.split('\n\n')
    dots = set(literal_eval(d) for d in dots.split('\n'))
    folds = [re.search(r'[\w\s]+([xy])=(\d+)', line).groups() for line in folds.split('\n')]
    return dots, folds


def do_folds(dots, folds):
    for axis, loc in folds:
        loc = int(loc)
        if axis == 'x':
            dots = {(x if x < loc else 2 * loc - x, y) for x, y in dots}
        else:
            dots = {(x, y if y < loc else 2 * loc - y) for x, y in dots}

    return dots


def display(dots):
    max_x = max(i[0] for i in dots)
    max_y = max(i[-1] for i in dots)

    return '\n'.join(''.join('#' if (x, y) in dots else ' ' for x in range(max_x + 1)) for y in range(max_y + 1))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''

    dots, folds = parse(sample)
    assert len(do_folds(dots, folds[:1])) == 17
    assert len(do_folds(dots, folds)) == 16

    puz = Puzzle(2021, 13)
    dots, folds = parse(puz.input_data)

    puz.answer_a = len(do_folds(dots, folds[:1]))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = ocr(display(do_folds(dots, folds)))
    print(f'Part 2: {puz.answer_b}')
