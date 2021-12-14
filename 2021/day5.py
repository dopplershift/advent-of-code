from ast import literal_eval
from collections import defaultdict


def run(data):
    segs = parse(data)
    return count(make_grid(segs)), count(make_grid(segs, diag=True))


def parse(s):
    return [tuple(map(literal_eval, line.split(' -> ')))
            for line in s.split('\n')]


def make_grid(segs, diag=False):
    grid = defaultdict(lambda: 0)

    for (start_x, start_y), (end_x, end_y) in segs:
        xinc = 1 if start_x < end_x else -1
        yinc = 1 if start_y < end_y else -1
        if start_y == end_y:
            for i in range(start_x, end_x + xinc, xinc):
                grid[i, start_y] += 1
        elif start_x == end_x:
            for i in range(start_y, end_y + yinc, yinc):
                grid[start_x, i] += 1
        elif diag:
            for x, y in zip(range(start_x, end_x + xinc, xinc),
                            range(start_y, end_y + yinc, yinc)):
                grid[x, y] += 1
    return grid


def count(grid):
    return sum(v > 1 for v in grid.values())


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''

    test_a, test_b = run(sample)
    assert test_a == 5
    assert test_b == 12

    puz = Puzzle(2021, 5)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
