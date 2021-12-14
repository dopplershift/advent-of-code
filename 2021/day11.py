from itertools import count, product


def run(data):
    grid = parse(data)
    part_a = simulate(grid, 100)
    grid = parse(data)
    part_b = find_synchro(grid)
    return part_a, part_b


def parse(s):
    grid = {}
    for r, row in enumerate(s.split('\n')):
        for c, col in enumerate(row):
            grid[c, r] = int(col)
    return grid


def step(grid):
    for k in grid:
        grid[k] += 1

    done = set()
    todo = {k for k in grid if grid[k] > 9}
    count = 0
    while todo:
        x, y = todo.pop()
        done.add((x, y))
        for dx, dy in product((-1, 0, 1), (-1, 0, 1)):
            if dx or dy:
                n = (x + dx, y + dy)
                if n in grid and n not in done:
                    grid[n] += 1
                    if grid[n] > 9:
                        todo.add(n)

    for p in done:
        grid[p] = 0

    return len(done)


def simulate(grid, n):
    return sum(step(grid) for _ in range(n))


def find_synchro(grid):
    for i in count(1):
        if step(grid) == len(grid):
            return i


if __name__ == '__main__':
    from aocd.models import Puzzle

    small = '''11111
19991
19191
19991
11111'''

    assert step(parse(small)) == 9

    sample = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''

    assert simulate(parse(sample), 10) == 204

    test_a, test_b = run(sample)
    assert test_a == 1656
    assert test_b == 195

    puz = Puzzle(2021, 11)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
