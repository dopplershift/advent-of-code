from collections import Counter
import itertools


def parse(s):
    return {(c, r)
            for r, line in enumerate(s.split('\n'))
            for c, char in enumerate(line)
            if char == '#'}


def neighborhood(loc):
    for deltas in itertools.product((-1, 0, 1), repeat=len(loc)):
        if any(deltas):
            yield tuple(x + dx for x, dx in zip(loc, deltas))


def solve(grid, iters, dims):
    grid = {pt + tuple([0] * (dims - len(pt))) for pt in grid}
    for _ in range(iters):
        # Get a pool of all potential sites, counting how many active cells call them neighbor
        candidates = Counter(itertools.chain.from_iterable(neighborhood(active) for active in grid))

        # The next grid is only those cells that meet the right count of neighbors
        grid = {loc for loc, count in candidates.items()
                if count == 3 or (count == 2 and loc in grid)}
    return grid


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''.#.
..#
###'''

    g = parse(t)

    assert len(list(neighborhood((0, 0, 0)))) == 26
    assert len(list(neighborhood((0, 0, 0, 0)))) == 80
    assert len(solve(g, 6, 3)) == 112
    assert len(solve(g, 6, 4)) == 848

    puz = Puzzle(2020, 17)
    grid = parse(puz.input_data)

    puz.answer_a = len(solve(grid, 6, 3))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = len(solve(grid, 6, 4))
    print(f'Part 2: {puz.answer_b}')
