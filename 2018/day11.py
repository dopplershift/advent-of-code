import numpy as np


def get_level(x, y, serial):
    rack = x + 10
    return ((rack * y + serial) * rack % 1000) // 100 - 5


def gen_grid(nx, ny, serial):
    x = np.arange(1, nx + 1)
    y = np.arange(1, ny + 1)[:, None]
    return get_level(x, y, serial)


def find_max(grid, size=3):
    max_loc = (0, 0)
    max_sum = -2**32
    for i in range(grid.shape[0] - size + 1):
        for j in range(grid.shape[1] - size + 1):
            total = np.sum(grid[i:i+size, j:j+size])
            if total > max_sum:
                max_sum = total
                max_loc = (j + 1, i + 1)
    return max_loc + (max_sum,)


def find_max_box(grid, cap=30):
    max_loc = (0, 0)
    max_sum = -2**32
    max_size = 0
    for size in range(1, cap):
        *loc, total = find_max(grid, size)
        if total > max_sum:
            max_loc = tuple(loc)
            max_size = size
            max_sum = total
    return max_loc + (max_size,)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert get_level(3, 5, 8) == 4
    assert get_level(122, 79, 57) == -5
    assert get_level(217, 196, 39) == 0
    assert get_level(101, 153, 71) == 4

    assert find_max(gen_grid(300, 300, 18))[:2] == (33, 45)
    assert find_max(gen_grid(300, 300, 42))[:2] == (21, 61)

    assert find_max_box(gen_grid(300, 300, 18)) == (90, 269, 16)

    puz = Puzzle(2018, 11)
    my_id = int(puz.input_data)

    *loc, _ = find_max(gen_grid(300, 300, my_id))
    puz.answer_a = ','.join(str(i) for i in loc)
    print(f'Part 1: {puz.answer_a}')

    ident = find_max_box(gen_grid(300, 300, my_id))
    puz.answer_b = ','.join(str(i) for i in ident)
    print(f'Part 2: {puz.answer_b}')
