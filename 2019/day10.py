from functools import lru_cache

import numpy as np

from aoc_tools import gcd


def read_asteroids(lines):
    return [(col, row)
            for row, line in enumerate(lines)
            for col, c in enumerate(line.strip())
            if c == '#']


def get_direction(x, y):
    div = gcd(abs(x), abs(y))
    return x // div, y // div


def count_options(loc, asteroids):
    return len({get_direction(a[0] - loc[0], a[1] - loc[1]) for a in asteroids if a != loc})


def find_max_options(asteroids):
    return max((count_options(location, asteroids), location) for location in asteroids)


def order_by_angles(asteroids, loc):
    orig_pts = np.array(asteroids).T
    pts = np.array([[1], [-1]]) * (orig_pts - np.array(loc)[:, None])
    dist = np.abs(pts).sum(axis=0)
    sorter = np.argsort(dist, kind='stable')

    orig_pts = orig_pts[np.array([[0], [1]]), sorter]
    pts = pts[np.array([[0], [1]]), sorter]

    angles = np.pi / 2 - np.arctan2(pts[1], pts[0])
    angles[angles < 0] += 2 * np.pi

    sorter = np.argsort(angles, kind='stable')
    angles = angles[sorter]
    orig_pts = orig_pts[np.array([[0], [1]]), sorter]
    pts = pts[np.array([[0], [1]]), sorter]

    prev = -999
    num = 0
    for i, a in enumerate(angles):
        if np.fabs(a - prev) < 1e-4:
            num += 1
            angles[i] += num * (2 * np.pi)
        else:
            num = 0
            prev = a

    sorter = np.argsort(angles, kind='stable')
    angles = angles[sorter]
    return orig_pts[np.array([[0], [1]]), sorter]


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = read_asteroids('.#..#\n.....\n#####\n....#\n...##'.split('\n'))
    assert [count_options(p, t) for p in t] == [7, 7, 6, 7, 7, 7, 5, 7, 8, 7]
    assert find_max_options(t) == (8, (3, 4))

    f = '''......#.#.
    #..#.#....
    ..#######.
    .#.#.###..
    .#..#.....
    ..#....#.#
    #..#....#.
    .##.#..###
    ##...#..#.
    .#....####'''.split('\n')
    t = read_asteroids(f)
    assert find_max_options(t) == (33, (5, 8))

    f = '''#.#...#.#.
    .###....#.
    .#....#...
    ##.#.#.#.#
    ....#.#.#.
    .##..###.#
    ..#...##..
    ..##....##
    ......#...
    .####.###.'''.split('\n')
    t = read_asteroids(f)
    assert find_max_options(t) == (35, (1, 2))

    f = '''.#..#..###
    ####.###.#
    ....###.#.
    ..###.##.#
    ##.##.#.#.
    ....###..#
    ..#.#..#.#
    #..#.#.###
    .##...##.#
    .....#.#..'''.split('\n')
    t = read_asteroids(f)
    assert find_max_options(t) == (41, (6, 3))

    f = '''.#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##'''.split('\n')
    t = read_asteroids(f)
    assert find_max_options(t) == (210, (11, 13))

    # Test for part 2
    f = '''.#..##.###...#######
    ##.############..##.
    .#.######.########.#
    .###.#######.####.#.
    #####.##.#.##.###.##
    ..#####..#.#########
    ####################
    #.####....###.#.#.##
    ##.#################
    #####.##.###..####..
    ..######..##.#######
    ####.##.####...##..#
    .#####..#.######.###
    ##...#.##########...
    #.##########.#######
    .####.#.###.###.#.##
    ....##.##.###..#####
    .#.#.###########.###
    #.#.#.#####.####.###
    ###.##.####.##.#..##'''.split('\n')
    t = read_asteroids(f)
    assert tuple(order_by_angles(t, (11, 13))[:, 199]) == (8, 2)

    puz = Puzzle(2019, 10)
    a = read_asteroids(puz.input_data.split('\n'))
    best, loc = find_max_options(a)

    puz.answer_a = best
    print(f'Part 1: {puz.answer_a}')

    # 199 -> 200th asteroid
    pt = order_by_angles(a, loc)[:, 199]
    puz.answer_b = int(100 * pt[0] + pt[1])
    print(f'Part 2: {puz.answer_b}')
