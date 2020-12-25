def flip(s):
    grid = set()
    for tile in s.split('\n'):
        tile = tile.lstrip()
        pointer = 0
        x, y = 0, 0
        while pointer < len(tile):
            if tile[pointer] == 'e':
                pointer += 1
                dx, dy = 2, 0
            elif tile[pointer] == 'w':
                pointer += 1
                dx, dy = -2, 0
            elif tile[pointer] == 'n':
                pointer += 1
                if tile[pointer] == 'e':
                    pointer += 1
                    dx, dy = 1, 1
                elif tile[pointer] == 'w':
                    pointer += 1
                    dx, dy = -1, 1
            elif tile[pointer] == 's':
                pointer += 1
                if tile[pointer] == 'e':
                    pointer += 1
                    dx, dy = 1, -1
                elif tile[pointer] == 'w':
                    pointer += 1
                    dx, dy = -1, -1

            x += dx
            y += dy
        if (x, y) in grid:
            grid.remove((x,y))
        else:
            grid.add((x,y))
    return grid


def neighbors(loc):
    x, y = loc
    for dx, dy in ((2, 0), (1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1)):
        yield x + dx, y + dy


def iterate(g, n=100):
    for _ in range(n):
        next_grid = set()
        candidates = g | {n for tile in g for n in neighbors(tile)}
        for tile in candidates:
            count = sum(n in g for n in neighbors(tile))
            if tile in g and not (count == 0 or count > 2):
                next_grid.add(tile)
            elif tile not in g and count == 2:
                next_grid.add(tile)
        g = next_grid
    return g


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''sesenwnenenewseeswwswswwnenewsewsw
    neeenesenwnwwswnenewnwwsewnenwseswesw
    seswneswswsenwwnwse
    nwnwneseeswswnenewneswwnewseswneseene
    swweswneswnenwsewnwneneseenw
    eesenwseswswnenwswnwnwsewwnwsene
    sewnenenenesenwsewnenwwwse
    wenwwweseeeweswwwnwwe
    wsweesenenewnwwnwsenewsenwwsesesenwne
    neeswseenwwswnwswswnw
    nenwswwsewswnenenewsenwsenwnesesenew
    enewnwewneswsewnwswenweswnenwsenwsw
    sweneswneswneneenwnewenewwneswswnese
    swwesenesewenwneswnwwneseswwne
    enesenwswwswneneswsenwnewswseenwsese
    wnwnesenesenenwwnenwsewesewsesesew
    nenewswnwewswnenesenwnesewesw
    eneswnwswnwsenenwnwnwwseeswneewsenese
    neswnwewnwnwseenwseesewsenwsweewe
    wseweeenwnesenwwwswnew'''

    g = flip(t)
    assert len(g) == 10

    g = iterate(g, 100)
    assert len(g) == 2208

    puz = Puzzle(2020, 24)

    g = flip(puz.input_data)
    puz.answer_a = len(g)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = len(iterate(g, 100))
    print(f'Part 2: {puz.answer_b}')