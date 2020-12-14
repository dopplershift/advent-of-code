import numpy as np


def coverage(locs):
    nearest = np.zeros((1000, 1000), dtype=np.int)
    best_dist = np.full_like(nearest, np.inf, dtype=np.float64)
    ygrid = np.arange(nearest.shape[0])[:, None]
    xgrid = np.arange(nearest.shape[1])
    for ind, (x, y) in enumerate(locs):
        dist = np.abs(x - xgrid) + np.abs(y - ygrid)
        even = dist == best_dist
        nearest[even] = -1
        better = dist < best_dist
        best_dist[better] = dist[better]
        nearest[better] = ind
    
    candidates = set(range(len(locs)))
    candidates -= set(nearest[:, 0])
    candidates -= set(nearest[:, -1])
    candidates -= set(nearest[0, :])
    candidates -= set(nearest[-1, :])
    
    return max((nearest == c).sum() for c in candidates)


def region_max_total_dist(locs, thresh=10000):
    size = 1000
    total_dist = np.zeros((size, size), dtype=np.int)
    ygrid = np.arange(total_dist.shape[0])[:, None]
    xgrid = np.arange(total_dist.shape[1])
    for ind, (x, y) in enumerate(locs):
        dist = np.abs(x - xgrid) + np.abs(y - ygrid)
        total_dist += dist
        
#    print(total_dist < thresh)
    return (total_dist < thresh).sum()


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert coverage([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]) == 17
    assert region_max_total_dist([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)], 32) == 16

    puz = Puzzle(2018, 6)
    locs = [tuple(map(int, l.split(','))) for l in puz.input_data.split('\n')]

    puz.answer_a = int(coverage(locs))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = int(region_max_total_dist(locs))
    print(f'Part 2: {puz.answer_b}')