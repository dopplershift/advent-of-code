import re
import string

number = re.compile(r'\d+')
nonsymbol = set(string.digits + '.')


def part_nos(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c not in nonsymbol:
                yield from adjacent_digits(grid, y, x)


def adjacent_digits(grid, y, x):
    for match in number.finditer(grid[y]):
        if match.start(0) == x + 1 or match.end(0) == x:
            yield int(match.group(0))
    if y > 0:
        for match in number.finditer(grid[y - 1]):
            if match.start(0) <= x + 1 and match.end(0) >= x:
                yield int(match.group(0))
    if y < len(grid) - 1:
        for match in number.finditer(grid[y + 1]):
            if match.start(0) <= x + 1 and match.end(0) >= x:
                yield int(match.group(0))


def gear_ratios(grid):
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '*':
                gears = list(adjacent_digits(grid, y, x))
                if len(gears) == 2:
                    yield gears[0] * gears[1]


def parse(data):
    return data.split('\n')


def run(data):
    grid = parse(data)
    return sum(part_nos(grid)), sum(gear_ratios(grid))

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
755....55.
...*.$....
.664.598..'''

    test_a, test_b = run(sample)
    assert test_a == 4361
    assert test_b == (664 * 755) + (467 * 35)

    puz = Puzzle(2023, 3)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
