def parse(data):
    return {(r, c): int(v) for r, row in enumerate(data.split('\n')) for c, v in enumerate(row)}


def scan(grid):
    rows = max(k[0] for k in grid) + 1
    cols = max(k[-1] for k in grid) + 1

    seen = set()
    for y in range(rows):
        tallest = -1
        for x in range(cols):
            if grid[y, x] > tallest:
                seen.add((y, x))
                tallest = grid[y, x]

        tallest = -1
        for x in range(cols - 1, -1, -1):
            if grid[y, x] > tallest:
                seen.add((y, x))
                tallest = grid[y, x]

    for x in range(cols):
        tallest = -1
        for y in range(rows):
            if grid[y, x] > tallest:
                seen.add((y, x))
                tallest = grid[y, x]

        tallest = -1
        for y in range(rows - 1, -1, -1):
            if grid[y, x] > tallest:
                seen.add((y, x))
                tallest = grid[y, x]

    return seen


def score(grid):
    rows = max(k[0] for k in grid) + 1
    cols = max(k[-1] for k in grid) + 1

    scores = {}
    for (cy, cx), tree in grid.items():
        l = 0
        for x in range(cx - 1, -1, -1):
            l += 1
            if grid[cy, x] >= tree:
                break
        r = 0
        for x in range(cx + 1, cols, 1):
            r += 1
            if grid[cy, x] >= tree:
                break
        d = 0
        for y in range(cy - 1, -1, -1):
            d += 1
            if grid[y, cx] >= tree:
                break
        u = 0
        for y in range(cy + 1, rows, 1):
            u += 1
            if grid[y, cx] >= tree:
                break
        scores[cy, cx] = l * r * u *d
    return scores


def run(data):
    trees = parse(data)
    return len(scan(trees)), max(score(trees).values())


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
