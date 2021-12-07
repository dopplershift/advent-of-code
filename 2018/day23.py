# TODO: Part 2 is slow and seems really manually intensive
import numpy as np
from scipy.optimize import basinhopping


def parse(f):
    l = []
    for line in f:
        x, y, z, r = line.split(',')
        x = int(x.lstrip()[5:])
        y = int(y)
        z = int(z[:-1])
        r = int(r[3:])
        l.append((x, y, z, r))
    return np.array(l).T


def within_max(x, y, z, r):
    max_ind = r.argmax()
    return np.abs(x - x[max_ind]) + np.abs(y - y[max_ind]) + np.abs(z - z[max_ind]) <= r[max_ind]


def count_within(x, y, z, r, x0, y0, z0):
    return (np.abs(x - x0) + np.abs(y - y0) + np.abs(z - z0) <= r).sum()

if __name__ == '__main__':
    from aocd.models import Puzzle

    f = '''pos=<0,0,0>, r=4
    pos=<1,0,0>, r=1
    pos=<4,0,0>, r=3
    pos=<0,2,0>, r=1
    pos=<0,5,0>, r=3
    pos=<0,0,3>, r=1
    pos=<1,1,1>, r=1
    pos=<1,1,2>, r=1
    pos=<1,3,1>, r=1'''
    x, y, z, r = parse(f.split('\n'))
    assert within_max(x, y, z, r).sum() == 7

    f = '''pos=<10,12,12>, r=2
    pos=<12,14,12>, r=2
    pos=<16,12,12>, r=4
    pos=<14,14,14>, r=6
    pos=<50,50,50>, r=200
    pos=<10,10,10>, r=5'''
    x, y, z, r = parse(f.split('\n'))
    assert count_within(x, y, z, r, 12, 12, 12) == 5

    puz = Puzzle(2018, 23)
    x, y, z, r = parse(puz.input_data.split('\n'))
    mask = within_max(x, y, z, r)
    puz.answer_a = int(mask.sum())
    print(f'Part 1: {puz.answer_a}')

    x0 = (23837205, 58141311, 11772354)
    for _ in range(10):
        res = basinhopping(lambda xpt: 1000 - count_within(x, y, z, r, *xpt), x0, T=100, niter=100000)
        x0 = np.round(res['x'])
#         print(x0, res['fun'])

#     print(count_within(x, y, z, r, 23837205, 58141311, 11772354))

    puz.answer_b = int(sum(x0))
    print(f'Part 2: {puz.answer_b}')
