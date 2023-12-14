class Platform:
    def __init__(self, nx, ny):
        self.xsize = nx
        self.ysize = ny
        self._grid = dict()
        self._string = None

    @classmethod
    def fromstring(cls, s):
        lines = s.split('\n')
        plat = cls(len(lines[0]), len(lines))
        plat._grid = {(x, y): c for y, line in enumerate(lines) for x, c in enumerate(line)}
        return plat

    def __getitem__(self, key):
        return self._grid[key]

    def __setitem__(self, key, val):
        self._grid[key] = val
        self._string = None

    def __iter__(self):
        return iter(self._grid.items())

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        if self._string is None:
            self._string = '\n'.join(''.join(self[x, y] for x in range(self.xsize))
                                     for y in range(self.ysize))
        return self._string

    __repr__ = __str__


def cycle(platform):
    for d in 'NWSE':
        platform = shift(platform, d)
    return platform


def shift(platform, direc):
    new_platform = Platform(platform.xsize, platform.ysize)

    if direc in 'NS':
        if direc == 'N':
            starty = 0
            endy = platform.ysize
            incy = 1
        else:
            starty = platform.ysize - 1
            endy = -1
            incy = -1
        for x in range(platform.xsize):
            available = starty
            for y in range(starty, endy, incy):
                if platform[x, y] == '#':
                    new_platform[x, y] = '#'
                    available = y + incy
                elif platform[x, y] == 'O':
                    new_platform[x, available] = 'O'
                    if available != y:
                        new_platform[x, y] = '.'
                    available += incy
                else:
                    new_platform[x, y] = platform[x, y]
    else:  # 'EW'
        if direc == 'W':
            startx = 0
            endx = platform.xsize
            incx = 1
        else:
            startx = platform.xsize - 1
            endx = -1
            incx = -1
        for y in range(platform.ysize):
            available = startx
            for x in range(startx, endx, incx):
                if platform[x, y] == '#':
                    new_platform[x, y] = '#'
                    available = x + incx
                elif platform[x, y] == 'O':
                    new_platform[available, y] = 'O'
                    if available != x:
                        new_platform[x, y] = '.'
                    available += incx
                else:
                    new_platform[x, y] = platform[x, y]
    return new_platform


def load(platform):
    return sum(platform.ysize - y for (_, y), val in platform if val == 'O')


def part2(platform):
    # Track cycle progression until we repeat
    loop = []
    n = 1_000_000_000
    for i in range(n):
        if platform in loop:
            break
        loop.append(platform)
        platform = cycle(platform)

    # Use the index into the sequence to figure out how long cycle is
    ind = (n - i) % (len(loop) - loop.index(platform) + 1)
    return loop[ind]


def run(data):
    platform = Platform.fromstring(data)
    return load(shift(platform, 'N')), load(part2(platform))

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''

    test_a, test_b = run(sample)
    assert test_a == 136
    assert test_b == 64

    puz = Puzzle(2023, 14)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
