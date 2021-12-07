from ast import literal_eval


def parse(s):
    return [tuple(map(literal_eval, line.split(' -> ')))
            for line in s.split('\n')]


def make_grid(segs, diag=False):
    grid = dict()

    for start, end in segs:
        if start[-1] == end[-1]:
            left = min(start[0], end[0])
            right = max(start[0], end[0])
            for i in range(left, right + 1):
                pt = (i, start[-1])
                grid[pt] = grid.get(pt, 0) + 1
        elif start[0] == end[0]:
            top = min(start[-1], end[-1])
            bottom = max(start[-1], end[-1])
            for i in range(top, bottom + 1):
                pt = (start[0], i)
                grid[pt] = grid.get(pt, 0) + 1
        elif diag:
            left = min(start, end)
            right = max(start, end)
            yinc = 1 if left[-1] < right[-1] else -1
            for x, y in zip(range(left[0], right[0] + 1),
                            range(left[-1], right[-1] + yinc, yinc)):
                pt = (x, y)
                grid[pt] = grid.get(pt, 0) + 1
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

    segs = parse(sample)
    assert count(make_grid(segs)) == 5
    assert count(make_grid(segs, diag=True)) == 12

    puz = Puzzle(2021, 5)
    segs = parse(puz.input_data)

    puz.answer_a = sum(v > 1 for v in make_grid(segs).values())
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = sum(v > 1 for v in make_grid(segs, diag=True).values())
    print(f'Part 2: {puz.answer_b}')