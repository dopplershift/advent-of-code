from collections import deque
import functools
import operator


def run(data):
    grid = parse(data)
    return total_risk(grid), basins(grid)


def parse(s):
    return [list(map(int, line)) for line in s.split('\n')]


def neighbors(x, y, grid):
    if x > 0:
        yield x - 1, y
    if x < len(grid[0]) - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < len(grid) - 1:
        yield x, y + 1


def low_points(height_map):
    for y, row in enumerate(height_map):
        for x, col in enumerate(row):
            if all(col < height_map[oy][ox] for ox, oy in neighbors(x, y, height_map)):
                yield x, y


def fill_size(startx, starty, grid):
    done = set()
    count = 0
    todo = deque([(startx, starty)])
    while todo:
        pt = todo.pop()
        if pt not in done:
            count += 1
            done.add(pt)
            for x, y in neighbors(*pt, grid):
                if grid[y][x] != 9:
                    todo.appendleft((x, y))
    return count


def basins(height_map):
    basins = [fill_size(x, y, height_map) for x, y in low_points(height_map)]
    return functools.reduce(operator.mul, sorted(basins)[-3:], 1)


def total_risk(height_map):
    return sum(height_map[y][x] + 1 for x, y in low_points(height_map))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''2199943210
3987894921
9856789892
8767896789
9899965678'''

    test_a, test_b = run(sample)
    assert test_a == 15
    assert test_b == 1134

    puz = Puzzle(2021, 9)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
