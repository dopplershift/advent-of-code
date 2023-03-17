def parse(s):
    return {(c, r): 1 if v == '#' else 0
            for r, line in enumerate(s.splitlines())
            for c, v in enumerate(line)}


def neighbors(grid, c, r):
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if x or y:
                yield grid.get((c + x, r + y), 0)


def iterate(grid, n, part2=False):
    nrows = max(k[1] for k in grid)
    ncols = max(k[0] for k in grid)
    if part2:
        grid[0, 0] = 1
        grid[0, nrows] = 1
        grid[ncols, 0] = 1
        grid[ncols, nrows] = 1
    for _ in range(n):
        grid = {loc: 1 if (sum(neighbors(grid, *loc)) == 3 or (sum(neighbors(grid, *loc)) == 2 and val)
                           or (part2 and loc[0] in {0, ncols} and loc[1] in {0, nrows})) else 0
                 for loc, val in grid.items()}
    return grid


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''.#.#.#
...##.
#....#
..#...
#.#..#
####..'''

    assert sum(iterate(parse(t), 4).values()) == 4
    assert sum(iterate(parse(t), 5, part2=True).values()) == 17

    puz = Puzzle(2015, 18)
    light_grid = parse(puz.input_data)

    puz.answer_a = sum(iterate(light_grid, 100).values())
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = sum(iterate(light_grid, 100, part2=True).values())
    print(f'Part 2: {puz.answer_b}')
