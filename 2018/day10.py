import numpy as np

from aoc_tools import ocr


def parse(f):
    for line in f:
        _, coords = line[:25].split('=')
        x = int(coords[1:7])
        y = int(coords[8:15])
        _, comps = line[25:].split('=')
        u = int(comps[1:3])
        v = int(comps[4:7])
        yield x, y, u, v


def cost(t):
    return len(set(x + u * t)) + len(set(y + v * t))


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2018, 10)
    vals = np.array(list(parse(puz.input_data.split('\n'))))

    x, y, u, v = vals.T
    min_time = min(range(20000), key=cost)

    final_x = x + u * min_time
    final_y = y + v * min_time

    min_x = final_x.min()
    max_x = final_x.max()
    min_y = final_y.min()
    max_y = final_y.max()

    board = [[' ' for _ in range(min_x, max_x + 1)]
             for _ in range(min_y, max_y + 1)]

    for x,y in zip(final_x, final_y):
        board[y - min_y][x - min_x] = '#'

    puz.answer_a = ocr('\n'.join(''.join(row)for row in board))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = min_time
    print(f'Part 2: {puz.answer_b}')
