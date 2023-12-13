import itertools

def total_paths(image, stretch=2):
    galaxies = [(x, y) for y, row in enumerate(image) for x, c in enumerate(row) if c == '#']
    stretch_y = [y for y, row in enumerate(image) if '#' not in row]
    stretch_x = [x for x in range(len(image[0])) if all(row[x] != '#' for row in image)]

    total = 0
    for g1, g2 in itertools.combinations(galaxies, 2):
        dy = abs(g2[1] - g1[1]) + (stretch - 1) * sum(y in stretch_y for y in range(g2[1], g1[1], 1 if g1[1] > g2[1] else -1))
        dx = abs(g2[0] - g1[0]) + (stretch - 1) * sum(x in stretch_x for x in range(g2[0], g1[0], 1 if g1[0] > g2[0] else -1))
        total += dx + dy
    return total


def parse(data):
    return data.split('\n')


def run(data):
    image = parse(data)
    return total_paths(image), total_paths(image, 1_000_000)

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''

    test_a, _ = run(sample)
    assert test_a == 374

    image = parse(sample)
    assert total_paths(image) == 374
    assert total_paths(image, 10) == 1030
    assert total_paths(image, 100) == 8410

    puz = Puzzle(2023, 11)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
