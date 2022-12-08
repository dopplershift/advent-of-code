def parse(data):
    return [list(map(int, row)) for row in data.split('\n')]


def visible(check_x, check_y, grid):
    height = grid[check_y][check_x]
    return (all(grid[check_y][x] < height for x in range(check_x)) or
            all(grid[check_y][x] < height for x in range(check_x + 1, len(grid[0]))) or
            all(grid[y][check_x] < height for y in range(check_y)) or
            all(grid[y][check_x] < height for y in range(check_y + 1, len(grid))))


def scan(grid):
    return sum(visible(x, y, grid) for y in range(len(grid)) for x in range(len(grid[y])))


def score(check_x, check_y, grid):
    height = grid[check_y][check_x]
    left = dist(lambda x: grid[check_y][x] < height, reversed(range(check_x)))
    right = dist(lambda x: grid[check_y][x] < height, range(check_x + 1, len(grid[0])))
    up = dist(lambda y: grid[y][check_x] < height, reversed(range(check_y)))
    down = dist(lambda y: grid[y][check_x] < height, range(check_y + 1, len(grid)))

    return up * down * left * right


def dist(check, seq):
    d = 0
    for item in seq:
        d += 1
        if not check(item):
            break
    return d


def scenic(grid):
    return max(score(x, y, grid) for y in range(len(grid)) for x in range(len(grid[y])))


def run(data):
    trees = parse(data)
    return scan(trees), scenic(trees)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''30373
25512
65332
33549
35390'''

    test_a, test_b = run(sample)
    assert test_a == 21
    assert test_b == 8

    puz = Puzzle(2022, 8)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
