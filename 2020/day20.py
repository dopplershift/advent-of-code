from collections import deque
import math

import numpy as np
import scipy.ndimage


def parse(s):
    tiles = {}
    lookup = {'.': 0, '#': 1}
    for tile in s.split('\n\n'):
        tile_id, data = tile.split(':\n')
        tile_id = int(tile_id.split()[-1])
        arr = np.array([[lookup[c] for c in row.lstrip()] for row in data.split('\n')])
        arr.flags.writeable = False
        tiles[tile_id] = arr[::-1, :]
    return tiles


def edges(tile, flips=False):
    for s in [(slice(None), 0), (slice(None), -1), (0, slice(None)), (-1, slice(None))]:
        edge = tile[s]
        yield tuple(edge)
        if flips:
            yield tuple(edge)[::-1]


def fit_corner(tile, other_edges):
    # Make sure we put the edges in the right spot
    # If top edge is a match in any form, flip vertically
    if tuple(tile[0, :]) in other_edges or tuple(tile[0, ::-1]) in other_edges:
        tile = tile[::-1]
    # If left edge is a match in any form, flip horizontally
    if tuple(tile[:, 0]) in other_edges or tuple(tile[::-1, 0]) in other_edges:
        tile = tile[:, ::-1]
    return tile


def fit_above(tile, edge):
    # Make sure we put the matching edge at the top
    # If any version of left or right matches, rotate
    if edge in (tuple(tile[:, 0]), tuple(tile[::-1, 0]), tuple(tile[:, -1]), tuple(tile[::-1, -1])):
        tile = tile.T
    # If either top or bottom edge reversed is a match, flip horizontally
    if tuple(tile[0, ::-1]) == edge or tuple(tile[-1, ::-1]) == edge:
        tile = tile[:, ::-1]
    # If bottom edge is a match, flip vertically
    if tuple(tile[-1, :]) == edge:
        tile = tile[::-1]
    return tile


def fit_left(tile, edge):
    return fit_above(tile.T, edge).T


def find_match(pool, tiles, edge):
    while pool:
        choice = pool.pop()
        tile = tiles[choice]
        if edge in set(edges(tile, flips=True)):
            return choice
        pool.appendleft(choice)


def assemble(tiles):
    queue = deque(tiles)
    n = int(math.sqrt(len(tiles)))
    layout = [[None] * n for _ in range(n)]

    # Loop until we find the first corner
    while queue:
        tile_id = queue.pop()
        tile = tiles[tile_id]
        other_edges = {edge for other in tiles.values() for edge in edges(other) if other is not tile}
        count = sum(edge in other_edges for edge in edges(tile, flips=True))
        if count != 2:
            queue.appendleft(tile_id)
            continue

        tiles[tile_id] = fit_corner(tile, other_edges)
        layout[0][0] = tile_id
        break

    for row in range(n):
        if row > 0:
            match = tuple(tiles[layout[row - 1][0]][-1, :])
            choice = find_match(queue, tiles, match)
            fit = fit_above(tiles[choice], match)
            tiles[choice] = fit
            layout[row][0] = choice
        for col in range(1, n):
            match = tuple(tiles[layout[row][col-1]][:, -1])
            choice = find_match(queue, tiles, match)
            fit = fit_left(tiles[choice], match)
            tiles[choice] = fit
            layout[row][col] = choice

    return layout


def stitch(layout, tiles):
    return np.concatenate(
        tuple(np.concatenate(tuple(tiles[tile_id][1:-1, 1:-1] for tile_id in row), axis=1)
              for row in layout), axis=0)


def roughness(img):
    m = '''                  #.
#    ##    ##    ###
 #  #  #  #  #  #   '''
    monster = np.array([[1 if c == '#' else 0 for c in row] for row in m.split('\n')])
    locs = 0
    for i in range(8):
        kernel = monster
        if i & 0x1:
            kernel = kernel.T
        if i & 0x2:
            kernel = kernel[::-1]
        if i & 0x4:
            kernel = kernel[:, ::-1]
        con = scipy.ndimage.convolve(img, kernel, mode='constant')
        locs = (con == monster.sum()).sum()
        if locs:
            break

    return int(img.sum() - locs * monster.sum())

if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''Tile 2311:
    ..##.#..#.
    ##..#.....
    #...##..#.
    ####.#...#
    ##.##.###.
    ##...#.###
    .#.#.#..##
    ..#....#..
    ###...#.#.
    ..###..###

    Tile 1951:
    #.##...##.
    #.####...#
    .....#..##
    #...######
    .##.#....#
    .###.#####
    ###.##.##.
    .###....#.
    ..#.#..#.#
    #...##.#..

    Tile 1171:
    ####...##.
    #..##.#..#
    ##.#..#.#.
    .###.####.
    ..###.####
    .##....##.
    .#...####.
    #.##.####.
    ####..#...
    .....##...

    Tile 1427:
    ###.##.#..
    .#..#.##..
    .#.##.#..#
    #.#.#.##.#
    ....#...##
    ...##..##.
    ...#.#####
    .#.####.#.
    ..#..###.#
    ..##.#..#.

    Tile 1489:
    ##.#.#....
    ..##...#..
    .##..##...
    ..#...#...
    #####...#.
    #..#.#.#.#
    ...#.#.#..
    ##.#...##.
    ..##.##.##
    ###.##.#..

    Tile 2473:
    #....####.
    #..#.##...
    #.##..#...
    ######.#.#
    .#...#.#.#
    .#########
    .###.#..#.
    ########.#
    ##...##.#.
    ..###.#.#.

    Tile 2971:
    ..#.#....#
    #...###...
    #.#.###...
    ##.##..#..
    .#####..##
    .#..####.#
    #..#.#..#.
    ..####.###
    ..#.#.###.
    ...#.#.#.#

    Tile 2729:
    ...#.#.#.#
    ####.#....
    ..#.#.....
    ....#..#.#
    .##..##.#.
    .#.####...
    ####.#.#..
    ##.####...
    ##..#.##..
    #.##...##.

    Tile 3079:
    #.#.#####.
    .#..######
    ..#.......
    ######....
    ####.#..#.
    .#...#.##.
    #.#####.##
    ..#.###...
    ..#.......
    ..#.###...'''


    tiles = parse(t)
    l = assemble(tiles)
    assert l[0][0] * l[0][-1] * l[-1][0] * l[-1][-1] == 20899048083289

    img = stitch(l, tiles)
    assert roughness(img) == 273

    puz = Puzzle(2020, 20)

    tiles = parse(puz.input_data)
    l = assemble(tiles)

    puz.answer_a = l[0][0] * l[0][-1] * l[-1][0] * l[-1][-1]
    print(f'Part 1: {puz.answer_a}')

    img = stitch(l, tiles)
    puz.answer_b = roughness(img)
    print(f'Part 2: {puz.answer_b}')
