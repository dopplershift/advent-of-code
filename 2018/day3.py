from collections import namedtuple

import numpy as np


Claim = namedtuple('Claim', 'ident left top width height')


def parse(f):
    for line in f:
        claim_id, square = line.split('@')
        claim_id = int(claim_id[1:])
        loc, size = square.split(':')
        left, top = map(int, loc.split(','))
        width, height = map(int, size.split('x'))
        yield Claim(claim_id, left, top, width, height)


def find_overlap_area(claims, size=1000):
    cloth = np.zeros((size, size))
    for claim in claims:
        cloth[claim.left:claim.left + claim.width, claim.top:claim.top + claim.height] += 1
    return (cloth > 1).sum()


def find_nonoverlap(claims, size=1000):
    cloth = np.zeros((size, size), dtype=int)
    candidates = set()
    for claim in claims:
        area = cloth[claim.left:claim.left + claim.width, claim.top:claim.top + claim.height]
        if np.any(area):
            # Overlaps with some existing claims. Get them and remove all of them from the candidates
            for claim_id in np.unique(area):
                candidates -= {claim_id}
        else:
            # No overlap, so add to candidates
            candidates.add(claim.ident)
        # Regardless we need to mark off the area
        area[:] = claim.ident
    return list(candidates)[0]


if __name__ == '__main__':
    from aocd.models import Puzzle

    claims = list(parse(['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']))
    assert find_overlap_area(claims) == 4

    assert find_nonoverlap(claims) == 3

    puz = Puzzle(2018, 3)
    claims = list(parse(puz.input_data.split('\n')))

    puz.answer_a = int(find_overlap_area(claims))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_nonoverlap(claims)
    print(f'Part 2: {puz.answer_b}')
