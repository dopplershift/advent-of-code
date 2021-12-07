# TODO: Time's not great here
import numpy as np


def parse(f):
    val_map = {'.': 0, '|': 1, '#': 2}
    rows = []
    for line in f:
        rows.append([])
        for c in line.rstrip():
            rows[-1].append(val_map[c])
    return np.array(rows)


def iterate(grid, iters=10):
    for _ in range(iters):
        next_grid = np.zeros_like(grid)
        for (y, x), val in np.ndenumerate(grid):
            domain = grid[max(y - 1, 0) : y + 2, max(x - 1, 0) : x + 2]
            if val == 0 and np.sum(domain == 1) >= 3:
                next_grid[y, x] = 1
            elif val == 1 and np.sum(domain == 2) >= 3:
                next_grid[y, x] = 2
            elif val == 2 and not (np.sum(domain == 2) >= 2 and np.sum(domain == 1) >= 1):
                next_grid[y, x] = 0
            else:
                next_grid[y, x] = val
        grid = next_grid
    return grid


def score(grid):
    return np.sum(grid == 1) * np.sum(grid == 2)


if __name__ == '__main__':
    from aocd.models import Puzzle

    f = '''.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.'''
    grid = parse(f.split('\n'))

    new_grid = iterate(grid)
    assert score(new_grid) == 1147

    puz = Puzzle(2018, 18)
    grid = parse(puz.input_data.split('\n'))
    new_grid = iterate(grid)
    puz.answer_a = int(score(new_grid))
    print(f'Part 1: {puz.answer_a}')

    minutes = 500
    new_grid = iterate(grid, minutes)
    options = []
    for i in range(28):
        new_grid = iterate(new_grid, 1)
        options.append(score(new_grid))

    puz.answer_b = int(options[(1000000000 - minutes - 1) % len(options)])
    print(f'Part 2: {puz.answer_b}')
