import functools
from itertools import product

def parse(s):
    alg, img = s.split('\n\n')
    alg = [1 if c == '#' else 0 for c in alg if c in '.#']
    img = {(x, y): 1
           for y, row in enumerate(img.split('\n'))
           for x, c in enumerate(row) if c == '#'}
    return alg, img


def enhance(img, alg, default=0):
    min_x = min(pixel[0] for pixel in img)
    max_x = max(pixel[0] for pixel in img)
    min_y = min(pixel[1] for pixel in img)
    max_y = max(pixel[1] for pixel in img)
    enhanced = {}
    for x, y in product(range(min_x - 2, max_x + 3), range(min_y - 2, max_y + 3)):
        val = 0
        for ny, nx in product((y - 1, y, y + 1), (x - 1, x, x + 1)):
            val = (val<<1) | img.get((nx, ny), default)
        enhanced[x, y] = alg[val]
    return enhanced


def run(data):
    alg, img = parse(data)

    default = 0
    for i in range(50):
        img = enhance(img, alg, default)
        default = alg[default * 511]
        if i == 1:
            part_a = sum(img.values())

    return part_a, sum(img.values())


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

    test_a, test_b = run(sample)
    assert test_a == 35
    assert test_b == 3351

    puz = Puzzle(2021, 20)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
