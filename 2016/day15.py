import re


discinfo = re.compile(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', re.ASCII)

def parse(s):
    discs, npos, offset = zip(*[re.search(discinfo, line).groups() for line in s.split('\n')])
    return [(n, d + o) for d, n, o in zip(map(int, discs), map(int, npos), map(int, offset))]


def crt(info):
    t = 0
    inc = 1
    for n, offset in sorted(info):
        while (t + offset) % n:
            t += inc
        inc *= n
    return t


if __name__ == '__main__':
    from aocd.models import Puzzle

    s = '''Disc #1 has 5 positions; at time=0, it is at position 4.
    Disc #2 has 2 positions; at time=0, it is at position 1.'''
    i = parse(s)

    assert crt(i) == 5

    puz = Puzzle(2016, 15)
    info = parse(puz.input_data)

    puz.answer_a = crt(info)
    print('Part 1:', puz.answer_a)

    puz.answer_b = crt(info + [(11, 7)])
    print('Part 2:', puz.answer_b)