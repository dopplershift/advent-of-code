import re

import numpy as np


def solve(s):
    grid = np.zeros((1000, 1000), dtype=np.int8)
    for line in s.split('\n'):
        startx, starty, endx, endy = map(int, re.search(r'(\d+),(\d+) through (\d+),(\d+)', line).groups())
        sector = (slice(starty, endy + 1), slice(startx, endx + 1))
        if line.startswith('turn on'):
            grid[sector] = 1
        elif line.startswith('turn off'):
            grid[sector] = 0
        elif line.startswith('toggle'):
            grid[sector] = 1 - grid[sector]
    return grid


def solve2(s):
    grid = np.zeros((1000, 1000), dtype=np.int8)
    for line in s.split('\n'):
        startx, starty, endx, endy = map(int, re.search(r'(\d+),(\d+) through (\d+),(\d+)', line).groups())
        sector = (slice(starty, endy + 1), slice(startx, endx + 1))
        if line.startswith('turn on'):
            grid[sector] += 1
        elif line.startswith('turn off'):
            grid[sector] = np.clip(grid[sector] - 1, 0, None)
        elif line.startswith('toggle'):
            grid[sector] += 2
    return grid


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2015, 6)

    puz.answer_a = int(solve(puz.input_data).sum())
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = int(solve2(puz.input_data).sum())
    print(f'Part 2: {puz.answer_b}')
